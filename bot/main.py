import logging
import os
import pprint as pp

import tweepy
from dotenv import load_dotenv

load_dotenv()


class THORChainBot:
    def __init__(self):
        self.client = self.get_client_api_oauth1_api_v2()
        self.RETWEETABLE_CNT = 1
        self.THORCHAIN_BOT_LIST_MEMBERS: list = []
        self.THORCHAIN_BOT_LIST_ID: int = os.getenv("THORCHAIN_BOT_LIST_ID")
        self.RETWEETABLE_TWEET_IDS: list = []
        self.RETWEETABLE_TWEETS: dict = {}

    @staticmethod
    def get_client_api_oauth1_api_v2():
        """
        Sets up Twitter Auth using OAuth1 and Twitter's v2 APIs.
        :return: Authenticated Twitter client
        """
        logger.debug("Setting up API client using OAuth1 and APIs v2...")
        try:
            client = tweepy.Client(
                bearer_token=os.getenv("BEARER_TOKEN"),
                consumer_key=os.getenv("CONSUMER_KEY"),
                consumer_secret=os.getenv("CONSUMER_SECRET"),
                access_token=os.getenv("ACCESS_TOKEN"),
                access_token_secret=os.getenv("ACCESS_TOKEN_SECRET"),
            )
        except Exception as e:
            logger.error(f"Error creating API client", exc_info=True)
            raise e
        logger.debug("API client created.")
        return client

    def get_accounts_from_list(self):
        """
        Gets member information from THORCalendarBot's curated list
        """
        get_list_response: tweepy.client.Response = self.client.get_list(self.THORCHAIN_BOT_LIST_ID)
        if get_list_response.data:
            list_name = get_list_response.data.name
            list_id = get_list_response.data.id
        accs: dict = self.client.get_list_members(id=self.THORCHAIN_BOT_LIST_ID)
        members_info: dict = {}

        for acc in accs.data:
            members_info[acc.id] = acc.username
        self.THORCHAIN_BOT_LIST_MEMBERS = members_info
        logger.info(f"{list_name} ({list_id}) has {len(members_info)} members:\n{members_info}")
        return

    def download_and_filter_tweets_from_list(self, results=100):
        """
        Downloads tweets from the list of curated accounts maintained for THORCalendarBot. Then filters out the tweets
        based on customizable filters.
        :param results: Customize amount of tweets to download
        :return: A list of all filtered Retweetable Tweet IDs
        """
        list_all_tweets: list = []
        list_tweets_response: tweepy.client.Response = self.client.get_list_tweets(
            self.THORCHAIN_BOT_LIST_ID,
            max_results=(100 if results > 100 else results),
            tweet_fields=["author_id,entities,text,created_at"],
            user_fields=["public_metrics"],
        )
        list_all_tweets.extend(list_tweets_response.data)
        results -= list_tweets_response.meta.get('result_count')
        logger.info(f"Remaining results: {results}")

        if results > 0:
            pagination_token: str = list_tweets_response.meta.get('next_token')
            while results > 0:
                list_tweets_response: tweepy.client.Response = self.client.get_list_tweets(
                    self.THORCHAIN_BOT_LIST_ID,
                    max_results=(100 if results > 100 else results),
                    tweet_fields=["author_id,entities,text,created_at"],
                    user_fields=["public_metrics"],
                    pagination_token=pagination_token,
                )
                list_all_tweets.extend(list_tweets_response.data)
                results -= list_tweets_response.meta.get('result_count')
                logger.info(f"Remaining results: {results}")
                pagination_token = list_tweets_response.meta.get('next_token')
        logger.info(list_all_tweets)

        for tweet in list_all_tweets:
            while nottweetable := True:
                # List out different filter functions - Add additional filters below!
                self.filter_by_twitter_space_urls(tweet)
                if nottweetable:
                    logger.info(f"Skipping tweet ID: {tweet['id']}")
                    break
        logger.info(f"Retweetable Tweet IDs: {self.RETWEETABLE_TWEET_IDS}")
        return self.RETWEETABLE_TWEET_IDS

    def log_retweetable_tweets_data(self):
        """
        Logs Retweetable Tweet data to the console and to a log file.
        """
        logger.info(f"Length of RETWEETABLE_TWEETS: {len(self.RETWEETABLE_TWEET_IDS)}{os.linesep}")
        for i, tweet in enumerate(self.RETWEETABLE_TWEETS.keys(), start=1):
            t = self.RETWEETABLE_TWEETS[tweet]
            logger.info(
                f"#{i} {'-' * 50}{os.linesep}"
                f"author_username: {self.THORCHAIN_BOT_LIST_MEMBERS[int(t.data['author_id'])]},{os.linesep}"
                f"created_at: {t.created_at},{os.linesep}"
                f"tweet_id: {t.data['id']},{os.linesep}"
                f"expanded_url: {t.entities['urls'][0]['expanded_url']},{os.linesep}"
                f"data: {t.data['text']} {os.linesep}"
            )

        # Only export logs if this file ('main.py') is run directly
        if __name__ == '__main__':
            with open("../logs/log__retweetable_tweets.txt", "w") as f:
                for id in self.RETWEETABLE_TWEET_IDS:
                    pp.pprint(self.RETWEETABLE_TWEETS[id].data, stream=f)
        else:
            for id in self.RETWEETABLE_TWEET_IDS:
                logger.info(self.RETWEETABLE_TWEETS[id].data)

    def filter_by_twitter_space_urls(self, tweet):
        """
        Filter: identifies tweets that contain a Twitter Space embedded link. If filter identifies a valid tweet,
        add tweet ID to the 'RETWEETABLE_TWEET_IDS' field.
        """
        if (tweet.get('entities') or {}).get('urls'):
            urls: list = tweet.entities.get('urls')
            for url in urls:
                if "/spaces/" in url.get('expanded_url'):
                    self.RETWEETABLE_TWEET_IDS.append(tweet['id'])
                    logger.info(f"Adding tweet ID: {tweet['id']} {'=' * 20} #{self.RETWEETABLE_CNT}")
                    self.RETWEETABLE_TWEETS[tweet.id] = tweet
                    self.RETWEETABLE_CNT += 1
                    break

    def retweet_tweets(self):
        """
        Retweets tweets that have identified and saved to RETWEETABLE_TWEET_IDS (They have passed the filter criteria).
        """
        if self.RETWEETABLE_TWEET_IDS is []:
            logger.error("No retweetable tweets found.")

        tweets: list = self.RETWEETABLE_TWEET_IDS
        for i, tweet in enumerate(tweets[::-1], start=1):
            retweet_response = self.client.retweet(tweet)
            self.client.like(tweet)
            if retweet_response.data.get('retweeted'):
                logger.info(f"{i} - SUCCESSFULLY retweeted tweet ID: {tweet}")
            else:
                logger.error(f"FAILED to retweet tweet ID: {tweet}")
        return


def lambda_handler(event, context):
    """
    Function for AWS Lambda to call.
    :param event: default for AWS
    :param context:  default for AWS
    """
    logging.getLogger().setLevel(logging.INFO)
    global logger
    logger = logging.getLogger()
    run_thorchain_bot()


def run_thorchain_bot():
    """
    Main function that runs the THORChain Twitter Bot.
    """
    thorchainbot = THORChainBot()
    thorchainbot.get_accounts_from_list()
    thorchainbot.download_and_filter_tweets_from_list(results=100)
    thorchainbot.log_retweetable_tweets_data()
    # thorchainbot.retweet_tweets()
    print('End')


if __name__ == '__main__':
    # If running 'main.py' file directly: sets up logging accordingly
    logging.basicConfig(level=logging.INFO,
                        filename="../logs/log__twitter_feed_log.txt",
                        filemode="w")
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger().addHandler(console)
    logger = logging.getLogger()

    run_thorchain_bot()
