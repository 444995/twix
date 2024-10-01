# twix

twix is a Python library for scraping user data and tweets from X (formerly Twitter) profiles. It provides an easy-to-use API with a simple `XUser` class, handles authentication and request management automatically, and retrieves comprehensive user information and tweets.

## Installation

To install twix, do this:

```bash
pip install git+https://github.com/444995/twix.git
```

## Usage

```python
from twix import XUser

# Create an XUser instance
user = XUser("username")

# Access user information
print(f"Name: {user.name}")
print(f"Followers: {user.followers_count}")
print(f"Posts: {user.posts_count}")

# Get user tweets
tweets = user.tweets
for tweet in tweets:
    print(f"Tweet ID: {tweet['id']}")
    print(f"Text: {tweet['text']}")
    print(f"Created at: {tweet['created_at']}")
    print(f"Likes: {tweet['favorite_count']}")
    print("---")

# Get all user data as a dictionary
user_data = user.to_dict()
```

## Disclaimer

- This library is for educational purposes only. Ensure you comply with X's terms of service when using this library.
- Rate limiting is not implemented in this version. Be cautious with request frequency to avoid IP blocks.
- It should be noted that, **for now**, this library only retrieves tweets that can be viewed without an X account.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
