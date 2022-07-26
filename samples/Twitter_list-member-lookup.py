import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.getenv("BEARER_TOKEN")


def list_member_lookup():
    # User fields are adjustable, options include:
    # created_at, description, entities, id, location, name,
    # pinned_tweet_id, profile_image_url, protected,
    # public_metrics, url, username, verified, and withheld
    user_fields = "user.fields=created_at,description,verified"
    # You can replace list-id with the List ID you wish to find members of.
    id = os.getenv("THORCHAIN_BOT_LIST_ID")
    url = "https://api.twitter.com/2/lists/{}/members".format(id)
    return url, user_fields

def list_tweets():
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    tweet_fields = "tweet.fields=lang,author_id"
    # Be sure to replace list-id with any List ID
    id = os.getenv("THORCHAIN_BOT_LIST_ID")
    url = "https://api.twitter.com/2/lists/{}/tweets".format(id)
    return url, tweet_fields


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2ListMembersLookupPython"
    return r


def connect_to_endpoint(url, user_fields):
    response = requests.request("GET", url, auth=bearer_oauth, params=user_fields)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def main():
    url, user_fields = list_member_lookup()
    json_response = connect_to_endpoint(url, user_fields)
    print(json.dumps(json_response, indent=4, sort_keys=True))

    url, tweet_fields = list_tweets()
    json_response = connect_to_endpoint(url, tweet_fields)
    print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()