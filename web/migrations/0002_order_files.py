# Generated by Django 5.1.1 on 2025-01-05 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="files",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="附件"
            ),
        ),
    ]