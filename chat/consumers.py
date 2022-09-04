import json

from channels.generic.websocket import AsyncWebsocketConsumer
from mqttasgi.consumers import MqttConsumer
from matrix_asgi.consumers import MatrixConsumer

from tasmota.models import Device


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

    async def app_message(self, event):
        await self.send(text_data=json.dumps({"message": f"MQTT: {event['message']}"}))


class ChatMqttConsumer(MqttConsumer):
    async def connect(self):
        await self.subscribe("tele/+/SENSOR", 1)
        await self.subscribe("stat/+/RESULT", 1)
        await self.channel_layer.group_add("chat2mqtt", self.channel_name)
        await self.channel_layer.group_add("app2mqtt", self.channel_name)

    async def receive(self, mqtt_message):
        topic = mqtt_message["topic"]
        payload = mqtt_message["payload"].decode()
        if topic.startswith("stat/tasmota_") and topic.endswith("/RESULT"):
            await self.channel_layer.group_send(
                "mqtt2matrix",
                {
                    "type": "mqtt.message",
                    "message": f"{topic=}: {payload=}",
                },
            )
        else:
            await self.channel_layer.group_send(
                "mqtt2chat",
                {
                    "type": "mqtt.message",
                    "message": f"{topic=}: {payload=}",
                },
            )

    async def disconnect(self):
        await self.unsubscribe("tele/+/SENSOR")
        await self.unsubscribe("stat/+/RESULT")
        await self.channel_layer.group_discard("chat2mqtt", self.channel_name)

    async def chat_message(self, event):
        await self.publish("asgi", event["message"], qos=1, retain=False)

    async def app_message(self, event):
        await self.publish(event["topic"], event["payload"], qos=1, retain=False)


class ChatMatrixConsumer(MatrixConsumer):
    startswith = "!"

    async def connect(self):
        await self.channel_layer.group_add("chat2matrix", self.channel_name)
        await self.channel_layer.group_add("app2matrix", self.channel_name)
        await self.channel_layer.group_add("mqtt2matrix", self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("chat2matrix", self.channel_name)

    async def receive(self, matrix_message):
        match matrix_message["body"].strip().lower().split():
            case ("pow", nick):
                device = await Device.objects.aget(nick=nick)
                await device.get_power()
            case ("pow", nick, power):
                device = await Device.objects.aget(nick=nick)
                await device.set_power(power)
            case _:
                await self.channel_layer.group_send(
                    "matrix2chat",
                    {
                        "type": "matrix.message",
                        "message": matrix_message,
                    },
                )

    async def chat_message(self, message):
        await self.matrix_send("!PBcCHCjiPyGbThYAyQ:aen.im", message["message"])

    async def app_message(self, message):
        await self.matrix_send("!PBcCHCjiPyGbThYAyQ:aen.im", message["message"])

    async def mqtt_message(self, message):
        await self.matrix_send("!PBcCHCjiPyGbThYAyQ:aen.im", message["message"])
