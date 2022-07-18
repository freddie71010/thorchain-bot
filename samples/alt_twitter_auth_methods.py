import os
import tweepy


class THORChainBot:
    def __init__(self):
        # self.client = self.get_client_api_oauth1_apiV1()
        # self.client = self.get_client_api_oauth2_pkce_apiV2()
        pass

    @staticmethod
    def get_client_api_oauth1_apiV1():
        # Twitter API v1.1 Interface ----------------------------------------
        consumer_key = os.getenv("CONSUMER_KEY")
        consumer_secret = os.getenv("CONSUMER_SECRET")
        access_token = os.getenv("ACCESS_TOKEN")
        access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        return api

    @staticmethod
    def get_client_api_oauth2_pkce_apiV2():
        logger.debug("Setting up API client using OAuth2 PKCE and APIs v2...")
        try:
            oauth2_user_handler = tweepy.OAuth2UserHandler(
                client_id=os.getenv("CONSUMER_KEY"),
                client_secret=os.getenv("CONSUMER_SECRET"),
                redirect_uri="https://www.thorchain.com",
                scope=os.getenv("API_SCOPES").split(" "),
            )
            oauth2_url = oauth2_user_handler.get_authorization_url()
            logger.debug(oauth2_url)
            access_token = oauth2_user_handler.fetch_token(oauth2_url)
            client = tweepy.Client(access_token)
        except Exception as e:
            logger.error(f"Error creating API client", exc_info=True)
            raise e
        logger.debug("API client created.")
        return client
