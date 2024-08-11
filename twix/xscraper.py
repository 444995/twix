import json
import re
import requests
from requests.exceptions import RequestException
from datetime import datetime
from .exceptions import TokenRetrievalError, GuestIDRetrievalError, UserDataExtractionError

BASE_URL = 'https://x.com/'
GUEST_ID_URL = 'https://twitter.com/x/migrate'
API_URL = 'https://api.x.com/graphql/Yka-W8dz7RaEuQNkroPkYw/UserByScreenName'
AUTH_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAMupswEAAAAANC5Yk%2FHGiZmGDRV3EhXMBO3uX08%3DEwAT9YySxXZXGrYScXeoKUaeyqXQFeNVWUW4SaZUvtegCUVjIi'


class TokenRetriever:
    @staticmethod
    def get_tok():
        try:
            response = requests.get(BASE_URL)
            response.raise_for_status()
            match = re.search(r'tok=([^"&]+)', response.text)
            if not match:
                raise TokenRetrievalError("Failed to extract 'tok' from the response content")
            return match.group(1)
        except RequestException as e:
            raise TokenRetrievalError(f"Failed to retrieve 'tok': {str(e)}") from e

class GuestIDRetriever:
    @staticmethod
    def get_guest_id(tok):
        try:
            response = requests.get(GUEST_ID_URL, params={'tok': tok})
            response.raise_for_status()
            guest_id = response.cookies.get('guest_id')
            if guest_id is None:
                raise GuestIDRetrievalError("Failed to extract 'guest_id' from the response content")
            return guest_id
        except RequestException as e:
            raise GuestIDRetrievalError(f"Failed to retrieve 'guest_id': {str(e)}") from e

class UserDataExtractor:
    def __init__(self, guest_id):
        self.guest_id = guest_id

    def extract_user_data(self, username):
        headers = {
            'Authorization': f'Bearer {AUTH_TOKEN}',
            'Content-Type': 'application/json',
            'X-Guest-Token': self.guest_id,
        }

        params = {
            'variables': json.dumps({"screen_name": username, "withSafetyModeUserFields": True}),
            'features': json.dumps({
                "hidden_profile_subscriptions_enabled": True,
                "rweb_tipjar_consumption_enabled": True,
                "responsive_web_graphql_exclude_directive_enabled": True,
                "verified_phone_label_enabled": False,
                "subscriptions_verification_info_is_identity_verified_enabled": True,
                "subscriptions_verification_info_verified_since_enabled": True,
                "highlights_tweets_tab_ui_enabled": True,
                "responsive_web_twitter_article_notes_tab_enabled": True,
                "subscriptions_feature_can_gift_premium": True,
                "creator_subscriptions_tweet_preview_api_enabled": True,
                "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                "responsive_web_graphql_timeline_navigation_enabled": True
            }),
            'fieldToggles': json.dumps({"withAuxiliaryUserLabels": False}),
        }

        try:
            response = requests.get(API_URL, params=params, headers=headers)
            response.raise_for_status()
            with open("twix/response.json", "w") as f:
                f.write(json.dumps(response.json(), indent=4))
            user_data = response.json().get("data", {}).get("user", {}).get("result")
            if not user_data:
                raise UserDataExtractionError(f"Failed to extract user data for {username} from the response")
            return user_data
        except RequestException as e:
            raise UserDataExtractionError(f"Failed to retrieve user data for {username}: {str(e)}") from e

class XScraper:
    def __init__(self):
        self.tok = TokenRetriever.get_tok()
        self.guest_id = GuestIDRetriever.get_guest_id(self.tok)
        self.user_data_extractor = UserDataExtractor(self.guest_id)

    def get_user_info(self, username):
        user_data = self.user_data_extractor.extract_user_data(username)
        return self._parse_user_data(user_data)

    @staticmethod
    def _parse_user_data(user_data):
        legacy_data = user_data.get('legacy', {})
        return {
            "id": user_data.get('rest_id'),
            "name": legacy_data.get('name'),
            "screen_name": legacy_data.get('screen_name'),
            "description": legacy_data.get('description'),
            "followers_count": legacy_data.get('followers_count'),
            "friends_count": legacy_data.get('friends_count'),
            "posts_count": legacy_data.get('statuses_count'),
            "favourites_count": legacy_data.get('favourites_count'),
            "listed_count": legacy_data.get('listed_count'),
            "media_count": legacy_data.get('media_count'),
            "location": legacy_data.get('location'),
            "external_custom_url": legacy_data.get('display_url'),
            "created_at": datetime.strptime(
                legacy_data.get('created_at'), 
                "%a %b %d %H:%M:%S %z %Y"
            ).isoformat(),
            "profile_image_url": legacy_data.get('profile_image_url_https'),
            "profile_banner_url": legacy_data.get('profile_banner_url'),
            "is_blue_verified": user_data.get('is_blue_verified'),
            "birthdate": user_data.get('legacy_extended_profile', {}).get('birthdate'),
            "is_identity_verified": user_data.get('verification_info', {}).get('is_identity_verified', None), # Not sure what this EXACTLY means yet
            "highlighted_tweet_count": user_data.get('highlights_info', {}).get('highlighted_tweets'),
            "subscriptions_count": user_data.get('creator_subscriptions_count')
        }