# twix

twix is a Python library for scraping user data from X (formerly Twitter) profiles. It provides an easy-to-use API with a simple `XUser` class, handles authentication and request management automatically, and retrieves comprehensive user information.

## Installation

To install twix, follow these steps:

```bash
git clone https://github.com/444995/twix.git
cd twix
pip install .
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

# Get all user data as a dictionary
user_data = user.to_dict()
```

## Disclaimer

- This library is for educational purposes only. Ensure you comply with X's terms of service when using this library.
- Rate limiting is not implemented in this version. Be cautious with request frequency to avoid IP blocks.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.