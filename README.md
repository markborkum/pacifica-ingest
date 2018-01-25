# Pacifica Ingest
[![Build Status](https://travis-ci.org/pacifica/pacifica-ingest.svg?branch=master)](https://travis-ci.org/pacifica/pacifica-ingest)
[![Build status](https://ci.appveyor.com/api/projects/status/dhniln12ili29kgm?svg=true)](https://ci.appveyor.com/project/dmlb2000/pacifica-ingest)
[![Code Climate](https://codeclimate.com/github/pacifica/pacifica-ingest/badges/gpa.svg)](https://codeclimate.com/github/pacifica/pacifica-ingest)
[![Test Coverage](https://codeclimate.com/github/pacifica/pacifica-ingest/badges/coverage.svg)](https://codeclimate.com/github/pacifica/pacifica-ingest/coverage)
[![Issue Count](https://codeclimate.com/github/pacifica/pacifica-ingest/badges/issue_count.svg)](https://codeclimate.com/github/pacifica/pacifica-ingest)

## Docker Badges
[![Frontend Stars](https://img.shields.io/docker/stars/pacifica/ingest-frontend.svg?maxAge=2592000)](https://cloud.docker.com/swarm/pacifica/repository/docker/pacifica/ingest-frontend/general)
[![Backend Stars](https://img.shields.io/docker/stars/pacifica/ingest-backend.svg?maxAge=2592000)](https://cloud.docker.com/swarm/pacifica/repository/docker/pacifica/ingest-backend/general)
[![Frontend Pulls](https://img.shields.io/docker/pulls/pacifica/ingest-frontend.svg?maxAge=2592000)](https://cloud.docker.com/swarm/pacifica/repository/docker/pacifica/ingest-frontend/general)
[![Backend Pulls](https://img.shields.io/docker/pulls/pacifica/ingest-backend.svg?maxAge=2592000)](https://cloud.docker.com/swarm/pacifica/repository/docker/pacifica/ingest-backend/general)
[![Frontend Automated build](https://img.shields.io/docker/automated/pacifica/ingest-frontend.svg?maxAge=2592000)](https://cloud.docker.com/swarm/pacifica/repository/docker/pacifica/ingest-frontend/builds)
[![Backend Automated build](https://img.shields.io/docker/automated/pacifica/ingest-backend.svg?maxAge=2592000)](https://cloud.docker.com/swarm/pacifica/repository/docker/pacifica/ingest-backend/builds)

Pacifica data ingest service to process and validate incoming data from the uploader.

Ingest and validate data from the pacifica-uploader

# Building and Installing

This code depends on the following libraries and python modules:

Docker/docker-compose

Peewee

Celery

MySQL-Python

This is a standard python distutils build process.

```
python ./setup.py build
python ./setup.py install
```

# Running It

To bring up a test instance use docker-compose

```
docker-compose up
```

# Bundle Format

The bundle format is parsed using Python [tarfile](https://docs.python.org/2/library/tarfile.html)
with some additions. The metadata is kept in a file in the bundle as well as the data. The
metadata is put in a file called `metadata.txt` and is JSON formatted. The data is put under the
directory `data` in the bundle so it does not have name conflicts with the `metadata.txt` file.

So an example bundle as shown by running `tar -tf` on it is as follows:
```
data/a/b/foo.txt
data/a/c/bar.txt
metadata.txt
```

# API Examples

The endpoints that define the ingest process are as follows. The assumption is that the installer
knows the IP address and port the WSGI service is listening on.

## Ingest (Single HTTP Request)

Post a bundle ([defined above](#bundle-format)) to the endpoint.

```
POST /ingest
... tar bundle as body ...
```

The response will be the job ID information as if you requested it directly.

```json
{
  "job_id": 1234,
  "state": "OK",
  "task": "UPLOADING",
  "task_percent": "0.0",
  "updated": "2018-01-25 16:54:50",
  "created": "2018-01-25 16:54:50",
  "exception": ""
}
```

Failures that exist with this endpoint are during the course of uploading the bundle.
Sending data to this endpoint should consider long drawn out HTTP posts that maybe
longer than clients are used to handling.

## Get State for Job

Using the `job_id` field from the HTTP response from an ingest.

```json
GET /get_state?job_id=1234
{
  "job_id": 1234,
  "state": "OK",
  "task": "ingest files",
  "task_percent": "0.0",
  "updated": "2018-01-25 17:00:32",
  "created": "2018-01-25 16:54:50",
  "exception": ""
}
```

As the bundle of data is being processed errors may occure, if that happens the following
will be returned. It is useful when consuming this endpoint to plan for failures. Consider
logging or showing a message visable to the user that shows the ingest failed.

```json
GET /get_state?job_id=1234
{
  "job_id": 1234,
  "state": "FAILED",
  "task": "ingest files",
  "task_percent": "0.0",
  "updated": "2018-01-25 17:01:02",
  "created": "2018-01-25 16:54:50",
  "exception": "... some crazy python back trace ..."
}
```

# CLI Tools
