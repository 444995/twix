from .xscraper import XScraper

class XUser:
    def __init__(self, username):
        self.user_data = XScraper.scrape_user_data()
    
    @property
    def follower_count(self):
        return self.user_data["follower_count"]