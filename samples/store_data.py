# from replit import db
# import json


class StoreData:

    @staticmethod
    def get_oauth_token() -> dict:
        return json.loads(db.get_raw("oauth_token"))

    @staticmethod
    def set_oauth_token(token: dict) -> None:
        db.set_raw("oauth_token", json.dumps(token))

    @staticmethod
    def get_last_twitter_id() -> str:
        return db["last_twitter_id"]

    @staticmethod
    def set_last_twitter_id(last_id: str) -> None:
        db["last_twitter_id"] = last_id
