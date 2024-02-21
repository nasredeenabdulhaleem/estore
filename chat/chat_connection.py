import socketio
import json
import requests
import logging
from datetime import datetime, timedelta
import jwt
import time
from decouple import config

# logging.basicConfig(filename='chat-application.log', level=logging.INFO,
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# logger = logging.getLogger(__name__)


class ChatService:
    def __init__(self, api_url, ws_url):
        self.api_url = api_url
        self.ws_url = ws_url
        self.token = None
        self.token_expiration = None
        self.sio = socketio.Client()
        self.connected_users = set()
        self.logger = logging.getLogger(__name__)

        """Generate a JWT and store it and its expiration time."""

    def authenticate(self):
        jwt_secret = config("CHAT_JWT_SECRET")
        jwt_issuer = config("CHAT_JWT_ISSUER")
        jwt_audience = config("CHAT_JWT_AUDIENCE")
        jwt_name = config("CHAT_JWT_Name")

        payload = {
            "sub": "user101",  # subject of the token (usually user id)
            "name": jwt_name,  # additional data
            "role": "admin",
            "iat": int(time.time()),  # issued at
            "iss": jwt_issuer,  # issuer
            "aud": jwt_audience,  # audience
        }

        self.token = jwt.encode(payload, jwt_secret, algorithm="HS256")

        # Set the token to expire in 23 hour
        self.token_expiration = datetime.now() + timedelta(hours=23)

    def connect_to_chat(self, user_id):
        try:
            self.sio.connect(
                f"{self.ws_url}?userId={user_id}",
                headers={"Authorization": f"Bearer {self.token}"},
            )
            self.sio.on("disconnect", self.handle_disconnect)
        except (socketio.exceptions.ConnectionError, OSError) as e:
            print(f"Connection failed. Retrying...{e}")
            self.logger.error(f"Failed to connect to chat: {e}")
            time.sleep(5)

    def handle_disconnect(self):
        print("Disconnected from server. Attempting to reconnect...")
        self.connect_to_chat(user_id="user01")

    def check_server_health(self):
        """Check the health of the chat app server."""
        # self.refresh_token()
        try:
            response = requests.get(
                f"{self.api_url}/health",
                headers={"Authorization": f"Bearer {self.token}"},
            )
            response.raise_for_status()
            return response.status_code == 200
        except requests.RequestException as e:
            self.logger.error(f"Failed to check server health: {e}")
            return False

    def send_test_message(self, message="This is a test message"):
        if self.sio.connected:
            test_message = {
                "senderId": "pythonClient",
                "receiverId": "chat001",
                "content": "This is a test message from Python client",
            }
            self.sio.emit("message", test_message)

    def disconnect_from_chat(self):
        if self.sio.connected:
            self.sio.disconnect()

    # def send_message(self, message):
    #     # self.refresh_token()
    #     if self.sio.connected:
    #         self.sio.emit("message", message)

    def receive_message(self):
        # In Socket.IO, you would typically set up an event handler
        # to handle incoming messages, rather than calling a method
        # to receive a message. This might look something like this:

        @self.sio.on("message")
        def on_message(data):
            print("Received message: ", data)

    def get_connected_users(self):
        # self.refresh_token()
        response = requests.get(
            f"{self.api_url}/users", headers={"Authorization": f"Bearer {self.token}"}
        )
        self.connected_users = set(response.json())
        return self.connected_users

    def get_connected_clients(self):
        """Get the list of connected clients."""
        # self.refresh_token()
        try:
            response = requests.get(
                f"{self.api_url}/chat",
                headers={"Authorization": f"Bearer {self.token}"},
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Failed to get connected clients: {e}")
            raise

    def create_new_user(self, user_id, username, role="user"):
        """Create a new user."""
        try:
            data = {
                "chat_id": user_id,
                "username": username,
                "role": role,
            }
            response = requests.post(
                f"{self.api_url}/users",
                headers={"Authorization": f"Bearer {self.token}"},
                data=data,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Failed to create new user: {e}")
            raise

    def get_all_user_chat(self, chat_id):
        """Get all chat messages for a user."""
        try:
            response = requests.get(
                f"{self.api_url}/chat/{chat_id}",
                headers={"Authorization": f"Bearer {self.token}"},
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Failed to get all user chat: {e}")
            raise

    def get_chat(self, sender_id, receiver_id):
        """Get chat messages between two users."""
        try:
            response = requests.get(
                f"{self.api_url}/chat/{sender_id}/{receiver_id}",
                headers={"Authorization": f"Bearer {self.token}"},
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Failed to get chat: {e}")
            raise

    def send_message(self, sender_id, receiver_id, message):
        if self.sio.connected:
            message = {
                "senderId": sender_id,
                "receiverId": receiver_id,
                "content": message,
            }
            self.sio.emit("message", message)

    async def handle_chat(self):
        await self.connect_to_chat()
        while True:
            message = await self.receive_message()
            print(message)
