LAMBDA_BUILD_IMAGE := lambci/lambda:build-python3.7

all: build

build: build/layer.zip

clean:
	rm -f requirements.txt
	rm -rf build

# Remove any editable packages from lambda layers
requirements.txt: ../../../requirements.txt
	cat $< | sed '/^-e /d'  > $@

# Only rebuild when requirements.
build/requirements.md5: requirements.txt
	mkdir -p build
	md5 -q $< > $@

# Mounted directories:
# - /var/task: build source, aka this file and requirements.txt
# - /var/build/staging: pip staging dir
# - /var/build/output: layer.zip
build/layer.zip: build/requirements.md5 build.sh
	mkdir -p build
	docker run --rm \
		-v $(CURDIR):/var/task/:ro \
		-v $(CURDIR)/build:/var/build/ \
		-w /var/build/ \
		$(LAMBDA_BUILD_IMAGE) bash /var/task/build.sh
	@ls -lah $@

.PHONY: build clean
