import asyncio
import json
import websockets
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
        self.websocket = None
        self.connected_users = set()
        self.logger = logging.getLogger(__name__)

        """Generate a JWT and store it and its expiration time."""

    def authenticate(self):
        jwt_secret = config("CHAT_JWT_SECRET")
        jwt_issuer = config("CHAT_JWT_ISSUER")
        jwt_audience = config("CHAT_JWT_AUDIENCE")

        payload = {
            "sub": "user101",  # subject of the token (usually user id)
            "name": "John Doe",  # additional data
            "iat": int(time.time()),  # issued at
            "iss": jwt_issuer,  # issuer
            "aud": jwt_audience,  # audience
        }

        self.token = jwt.encode(payload, jwt_secret, algorithm="HS256")
        print(self.token)
        # Set the token to expire in 23 hour
        self.token_expiration = datetime.now() + timedelta(hours=23)

    async def connect_to_chat(self, user_id):
        while True:
            try:
                self.websocket = await websockets.connect(
                    f"{self.ws_url}?userId={user_id}",
                    extra_headers={"Authorization": f"Bearer {self.token}"},
                )
                break
            except (websockets.exceptions.ConnectionClosed, OSError) as e:
                print("Connection failed. Retrying...")
                self.logger.error(f"Failed to connect to chat: {e}")
                await asyncio.sleep(5)  # Wait for 5 seconds before retrying

    def check_server_health(self):
        """Check the health of the chat app server."""
        # self.refresh_token()
        try:
            response = requests.get(
                f"{self.api_url}/health",
                headers={"Authorization": f"Bearer {self.token}"},
            )
            response.raise_for_status()
            print(response.json())
            return response.status_code == 200
        except requests.RequestException as e:
            self.logger.error(f"Failed to check server health: {e}")
            return False

    async def send_test_message(self, message="This is a test message"):
        if self.websocket:
            ws = self.websocket
            # await self.websocket.send(message)
            test_message = {
                "senderId": "pythonClient",
                "receiverId": "chat001",
                "content": "This is a test message from Python client",
            }
            await ws.send(json.dumps(test_message))
            ws.close()

    async def disconnect_from_chat(self):
        if self.websocket:
            await self.websocket.close()
            self.websocket = None

    async def send_message(self, message):
        self.refresh_token()
        if self.websocket:
            await self.websocket.send(message)

    async def receive_message(self):
        self.refresh_token()
        if self.websocket:
            return await self.websocket.recv()

    def get_connected_users(self):
        self.refresh_token()
        response = requests.get(
            f"{self.api_url}/users", headers={"Authorization": f"Bearer {self.token}"}
        )
        self.connected_users = set(response.json())
        return self.connected_users

    def get_connected_clients(self):
        """Get the list of connected clients."""
        self.refresh_token()
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

    async def handle_chat(self):
        await self.connect_to_chat()
        while True:
            message = await self.receive_message()
            print(message)
