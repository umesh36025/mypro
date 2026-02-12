from channels.routing import URLRouter
from Messaging.routing import websocket_urlpatterns as messaging_ws
from notifications.routing import websocket_urlpatterns as notification_ws

websocket_urlpatterns = messaging_ws + notification_ws
