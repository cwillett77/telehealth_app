# Generated by Django 5.0.1 on 2024-02-12 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_alter_customuser_credentials"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="credentials",
            field=models.TextField(blank=True, null=True),
        ),
    ]
