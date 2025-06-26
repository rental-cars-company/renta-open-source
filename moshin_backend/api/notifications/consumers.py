from channels.generic.websocket import AsyncJsonWebsocketConsumer


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if user.is_authenticated:
            self.group_name = f"user_{user.id}"
            await self.channel_layer.group_add(
                self.group_name, self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def notification(self, event):
        await self.send_json(event["data"])
