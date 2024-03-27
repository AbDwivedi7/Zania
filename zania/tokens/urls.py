from django.urls import path

from zania.tokens.views import (
    LoginView,
)

urlpatterns = [
    path('login', LoginView.as_view(), name="User Login"),
]
