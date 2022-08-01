from mqttasgi.consumers import MqttConsumer


class ChatMqttConsumer(MqttConsumer):
    async def connect(self):
        await self.subscribe("tele/+/SENSOR", 1)
        await self.channel_layer.group_add("chat2mqtt", self.channel_name)

    async def receive(self, mqtt_message):
        topic = mqtt_message["topic"]
        payload = mqtt_message["payload"].decode()
        await self.channel_layer.group_send(
            "mqtt2chat",
            {
                "type": "mqtt.message",
                "message": f"{topic=}: {payload=}",
            },
        )

    async def disconnect(self):
        await self.unsubscribe("tele/+/SENSOR")
        await self.channel_layer.group_discard("chat2mqtt", self.channel_name)

    async def chat_message(self, event):
        await self.publish("asgi", event["message"], qos=1, retain=False)
