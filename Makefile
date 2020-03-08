BASE := $(shell /bin/pwd)
PIPENV ?= pipenv
CFNCLI ?= cfn-cli

.PHONY: target env update layers

all: target

target:
	$(info ${HELP_MESSAGE})
	@exit 0

clean:
	@echo Cleaning...
	@$(MAKE) -C infra/lambda-layers clean
	@$(MAKE) -C src/todoapi clean
	@$(MAKE) -C services/todoapi clean

#
# Pipenv
#
env: requirements.txt requirements-dev.txt Pipfile.lock
	@$(PIPENV) sync --dev

update: Pipfile
	@$(PIPENV) update --dev

Pipfile.lock: Pipfile
	@$(PIPENV) lock --dev

requirements.txt: Pipfile.lock
	@$(PIPENV) lock --requirements > $@

requirements-dev.txt: Pipfile.lock
	#@$(PIPENV) run pip install black
	@$(PIPENV) lock --dev --requirements > $@

#
# SAM
#
layers: env
	@$(MAKE) -C infra/lambda-layers build

build:
	@$(MAKE) -C src/todoapi build
	@$(MAKE) -C services/todoapi build

package: build
	@$(MAKE) -C services/todoapi package

#
# Code quality
#
test:
	pytest

coverage:
	pytest --cov=src

lint:
	flake8 --config=.flake8
	bandit -r src

cfn-lint:
	cfn-lint --format parseable

format:
	black ./src ./tests/unit

define HELP_MESSAGE

env
  Boostrap/update enviroment.

update
  Update docker and pipenv environment.

layers:
  Build lambda layers.

build
  Build lambda functions.

package
  Package CloudFormation templates, requires following enviroment variables:
    S3_BUCKET: s3 bucket to write packaged resources.
    S3_PREFIX: s3 prefix to write packaged resources.
    KMS_KEY_ID: KMS key to encrypt resources.

test
  Run unittest on lambda functions.

coverage
  Run code coverage using unittests.

lint
  Run code lint on lambda functions.

cfn-lint
  CloudFormation template lint.

format
  Format code using Black.

endef
