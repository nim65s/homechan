from django.db import models

from channels.layers import get_channel_layer


class Device(models.Model):
    end_mac = models.CharField(max_length=6, unique=True)
    nick = models.CharField(max_length=20, unique=True)
    friendly_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        """Get nick."""
        return self.nick

    async def get_power(self):
        """Retrieve power status over MQTT."""
        layer = get_channel_layer()
        await layer.group_send(
            "app2mqtt",
            {
                "type": "app.message",
                "topic": f"cmnd/tasmota_{self.end_mac}/Power",
                "payload": "",
            },
        )

    async def set_power(self, power):
        """Send power order over MQTT."""
        layer = get_channel_layer()
        if power in ("on", "off"):
            await layer.group_send(
                "app2mqtt",
                {
                    "type": "app.message",
                    "topic": f"cmnd/tasmota_{self.end_mac}/Power",
                    "payload": power.upper(),
                },
            )
        else:
            await layer.group_send(
                "app2matrix",
                {"type": "app.message", "message": "Error: power must be ON or OFF"},
            )
