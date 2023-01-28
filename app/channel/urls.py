"""
URL mappings for the channel app.
"""

from channel import views
from django.urls import (
    path,
    include
)
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('channels', views.ChannelViewSet)

app_name = 'channel'
urlpatterns = [
    path('', include(router.urls)),
    path('messages/<int:message_id>', views.MessageSerializer)
]
