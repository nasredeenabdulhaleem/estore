from django.urls import include, path
from chat.views import UserChatListView, UserChatView

urlpatterns = [
    path(
        "",
        UserChatListView.as_view(),
        name="user-chat-list",
    ),
    path(
        "user-chat/",
        UserChatView.as_view(),
        name="user-chat",
    ),
]
