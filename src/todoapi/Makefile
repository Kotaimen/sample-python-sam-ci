all: build

.PHONY: build clean

clean:
	python setup.py clean --all

build:
	# only build source dist so sam can build nativelly using lambci container.
	python setup.py build sdist
