from django.shortcuts import render
from django.views.generic import View
from chat.chat_connection import ChatService

from shop.globalcontext import user_context_processor
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from decouple import config
import asyncio

# Initialize the ChatService with the API and WebSocket URLs
api_url = config("CHAT_API_URL")
ws_url = config("CHAT_WS_URL")
chat_service = ChatService(api_url, ws_url)

# Authenticate the chat service
# chat_service.authenticate()
chat_service.check_server_health()
# asyncio.run(chat_service.connect_to_chat(user_id="user01"))
# asyncio.run(chat_service.send_test_message())
# Create your views here.


def is_user(user):
    return user.is_authenticated and user.role == "User"


class UserChatListView(View):
    template_name = "chat/user-chatlist.html"

    # def test_func(self):
    #     return is_user(self.request.user)

    def get(self, request, *args, **kwargs):
        user = request.user
        return render(
            request,
            self.template_name,
            context={"data": user_context_processor(self.request)},
        )


class UserChatView(View):
    template_name = "chat/user-chat.html"

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
            context={"data": user_context_processor(self.request)},
        )


class VendorChatListView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = "chat/vendor-chatlist.html"

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == "Vendor"

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
            context={"data": user_context_processor(self.request)},
        )


# create a method for this route in my third party chat service Route: /chat
# Method: GET
# Handler: getConnectedClients()
# No parameters or body required
