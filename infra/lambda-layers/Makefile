all: package

.PHONY: clean package layers build

LAMBDA_RUNTIME ?= python3.7

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
		lambci/lambda:build-${LAMBDA_RUNTIME} \
		bash /var/task/build.sh

build: build/common-layer.zip

package: build
	sam package --output-template-file build/packaged.yaml \
		--s3-bucket ${S3_BUCKET} \
		--s3-prefix ${S3_PREFIX} \
		--kms-key-id ${KMS_KEY_ID}
