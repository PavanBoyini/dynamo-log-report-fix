# NOTE: pin this to the current digest of your org's approved base image
# before using in production, e.g.:
#   docker pull python:3.12-slim
#   docker inspect --format='{{index .RepoDigests 0}}' python:3.12-slim
FROM python:3.12-slim@sha256:<pin-to-current-digest-of-approved-base>

RUN pip install --no-cache-dir pytest==8.4.1 pytest-json-ctrf==0.3.5

WORKDIR /app

COPY access.log /app/access.log
