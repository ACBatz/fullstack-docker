#!/bin/bash

docker build --tag base --file Dockerfile.base .

docker build --tag batzel-globe --file Dockerfile.app .

docker run -d -p 5000:5000 --name batzel-globe batzel-globe