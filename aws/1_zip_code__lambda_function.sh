#!/bin/bash

# 1_zip_code__lambda_function.sh:
# Utility function that packages the contents of bot/ into a file called thorchainbot_code__lambda_function.zip
# You'll upload this file to the Lambda function.

# Make sure you are running this script from project root directory:
# > sh aws/1_zip_code__lambda_function.sh

cd bot/
zip ../thorchainbot_code__lambda_function.zip * -x "__pycache__*"