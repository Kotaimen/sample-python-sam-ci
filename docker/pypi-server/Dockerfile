FROM lambci/lambda:build-python3.8

RUN \
    pip install pypiserver

EXPOSE 8080
VOLUME ["/packages"]
ENTRYPOINT  ["pypi-server", "-p", "8080", "/packages"]

