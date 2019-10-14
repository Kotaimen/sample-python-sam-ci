lambda_files := $(shell find ./lambdas -name '*.py') $(shell find ../../src -name '*.py')

all: build

.PHONY: build package clean

clean:
	rm -rf .aws-sam

build: .aws-sam/build/template.yaml
	@echo Build using sam-cli ...

.aws-sam/build/template.yaml: template.yaml $(lambda_files)
	sam build --debug

package: build
	cd .aws-sam/build && sam package --output-template-file packaged.yaml --s3-bucket ${TEMPLATE_BUCKET} --s3-prefix ${TEMPLATE_PREFIX} --kms-key-id ${KMS_KEY_ARN}
