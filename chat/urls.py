from django.urls import include, path
from chat.views import (
    UserChatListView,
    UserChatView,
    VendorChatListView,
    VendorChatView,
    send_chat_message,
)

urlpatterns = [
    path("chat/send-message/", send_chat_message, name="send-message"),
    path(
        "chat/",
        UserChatListView.as_view(),
        name="user-chat-list",
    ),
    path(
        "user-chat/<str:vendor>/",
        UserChatView.as_view(),
        name="user-chat",
    ),
    path(
        "<bussiness_name>/vendor-conversations/",
        VendorChatListView.as_view(),
        name="vendor-chat-list",
    ),
    path(
        "<business_name>/chat/<str:user_id>/",
        VendorChatView.as_view(),
        name="vendor-user-chat",
    ),
]
