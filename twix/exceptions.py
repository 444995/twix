class TokenRetrievalError(Exception):
    """Raised when there's an error retrieving the 'tok' value."""
    pass

class GuestIDRetrievalError(Exception):
    """Raised when there's an error retrieving the 'guest_id' value."""
    pass

class UserDataExtractionError(Exception):
    """Raised when there's an error extracting user data."""
    pass