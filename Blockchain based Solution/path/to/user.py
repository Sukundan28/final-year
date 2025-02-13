class User:
    def __init__(self, name, email, phone, username, password_hash, aaa_card, token_id, secret_key, accounts, profile_data, posts=None):
        self.name = name
        self.email = email
        self.phone = phone
        self.username = username
        self.password_hash = password_hash
        self.aaa_card = aaa_card
        self.token_id = token_id
        self.secret_key = secret_key
        self.accounts = accounts
        self.profile_data = profile_data
        self.posts = posts if posts is not None else []  # Initialize posts as an empty list if not provided
        # ... other initializations ... 