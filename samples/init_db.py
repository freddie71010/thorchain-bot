from store_data import StoreData

if __name__ == "__main__":

    defaultToken = {
        "access_token": "XXX",
        "refresh_token": "XXX",
        "expires_at": 0
    }

    StoreData.set_oauth_token(defaultToken)
    StoreData.set_last_twitter_id(None)
    print("Init Database - done")
