#!/bin/bash

# 2_create_venv__lambda_layer.sh:
# Utility function that packages the libraries specified in requirements into a file called thorchainbot_venv__lambda_layer.zip
# You'll upload this file to a Lambda Layer.

# Make sure you are running this script from project root directory && and run as admin:
# > sudo sh aws/2_create_venv__lambda_layer.sh 3.8


if [ "$1" != "" ] || [$# -gt 1]; then
	echo "Creating THORChainBot lambda layer compatible with python version $1"
	docker run -v "$PWD":/var/task "lambci/lambda:build-python$1" /bin/sh -c "pip install -r requirements.txt -t python/lib/python$1/site-packages/; exit"
	zip -r thorchainbot_venv__lambda_layer.zip python > /dev/null
	rm -rf python
	echo "Done creating THORChainBot lambda layer!"
	ls -lah thorchainbot_venv__lambda_layer.zip

else
	echo "Enter python version as argument - ./2_create_venv__lambda_layer.sh 3.8"
fi