#TEMPLATE_BUCKET=samdemo-prereq-artifactbucket-eq2mr518p3dq
#TEMPLATE_PREFIX=codebuild-packaged-templates
#KMS_KEY_ARN=arn:aws:kms:us-east-1:877602539438:key/1a1157aa-d9ed-4b01-b1b2-b7c0baae0843


all: package

.PHONY: clean package layers build

clean:
	rm -rf build

common-layer/requirements.txt: ../../requirements.txt
	# Remove any editable packages from lambda layers
	cat $< | sed '/^-e /d'  > $@

build/common-layer.md5: common-layer/requirements.txt
	mkdir -p build
	md5sum $< | cut -f 1 -d " " > $@

build/common-layer.zip: common-layer/build.sh build/common-layer.md5
	# Mounted directories:
	# - /var/task: build source, aka this file and requirements.txt
	# - /var/build/staging: pip staging dir
	# - /var/build/output: layer.zip
	docker run --rm \
		-v $(CURDIR)/common-layer/:/var/task/:ro \
		-v $(CURDIR)/build/:/tmp/build/ \
		-w /tmp/build/ \
		lambci/lambda:build-python3.7 \
		bash /var/task/build.sh

build: build/common-layer.zip

package: build
	sam package --output-template-file build/packaged.yaml \
		--s3-bucket ${TEMPLATE_BUCKET} \
		--s3-prefix ${TEMPLATE_PREFIX} \
		--kms-key-id ${KMS_KEY_ARN}