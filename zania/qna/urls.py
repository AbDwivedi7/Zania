from django.urls import path

from zania.qna.views import (
    QnaBotAPIView,
)

urlpatterns = [
    path('bot/qna', QnaBotAPIView.as_view(), name="QNA View"),
]
