import sys
import os
import streamlit as st
import json
import secrets
import hashlib
from datetime import datetime
import time
import matplotlib.pyplot as plt
import plotly.express as px

# Ensure the current directory is included in the module path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Import modules
from models.blockchain import BlockchainSystem
from models.user import User
from utils.validation import validate_email, validate_phone, validate_password, validate_aaa_card
from utils.encryption import generate_salt, hash_password_with_salt

# Ensure the `data` directory exists
if not os.path.exists('data'):
    os.makedirs('data')

class UserManager:
    def __init__(self, blockchain):
        self.users = {}
        self.token_to_user = {}
        self.blockchain = blockchain
        self.load_users()

    def save_users(self):
        users_data = {email: user.to_dict() for email, user in self.users.items()}
        with open('data/users.json', 'w') as f:
            json.dump(users_data, f, indent=4)

        with open('data/tokens.json', 'w') as f:
            json.dump(self.token_to_user, f, indent=4)

    def load_users(self):
        try:
            with open('data/users.json', 'r') as f:
                users_data = json.load(f)
                self.users = {}
                for email, data in users_data.items():
                    user = User(**data)
                    self.users[email] = user

            with open('data/tokens.json', 'r') as f:
                self.token_to_user = json.load(f)
        except FileNotFoundError:
            pass

    def register_user(self, name, email, phone, username, password, aaa_card):
        validate_email(email)
        validate_phone(phone)
        validate_password(password)
        validate_aaa_card(aaa_card)

        if email in self.users:
            raise ValueError("Email already registered")

        salt = generate_salt()
        password_hash = hash_password_with_salt(password, salt)
        token_id = secrets.token_urlsafe(16)
        secret_key = secrets.token_hex(8)

        user = User(
            name=name,
            email=email,
            phone=phone,
            username=username,
            password_hash=f"{salt}:{password_hash}",
            aaa_card=aaa_card,
            token_id=token_id,
            secret_key=secret_key,
            accounts=[username],
            profile_data={"created_at": str(datetime.now())},
            posts=[],
            videos=[],
            stories=[]
        )

        self.users[email] = user
        self.token_to_user[token_id] = email
        self.save_users()
        return user

    def login(self, token_id):
        if token_id not in self.token_to_user:
            raise ValueError("Invalid token ID")
        email = self.token_to_user[token_id]
        return self.users[email]

# Custom CSS for styling

def apply_custom_style():
    st.markdown("""
        <style>
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f0f2f5;
            color: #333;
        }
        .main {
            padding: 2rem;
        }
        .stTitle {
            color: #1E88E5;
            font-size: 2.5rem !important;
            font-weight: 700 !important;
            margin-bottom: 2rem !important;
            text-align: center;
        }
        .css-1d391kg {
            background-color: #f8f9fa;
            padding: 2rem 1rem;
        }
        .nav-button {
            background-color: transparent;
            border: none;
            color: #1E88E5;
            padding: 0.5rem 1rem;
            width: 100%;
            text-align: left;
            cursor: pointer;
            margin: 0.25rem 0;
            border-radius: 5px;
            transition: all 0.3s ease;
            font-size: 1rem;
        }
        .nav-button:hover {
            background-color: #e3f2fd;
        }
        .nav-button.active {
            background-color: #1E88E5;
            color: white;
        }
        .stTextInput > div > div > input {
            background-color: #fff;
            border: 1px solid #e0e0e0;
            border-radius: 5px;
            padding: 0.5rem;
        }
        .stButton > button {
            background-color: #1E88E5;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.5rem 2rem;
            font-weight: 600;
            width: 100%;
        }
        .stButton > button:hover {
            background-color: #1976D2;
        }
        .post-card {
            background-color: white;
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .profile-info {
            background-color: white;
            border-radius: 10px;
            padding: 2rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)

def create_static_navigation():
    menu_options = [
        ("🏠 Home", "Home"),
        ("🔑 Login", "Login"),
        ("📝 Register", "Register"),
        ("👤 Profile", "Profile"),
        ("⬆️ Upload Content", "Upload Content"),
        ("🔍 Explore", "Explore"),
        ("🚪 Logout", "Logout")
    ]

    for display_name, menu_name in menu_options:
        is_active = st.session_state.get('current_page') == menu_name
        if st.sidebar.button(display_name, key=f"nav_{menu_name}"):
            st.session_state.current_page = menu_name
            st.rerun()

def main():
    apply_custom_style()

    if 'blockchain' not in st.session_state:
        st.session_state.blockchain = BlockchainSystem()
        st.session_state.user_manager = UserManager(st.session_state.blockchain)

    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"

    st.sidebar.title("Navigation")
    create_static_navigation()

    menu = st.session_state.current_page

    if menu == "Home":
        st.title("SECURE SPHERE")
        st.write("Empowering social connections with blockchain security...")
        if menu == "Home":
            st.markdown("""
        <script>
        document.body.setAttribute('data-page', 'Home');
        </script>
    """, unsafe_allow_html=True)
        else:
            st.markdown("""
        <script>
        document.body.removeAttribute('data-page');
        </script>
    """, unsafe_allow_html=True)


    elif menu == "Login":
        st.title("🔑 Login")
        st.write("Enter your login details.")
        token_id = st.text_input("Enter Token ID")
  # Apply custom CSS for compact and stylish textbox with animation
        st.markdown("""
    <style>
    .stTextInput > div > div > input {
        background-color: #FFFFFF !important;
        color: #000000 !important; /* Dark Blue Text Color */
        border-radius: 10px !important;
        padding: 6px 10px !important;
        font-size: 16px !important;
    }

    .stTextInput > div > div > input:focus {
        box-shadow: 0 0 10px #1E88E5 !important;
    }
    </style>
""", unsafe_allow_html=True)
        if st.button("Login"):
            try:
                start_time = time.time()
                user = st.session_state.user_manager.login(token_id)
                st.session_state.user = user
                st.session_state.logged_in = True
                st.session_state.performance_metrics["login_times"].append(time.time() - start_time)
                st.success(f"Welcome back, {user.name}!")
                st.session_state.refresh = True  # Refresh the page
            except ValueError as e:
                st.error(str(e))

    elif menu == "Register":
        st.title("📝 Register")
        st.write("Create a new account.")
        with st.form("register_form"):
            name = st.text_input("Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password",)
            aaa_card = st.text_input("AAA Card Number")
            st.markdown("""
    <style>
    .stTextInput > div > div > input {
        background-color: #FFFFFF !important;
        color: #000000 !important; /* Dark Blue Text Color */
    }
    </style>
""", unsafe_allow_html=True)

            if st.form_submit_button("Register"):
                try:
                    start_time = time.time()
                    user = st.session_state.user_manager.register_user(
                        name, email, phone, username, password, aaa_card
                    )
                    st.session_state.performance_metrics["registration_times"].append(time.time() - start_time)
                    st.success(f"Registration successful! Your Token ID: {user.token_id}")
                    st.info(f"Your Secret Key: {user.secret_key}")
                except ValueError as e:
                    st.error(str(e))
    elif menu == "Profile":
        st.title("👤 Profile")
        st.write("View your profile details.")

        if 'user' in st.session_state and st.session_state.user:
            user = st.session_state.user
            st.write(f"Name: {user.name}")
            st.write(f"Email: {user.email}")
            st.write(f"Phone: {user.phone}")
            st.write(f"Username: {user.username}")
            st.write(f"AAA Card: {user.aaa_card}")
        else:
            st.warning("Please log in to view your profile.")

 # After Login: Uploading Options
    if st.session_state.get("logged_in"):
        if menu == "Upload Content":
            st.title("Upload Content")
            st.write("Here you can upload posts, videos, and stories.")

        # Upload Post
            st.subheader("Upload a Post")
            post_content = st.text_area("Write your post here")
        if st.button("Submit Post"):
            st.session_state.user.add_post(post_content)
            st.session_state.user_manager.save_users()
            st.success("Post uploaded successfully!")

        # Upload Video
        st.subheader("Upload a Video")
        video_url = st.text_input("Enter video URL")
        if st.button("Submit Video"):
            st.session_state.user.add_video(video_url)
            st.session_state.user_manager.save_users()
            st.success("Video uploaded successfully!")

        # Upload Story
        st.subheader("Upload a Story")
        story_content = st.text_area("Write your story here")
        if st.button("Submit Story"):
            st.session_state.user.add_story(story_content)
            st.session_state.user_manager.save_users()
            st.success("Story uploaded successfully!")
if 'performance_metrics' not in st.session_state:
    st.session_state.performance_metrics = {
        "login_times": [],
        "registration_times": []
    }

# Apply custom CSS for compact and stylish textbox with animation
st.markdown("""
    <style>
    .stTextInput > div > div > input {
        background-color: #d1f0d1 !important;
        color: #00008B !important; /* Dark Blue Text Color */
        border-radius: 8px !important;
        padding: 6px 10px !important;
        font-size: 16px !important;
    }

    .stTextInput > div > div > input:focus {
        box-shadow: 0 0 10px #1E88E5 !important;
        transform: scale(1.05) !important;
    }
                             /* Compact and stylish navigation buttons */
    .stButton > button {
        background-color: #6A1B9A !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        padding: 6px 10px !important;
        font-size: 14px !important;
        margin: 4px 0 !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button:hover {
        background-color: #4A148C !important;
        transform: scale(1.05) !important;
    }

    .stButton > button:active {
        transform: scale(0.98) !important;
    }
    .sidebar .block-container {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        height: 100% !important;
        width: 200px !important;
        background-color: #6A1B9A !important;
        color: #FFFFFF !important;
        z-index: 1000 !important;
        text-align: left !important;
    }

    </style>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
