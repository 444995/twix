import json
import re
import requests
from requests.exceptions import RequestException
from datetime import datetime
from .exceptions import TokenRetrievalError, GuestIDRetrievalError, UserDataExtractionError, UserTweetsExtractionError

BASE_URL = 'https://x.com/'
GUEST_ID_URL = 'https://twitter.com/x/migrate'
API_URL = 'https://api.x.com/graphql/Yka-W8dz7RaEuQNkroPkYw/UserByScreenName'
TWEETS_API_URL = 'https://api.x.com/graphql/E3opETHurmVJflFsUBVuUQ/UserTweets'
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
    FEATURES_PARAMS = json.dumps({
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
    })
    FIELDTOGGLES_PARAMS = json.dumps({
        "withAuxiliaryUserLabels": False}
    )

    def __init__(self, guest_id):
        self.guest_id = guest_id

    def _get_user_id(self, user_data):
        return user_data.get('rest_id')

    def extract_user_data(self, screen_name):
        headers = {
            'Authorization': f'Bearer {AUTH_TOKEN}',
            'Content-Type': 'application/json',
            'X-Guest-Token': self.guest_id,
        }

        params = {
            'variables': json.dumps({
                "screen_name": screen_name, 
                "withSafetyModeUserFields": True
            }),
            'features': self.FEATURES_PARAMS,
            'fieldToggles': self.FIELDTOGGLES_PARAMS,
        }

        try:
            response = requests.get(API_URL, params=params, headers=headers)
            response.raise_for_status()
            user_data = response.json().get("data", {}).get("user", {}).get("result")
            if not user_data:
                raise UserDataExtractionError(f"Failed to extract user data for {screen_name} from the response")

            user_id = self._get_user_id(user_data)
            return user_data, user_id
        except RequestException as e:
            raise UserDataExtractionError(f"Failed to retrieve user data for {screen_name}: {str(e)}") from e


import json
import requests
from requests.exceptions import RequestException

class UserTweetsExtractor:
    """
    It should be said that *for now* this is only tweets that can be seen without an X account.
    """
    FEATURES_PARAMS = json.dumps({
                "rweb_tipjar_consumption_enabled": True,
                "responsive_web_graphql_exclude_directive_enabled": True,
                "verified_phone_label_enabled": False,
                "creator_subscriptions_tweet_preview_api_enabled": True,
                "responsive_web_graphql_timeline_navigation_enabled": True,
                "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                "communities_web_enable_tweet_community_results_fetch": True,
                "c9s_tweet_anatomy_moderator_badge_enabled": True,
                "articles_preview_enabled": True,
                "responsive_web_edit_tweet_api_enabled": True,
                "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                "view_counts_everywhere_api_enabled": True,
                "longform_notetweets_consumption_enabled": True,
                "responsive_web_twitter_article_tweet_consumption_enabled": True,
                "tweet_awards_web_tipping_enabled": False,
                "creator_subscriptions_quote_tweet_preview_enabled": False,
                "freedom_of_speech_not_reach_fetch_enabled": True,
                "standardized_nudges_misinfo": True,
                "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                "rweb_video_timestamps_enabled": True,
                "longform_notetweets_rich_text_read_enabled": True,
                "longform_notetweets_inline_media_enabled": True,
                "responsive_web_enhance_cards_enabled": False
    })
    FIELDTOGGLES_PARAMS = json.dumps({
        "withArticlePlainText": False}
    )

    def __init__(self, guest_id):
        self.guest_id = guest_id

    def extract_public_tweets(self, user_id):
        json_data = self._fetch_tweets_data(user_id)
        return self._parse_tweets(json_data)

    def _fetch_tweets_data(self, user_id):
        headers = {
            'Authorization': f'Bearer {AUTH_TOKEN}',
            'Content-Type': 'application/json',
            'X-Guest-Token': self.guest_id,
        }

        params = {
            'variables': json.dumps({
                "userId": user_id,
                "count": 20,
                "includePromotedContent": True,
                "withQuickPromoteEligibilityTweetFields": True,
                "withVoice": True,
                "withV2Timeline": True
            }),
            'features': self.FEATURES_PARAMS,
            'fieldToggles': self.FIELDTOGGLES_PARAMS,
        }

        try:
            response = requests.get(TWEETS_API_URL, params=params, headers=headers)
            response.raise_for_status()
            json_data = response.json()
            if not json_data:
                raise UserTweetsExtractionError(f"Failed to extract user tweets for user ID {user_id}")
            return json_data
        except RequestException as e:
            raise UserTweetsExtractionError(f"Failed to retrieve user tweets for user ID {user_id}: {str(e)}") from e

    def _parse_tweets(self, json_data):
        entries = self._find_entries(json_data)
        if not entries:
            raise UserTweetsExtractionError("Failed to find 'entries' in the JSON data")
        return [self._extract_tweet_info(entry) for entry in entries if self._is_valid_tweet_entry(entry)]

    def _find_entries(self, data):
        if isinstance(data, dict):
            for key, value in data.items():
                if key == "entries" and isinstance(value, list):
                    return value
                result = self._find_entries(value)
                if result:
                    return result
        elif isinstance(data, list):
            for item in data:
                result = self._find_entries(item)
                if result:
                    return result
        return []

    def _is_valid_tweet_entry(self, entry):
        return ('content' in entry and 
                'itemContent' in entry['content'] and 
                'tweet_results' in entry['content']['itemContent'] and
                'result' in entry['content']['itemContent']['tweet_results'])

    def _extract_tweet_info(self, entry):
        tweet_data = entry['content']['itemContent']['tweet_results']['result']
        legacy_data = tweet_data.get('legacy', {})
        
        return {
            'id': tweet_data.get('rest_id'),
            'text': legacy_data.get('full_text'),
            'created_at': legacy_data.get('created_at'),
            'lang': legacy_data.get('lang'),
            'favorite_count': legacy_data.get('favorite_count'),
            'favorited': legacy_data.get('favorited'),
            'quote_count': legacy_data.get('quote_count'),
            'quoted_status_id_str': legacy_data.get('quoted_status_id_str'),
            'quoted_status_permalink': legacy_data.get('quoted_status_permalink'),
            'reply_count': legacy_data.get('reply_count'),
            'retweet_count': legacy_data.get('retweet_count'),
            'retweeted': legacy_data.get('retweeted'),
            'conversation_id_str': legacy_data.get('conversation_id_str'),
            'display_text_range': legacy_data.get('display_text_range'),
            'entities': legacy_data.get('entities'),
            'extended_entities': legacy_data.get('extended_entities'),
            'is_quote_status': legacy_data.get('is_quote_status'),
            'possibly_sensitive': legacy_data.get('possibly_sensitive'),
            'possibly_sensitive_editable': legacy_data.get('possibly_sensitive_editable'),
            'source': legacy_data.get('source'),
            'views': tweet_data.get('views', {}).get('count'),
            'edit_control': tweet_data.get('edit_control'),
            'is_translatable': tweet_data.get('is_translatable'),
            'bookmark_count': legacy_data.get('bookmark_count'),
            'bookmarked': legacy_data.get('bookmarked'),
            'unmention_data': tweet_data.get('unmention_data'),
            'note_tweet': tweet_data.get('note_tweet'),
            'quick_promote_eligibility': tweet_data.get('quick_promote_eligibility')
        }

class XScraper:
    def __init__(self):
        self.tok = TokenRetriever.get_tok()
        self.guest_id = GuestIDRetriever.get_guest_id(self.tok)
        self.user_data_extractor = UserDataExtractor(self.guest_id)
        self.user_tweets_extractor = UserTweetsExtractor(self.guest_id)

    def get_user_info(self, screen_name):
        user_data, user_id = self.user_data_extractor.extract_user_data(screen_name)
        tweets = self.user_tweets_extractor.extract_public_tweets(user_id)
        
        return self._parse_user_data(
            user_data, 
            user_id, 
            tweets
        )

    @staticmethod
    def _parse_user_data(user_data, user_id, tweets):
        legacy_data = user_data.get('legacy', {})
        return {
            "user_id": user_id,
            "name": legacy_data.get('name'),
            "screen_name": legacy_data.get('screen_name'),
            "tweets": tweets,
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
            "is_identity_verified": user_data.get('verification_info', {}).get('is_identity_verified', None),
            "highlighted_tweets_count": user_data.get('highlights_info', {}).get('highlighted_tweets'),
            "subscriptions_count": user_data.get('creator_subscriptions_count'),
        }