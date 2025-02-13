from datetime import datetime

class User:
    def __init__(self, name, email, phone, username, password_hash, aaa_card, token_id, secret_key, accounts, profile_data, posts=None, videos=None, stories=None, messages=None):
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
        self.posts = posts if posts is not None else []
        self.videos = videos if videos is not None else []
        self.stories = stories if stories is not None else []
        self.messages = messages if messages is not None else []

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "username": self.username,
            "password_hash": self.password_hash,
            "aaa_card": self.aaa_card,
            "token_id": self.token_id,
            "secret_key": self.secret_key,
            "accounts": self.accounts,
            "profile_data": self.profile_data,
            "posts": self.posts,
            "videos": self.videos,
            "stories": self.stories,
            "messages": self.messages
        }

    def add_post(self, post_content):
        self.posts.append({"content": post_content, "timestamp": str(datetime.now())})

    def add_video(self, video_url):
        self.videos.append({"url": video_url, "timestamp": str(datetime.now())})

    def add_story(self, story_content):
        self.stories.append({"content": story_content, "timestamp": str(datetime.now())})

    def add_message(self, sender, receiver, message_content):
        self.messages.append({
            "sender": sender,
            "receiver": receiver,
            "content": message_content,
            "timestamp": str(datetime.now())
        })