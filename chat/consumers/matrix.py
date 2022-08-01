from matrix_asgi.consumers import MatrixConsumer


class ChatMatrixConsumer(MatrixConsumer):
    startswith = "!"

    async def connect(self):
        await self.channel_layer.group_add("chat2matrix", self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("chat2matrix", self.channel_name)

    async def receive(self, matrix_message):
        await self.channel_layer.group_send(
            "matrix2chat",
            {
                "type": "matrix.message",
                "message": matrix_message,
            },
        )

    async def chat_message(self, message):
        await self.matrix_send("!PBcCHCjiPyGbThYAyQ:aen.im", message["message"])
