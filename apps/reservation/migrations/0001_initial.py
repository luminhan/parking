# Generated by Django 4.2.11 on 2024-04-21 09:39

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("parking_place", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Reservation",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("last_updated", models.DateTimeField(auto_now=True, db_index=True)),
                ("reservation_start", models.DateTimeField(db_index=True)),
                ("reservation_end", models.DateTimeField(db_index=True)),
                ("actual_end", models.DateTimeField(db_index=True, null=True)),
                ("confirmed", models.BooleanField(default=False)),
                ("amount", models.FloatField(default=0.0)),
                ("surcharge_amount", models.FloatField(default=0.0)),
                ("actual_amount", models.FloatField(default=0.0)),
                (
                    "parking_place",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reservations",
                        to="parking_place.parkingplace",
                    ),
                ),
                (
                    "parking_space",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reservations",
                        to="parking_place.parkingspace",
                    ),
                ),
                (
                    "vehicle",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reservations",
                        to="parking_place.vehicle",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
