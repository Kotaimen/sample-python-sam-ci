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
	@$(PIPENV) clean
	@$(MAKE) -C services clean



#
# Pipenv
#
env: requirements.txt requirements-dev.txt Pipfile.lock
	@$(PIPENV) sync --dev

update: Pipfile
	docker pull lambci/lambda:build-python3.7
	docker pull lambci/lambda:python3.7
	@$(PIPENV) update --dev

Pipfile.lock: Pipfile
	@$(PIPENV) lock --dev
	@echo updated pipenv with develop depedencies

requirements.txt: Pipfile.lock
	@$(PIPENV) lock --requirements > $@
	@echo generated requirements.txt

requirements-dev.txt: Pipfile.lock
	@$(PIPENV) run pip install black
	@$(PIPENV) lock --dev --requirements > $@
	@echo generated requirements-dev.txt

#
# SAM
#
layers: env
	@$(MAKE) -C infra/lambda-layers build

build:
	@$(MAKE) -C services build

package:
	@$(MAKE) -C services package

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

todo...
endef
