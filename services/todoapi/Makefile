lambda_files := $(shell find ./lambdas -name '*.py') $(shell find ../../src -name '*.py')

all: build

.PHONY: build package clean

clean:
	rm -rf .aws-sam

build: .aws-sam/build/template.yaml
	@echo Build using sam-cli ...

.aws-sam/build/template.yaml: template.yaml $(lambda_files)
	sam build --debug --use-container --docker-network=host

package:
	cd .aws-sam/build && \
	sam package \
		--output-template-file packaged.yaml \
		--s3-bucket ${S3_BUCKET} \
		--s3-prefix ${S3_PREFIX} \
		--kms-key-id ${KMS_KEY_ID}
