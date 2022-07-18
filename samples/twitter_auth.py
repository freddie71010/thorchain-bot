import tweepy
import time
import os


class TweeterAuth:
    @staticmethod
    def get_oauth_handler() -> tweepy.OAuth2UserHandler:
        return tweepy.OAuth2UserHandler(
            client_id=os.getenv("ACCESS_TOKEN"),
            redirect_uri=os.getenv("REDIRECT_URI"),
            scope=os.getenv("API_SCOPES").split(" "),
            client_secret=os.getenv("ACCESS_TOKEN_SECRET"))

    @staticmethod
    def get_access_token(token: dict) -> dict:
        handler = __class__.get_oauth_handler()
        return handler.refresh_token(
            os.getenv("TWITTER_API_REFRESH_TOKEN_URI"),
            refresh_token=token["refresh_token"])

    @staticmethod
    def token_has_expired(token: dict) -> bool:
        timeout = int(os.getenv("API_TOKEN_TIMEOUT", 0))
        return (time.time() + timeout) >= token["expires_at"]
