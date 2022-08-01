import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.channel_layer.group_add("mqtt2chat", self.channel_name)
        await self.channel_layer.group_add("matrix2chat", self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await self.channel_layer.group_discard("mqtt2chat", self.channel_name)
        await self.channel_layer.group_discard("matrix2chat", self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )
        await self.channel_layer.group_send(
            "chat2mqtt", {"type": "chat.message", "message": message}
        )
        await self.channel_layer.group_send(
            "chat2matrix", {"type": "chat.message", "message": message}
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({"message": event["message"]}))

    async def mqtt_message(self, event):
        await self.send(text_data=json.dumps({"message": f"MQTT: {event['message']}"}))

    async def matrix_message(self, event):
        await self.send(
            text_data=json.dumps({"message": f"Matrix: {event['message']}"})
        )
