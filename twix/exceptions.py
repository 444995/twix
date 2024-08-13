class TokenRetrievalError(Exception):
    """
    Raised when there's an error retrieving the 'tok' value.

    This exception is typically raised when the scraper fails to extract
    the authentication token from the X website response.
    """
    pass

class GuestIDRetrievalError(Exception):
    """
    Raised when there's an error retrieving the 'guest_id' value.

    This exception is typically raised when the scraper fails to obtain
    a guest ID from the X API, which is necessary for making unauthenticated
    requests.
    """
    pass

class UserDataExtractionError(Exception):
    """
    Raised when there's an error extracting user data.

    This exception is typically raised when the scraper fails to extract
    or parse user information from the X API response.
    """
    pass

class UserTweetsExtractionError(Exception):
    """
    Raised when there's an error extracting user tweets.

    This exception is typically raised when the scraper fails to extract
    or parse tweet data from the X API response. This applies to publicly
    visible tweets that can be accessed without an X account.
    """
    pass