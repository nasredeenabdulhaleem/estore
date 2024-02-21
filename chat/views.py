import time
from django.dispatch import receiver
from django.http import JsonResponse
import json
from django.core.serializers import serialize
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import View
from accounts.views import business_name_exists
from chat.chat_connection import ChatService
from chat.models import ChatUser
from accounts.models import User

from shop.globalcontext import user_context_processor
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from decouple import config

from shop.models import VendorProfile

# Initialize the ChatService with the API and WebSocket URLs
api_url = config("CHAT_API_URL")
ws_url = config("CHAT_WS_URL")
chat_service = ChatService(api_url, ws_url)

# Authenticate the chat service
chat_service.authenticate()
chat_service.check_server_health()
chat_service.connect_to_chat(user_id="nasredeen")
# chat_service.send_test_message()
chat_service.receive_message()
# Create your views here.


def is_user(user):
    return user.is_authenticated and user.role == "User"


def create_chat_user(user):
    try:
        if user.role == "User":
            new_user_user = chat_service.create_new_user(
                f"{user.username}{user.id}", user.username, role="user"
            )
            print("new user", new_user_user)
        else:
            new_user_user = chat_service.create_new_user(
                f"{user.vendor.business_name}{user.vendor.id}",
                user.vendor.business_name,
                role="vendor",
            )
            print("new user", new_user_user)
        # {'chat_id': 'test001', 'username': 'tester', 'role': 'admin', '_id': '65d3b7e2e62e19a96cc10566', 'createdAt': '2024-02-19T20:19:46.092Z', '__v': 0}
        chat_user = ChatUser.objects.create(
            user=user, chat_id=new_user_user["chat_id"], role=new_user_user["role"]
        )
        chat_user.save()
        return chat_user
    except Exception as e:
        return False


def check_and_create_chat_users(user, vendor):
    # Check if user and vendor chat users exist
    user_chat_user = ChatUser.objects.filter(user=user).first()
    vendor_chat_user = ChatUser.objects.filter(user=vendor).first()

    # If user chat user does not exist, try to create it
    if not user_chat_user:
        user_chat_user = create_chat_user(user)
        if not user_chat_user:
            return False

    # If vendor chat user does not exist, try to create it
    if not vendor_chat_user:
        vendor_chat_user = create_chat_user(vendor)
        if not vendor_chat_user:
            return False

    # If we reach this point, both chat users exist or were successfully created
    return True


class UserChatListView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = "chat/user-chatlist.html"

    def test_func(self):
        return is_user(self.request.user)

    def get(self, request, *args, **kwargs):
        user = request.user
        chat = ChatUser.objects.filter(user=user).first()
        if chat:
            chat_id = chat.chat_id
            chats = chat_service.get_all_user_chat(chat_id)
            print(chats)
            return render(
                request,
                self.template_name,
                context={
                    "data": user_context_processor(self.request),
                    "chat_id": chat_id,
                    "chats": chats,
                },
            )
        else:
            return render(
                request,
                self.template_name,
                context={"data": user_context_processor(self.request), "chats": False},
            )


class UserChatView(View):
    template_name = "chat/user-chat.html"

    def get(self, request, *args, **kwargs):
        user = request.user

        if not business_name_exists(self.kwargs["vendor"]):
            messages.error(request, "Vendor does not exist")
            return redirect("store:dashboard")
        vendor_profile = VendorProfile.objects.filter(
            business_name=self.kwargs["vendor"]
        ).first()
        vendor = User.objects.get(
            id=vendor_profile.user.id
        )  # VendorProfile.objects.filter(business_name = self.kwargs['vendor']).first().user
        if check_and_create_chat_users(user, vendor):
            print("chat users exist")
            sender_id = ChatUser.objects.filter(user=user).first()
            receiver_id = ChatUser.objects.filter(user=vendor).first()
            get_chat = chat_service.get_chat(
                sender_id=sender_id.chat_id, receiver_id=receiver_id.chat_id
            )
            return render(
                request,
                self.template_name,
                context={
                    "data": user_context_processor(self.request),
                    "chats": json.dumps(get_chat),
                    "sender_id": sender_id.chat_id,
                    "receiver_id": receiver_id.chat_id,
                },
            )
        else:
            messages.error(request, "Failed to start chat. Try again later")
            return redirect("store:dashboard")
            # return render(
            #     request,
            #     self.template_name,
            #     context={"data": user_context_processor(self.request)},
            # )


class VendorChatListView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = "chat/vendor-chatlist.html"

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == "Vendor"

    def get(self, request, *args, **kwargs):
        user = request.user
        chat = ChatUser.objects.filter(user=user).first()
        business_name = user.vendor.business_name
        if chat:
            chat_id = chat.chat_id
            chats = chat_service.get_all_user_chat(chat_id)
            print(chats)
            return render(
                request,
                self.template_name,
                context={
                    "data": user_context_processor(self.request),
                    "chat_id": chat_id,
                    "chats": chats,
                    "business_name": business_name,
                },
            )
        else:
            return render(
                request,
                self.template_name,
                context={"data": user_context_processor(self.request),"business_name":business_name, "chats": False},
            )

class VendorChatView(View):
    template_name= "chat/vendor-chat.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        business_name = self.kwargs['business_name']
        print(business_name)
        receiver_id = self.kwargs['user_id']

        # if not business_name_exists(self.kwargs["vendor"]):
        #     messages.error(request, "Vendor does not exist")
        #     return redirect("store:dashboard")
        # vendor_profile = VendorProfile.objects.filter(
        #     business_name=self.kwargs["vendor"]
        # ).first()
        # vendor = User.objects.get(
        #     id=vendor_profile.user.id
        # )  # VendorProfile.objects.filter(business_name = self.kwargs['vendor']).first().user
        # if check_and_create_chat_users(user, vendor):
        print("chat users exist")
        sender_id = ChatUser.objects.filter(user=user).first()
        # receiver_id = ChatUser.objects.filter(ch=vendor).first()
        get_chat = chat_service.get_chat(
            sender_id=sender_id.chat_id, receiver_id=receiver_id
        )
        return render(
            request,
            self.template_name,
            context={
                "data": user_context_processor(self.request),
                "chats": json.dumps(get_chat),
                "sender_id": sender_id.chat_id,
                "receiver_id": receiver_id,
                "business_name": business_name,
            },
        )
        # else:
        #     messages.error(request, "Failed to start chat. Try again later")
        #     return redirect("store:dashboard")
            # return render(
            #     request,
            #     self.template_name,
            #     context={"data": user_context_processor(self.request)},
            # )



def send_chat_message(request, *args, **kwargs):
    if request.method == "POST":
        body = json.loads(request.body)
        print(body)
        message = body["content"]
        sender_id = body["sender"]
        receiver_id = body["receiver"]
        print("sender_id", sender_id)
        print("receiver_id", receiver_id)
        print("message", message)
        user = request.user
        chat_message = chat_service.send_message(
            sender_id=sender_id, receiver_id=receiver_id, message=message
        )
        return JsonResponse({"message": "Message sent successfully"}, status=200)
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)
