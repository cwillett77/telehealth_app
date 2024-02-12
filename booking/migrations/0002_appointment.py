# Generated by Django 5.0.1 on 2024-02-12 02:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Appointment",
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
                ("appointment_time", models.DateTimeField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("booked", "Booked"),
                            ("completed", "Completed"),
                            ("cancelled", "Cancelled"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "doctor",
                    models.ForeignKey(
                        limit_choices_to={"user_type": "doctor"},
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="doctor_appointments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        limit_choices_to={"user_type": "patient"},
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="patient_appointments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
