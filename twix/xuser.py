from .xscraper import XScraper

class XUser:
    def __init__(self, username):
        self._scraper = XScraper()
        self._user_data = self._scraper.get_user_info(username)

    def __str__(self):
        return f"XUser: {self.name} (@{self.screen_name})"

    def __repr__(self):
        return f"XUser(username='{self.screen_name}')"

    def to_dict(self):
        return self._user_data

    @property
    def id(self):
        return self._user_data.get('id')

    @property
    def name(self):
        return self._user_data.get('name')

    @property
    def screen_name(self):
        return self._user_data.get('screen_name')

    @property
    def description(self):
        return self._user_data.get('description')

    @property
    def followers_count(self):
        return self._user_data.get('followers_count')

    @property
    def friends_count(self):
        return self._user_data.get('friends_count')

    @property
    def posts_count(self):
        return self._user_data.get('posts_count')

    @property
    def favourites_count(self):
        return self._user_data.get('favourites_count')

    @property
    def listed_count(self):
        return self._user_data.get('listed_count')

    @property
    def media_count(self):
        return self._user_data.get('media_count')

    @property
    def location(self):
        return self._user_data.get('location')

    @property
    def external_custom_url(self):
        return self._user_data.get('external_custom_url')

    @property
    def created_at(self):
        return self._user_data.get('created_at')

    @property
    def profile_image_url(self):
        return self._user_data.get('profile_image_url')

    @property
    def profile_banner_url(self):
        return self._user_data.get('profile_banner_url')

    @property
    def is_blue_verified(self):
        return self._user_data.get('is_blue_verified')

    @property
    def birthdate(self):
        return self._user_data.get('birthdate')

    @property
    def is_identity_verified(self):
        return self._user_data.get('is_identity_verified')

    @property
    def highlighted_tweet_count(self):
        return self._user_data.get('highlighted_tweet_count')

    @property
    def subscriptions_count(self):
        return self._user_data.get('subscriptions_count')

