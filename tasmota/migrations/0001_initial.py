# Generated by Django 4.1 on 2022-09-04 20:06

from django.db import migrations, models


def devices(apps, schema_editor):
    Device = apps.get_model("tasmota", "Device")
    Device.objects.create(
        end_mac="3E19A4", nick="frigo", friendly_name="Tasmota POW Frigo"
    )
    Device.objects.create(
        end_mac="3E2C43", nick="terrasse", friendly_name="Tasmota POW Terrasse"
    )
    Device.objects.create(
        end_mac="3E242C", nick="congel", friendly_name="Tasmota POW Congel"
    )
    Device.objects.create(
        end_mac="43D8FD", nick="chambre", friendly_name="Tasmota Sonoff TH Chambre"
    )


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Device",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("end_mac", models.CharField(max_length=6, unique=True)),
                ("nick", models.CharField(max_length=20, unique=True)),
                ("friendly_name", models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.RunPython(devices),
    ]
