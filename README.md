# Python SAM Application with Matrix CI/CD

This sample shows how to create python SAM application with "matrix" CodePipelines.

> Disclaimer: I use `cfn-cli` to deploy base CloudFormation templates but deploy using vanilla `aws-cli` or just Console is also ok, but in that case, I need copy stack outputs across region & accounts.

Highlights:

* Sample REST API developed using Flask and SAM.
  * Codebase is separated from lambda environment thus can be developed & tested as a regular Flask application.
* Build and run lambda functions locally, with help from `sam-local`.
* Cross region, cross account CodePipelines.
* "Collapsable" CloudFormation template controlled by parameter:
  * Deploys to same account or cross account.
  * Deploys to single primary region or two regions.
  * 1~3 stages.

Directory structures:

| Path                       | Description                                                  |
| -------------------------- | ------------------------------------------------------------ |
| `ci-base/`                 | CloudFormation templates for CI pipeline base infrastructure. |
| `ci-pipelines/`            | CloudFormation templates for CodePipelines.                  |
| `infra/lambda-layers/`     | CloudFormation template and scripts to build lambda layer.   |
| `services/todoapi/`        | CloudFormation template and wrapper code for TODOAPI service. |
| `src/todoapi/`             | TODOAPI codebase as a installable package, using `flask-restplus`. |
| `docker/`                  | Docker compose files for local build&test.                   |
| `tests/unit/test_todoapi/` | Unittests for todoapi, based on `Flask` unittest support.    |

## QuickStart

Note on "project identifier": Each set of infra deployment share a unique project identifier to break circular dependency between cross-account roles.

### Bootstrap Environment

Pre-requests (assuming a mac, but any recent Linux disto should work):

- Python 3.8 with pipenv
- Docker Desktop
- make
- md5sum

Goto project environment then run `make env` to create the virtual environment, then type `pipenv shell` to spawn a shell within the virtualenv:

```shell
> make env
...
Creating a virtualenv for this project…
Pipfile: ~/workspace/sample-python-sam-ci/Pipfile
Using /usr/local/bin/python3 (3.7.8) to create virtualenv…
...
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.
All dependencies are now up-to-date!

> pipenv shell
Loading .env environment variables…
Launching subshell in virtual environment…
Welcome to fish, the friendly interactive shell
(sample-python-sam-ci) bob@bigmac ~/sample-python-sam-ci> 
```

#### Optional: Update Package Lock

 `Pipfile.lock` and `requirements.txt` file contains last known good stable dependency, refresh these using:

```shell
> make update env layers
```

## "Matrix" Setup

This is the most complicated setup where the pipelines stays in tools account, deploy lambda and api stacks cross account and cross region.

<img src="media/image-20191104204700438.png" alt="image-20191104204700438" style="zoom:33%;" />

The pipeline have multiple stages and actions (hence the "matrix"):

<img src="media/Screen%20Shot%202020-03-07%20at%208.22.32%20PM.png" alt="Screen Shot 2020-03-07 at 8.22.32 PM" style="zoom:33%;" />

To deploy this, you'll need:

* Two AWS Accounts:
  * Tools
  * Production
* AWS profiles of accounts above with administrator role.

First, open `cfn-cli.yaml` in editor, replace following string:

| Replace          | With                                 |
| ---------------- | ------------------------------------ |
| `<profile-1>`    | Profile name for tools account.      |
| `<profile-3>`    | Profile name for production account. |
| `<account1>`     | Tools account ID.                    |
| `<prod-account>` | Production account ID.               |

Then, deploy stacks using: 

```shell
> cfn-cli stack deploy
Deploying stack CIBase.PipelineRole
...
...
(output omitted)
...
...
Stack deployment complete.

```

This process take ~20 minutes,  and following stacks are created:

| Stack Name                 | Account    | Region                | Description                                                  |
| -------------------------- | ---------- | --------------------- | ------------------------------------------------------------ |
| `pysamci-roles`            | Tools      | us-east-1             | Pipeline and CloudFormation roles for same-account deployment. |
| `pysamci-prereq`           | Tools      | us-west-2 (secondary) | Artifact bucket in secondary region.                         |
| `pysamci-prereq`           | Tools      | us-east-1             | Source & artifact bucket for the pipelines.                  |
| `pysamci-roles`            | Production | us-east-1             | Pipeline and CloudFormation roles for cross-account deployment. |
| `pysamci-pipeline-layers`  | Tools      | us-east-1             | CodePipeline to build, deploy lambda layer.                  |
| `pysamci-pipeline-todoapi` | Tools      | us-east-1             | CodePipeline to build and deploy todoapi service.            |

CodePipelines created by last two stacks in primary region:

| CodePipeline Name    | Description                    |
| -------------------- | ------------------------------ |
| `pysamci-todolayers` | Build and deploy lambda layer. |
| `pysamci-todoapi`    | Build and deploy TODOAPI.      |

To tigger CodePipeline so start deployment, goto CloudFormation console, find  `pysamci-prereq` stack in `us-east-1` region, goto Outputs tab and find output value named `SourceBucket`, then, zip up the code base and copy it to the source bucket: 

```shell
> zip -x '.idea/*' '.git/*' '.env' '*.zip' '*/.aws-sam/*' -9 -FS source.zip -r .
> aws s3 cp source.zip s3://<SourceBucket>
```

This should trigger the pipelines starting deploy CI managed stacks in two accounts and two regions:

|                        | Primary Region (us-east-1) | Secondary Region (us-west-2) |
| ---------------------- | -------------------------- | ---------------------------- |
| **Tools Account**      | `todolayer-dev`            | `todolayer-dev`              |
|                        | `todoapi-dev`              | `todoapi-dev`                |
| **Production Account** | `todolayer-prod`           | `todolayer-prod`             |
|                        | `todoapi-prod`             | `todoapi-prod`               |

## Local Build

TBD