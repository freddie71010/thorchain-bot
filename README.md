# thorchain-bot

This repo contains the source code to run a twitter bot for the @THORChain crypto community.

## How to Run
- Set up a virtual environment. Install `requirements.txt`.
- Create a `.env` file to store all of your credentials.
- Ucomment line 180: `# thorchainbot.retweet_tweets()` to retweet all tweets.

## Local Run Setup
- The `main.py` script will output two separate log files into a `/logs`  directory.

## AWS Lambda Setup
- Run the two scripts in chronological order located in the `/aws` directory. Make sure you run them ***from*** the home directory (AKA `thorchain-bot/`). These two bash scripts will generate the required zip files for use in AWS.
- Log into AWS and upload zip files:
  - *lambda_function.zip = upload as a Lambda Function
  - *lambda_layer.zip = upload as a Lambda Layer
- In AWS, set the `Runtime Settings > Handler > main.lambda_handler`
- Logs will all be combined into one format and viewable in AWS CloudWatch
