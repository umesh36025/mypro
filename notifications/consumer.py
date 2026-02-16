import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.http import JsonResponse
from rest_framework import status

class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope["user"]
        self.room_chat_name = f"user_{user.username}"
        if user.is_anonymous:
            await self.close()
        # self.room_chat_name = "user_1122"
        await self.channel_layer.group_add(self.room_chat_name,self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_chat_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        # print(text_data)
        data = json.loads(text_data)
        message = data.get("message")
        # message=text_data
        sender = self.scope["user"]
        print(sender)

        if not message:
            return JsonResponse({"message":"message Not Found"},status=status.HTTP_404_NOT_FOUND)

        # Save message into DB
        # is_saved=await self.save_message(sender.username, message,allowed=allowed)
        # if isinstance(is_saved,JsonResponse):
            # return is_saved

        # Broadcast to group
        await self.channel_layer.group_send(
            self.room_chat_name,
            {
                "type": "send_notification",
                # "sender": sender.username,
                "message": message,
                # "at": get_created_time_format(is_saved.created_at),
            })

    async def send_notification(self, event):

        await self.send(text_data=json.dumps({
            "title": "this is a notification",
            "message": event["message"],
            # "type": event["type"]
        }))
