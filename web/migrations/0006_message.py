# Generated by Django 5.1.1 on 2025-01-06 21:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0005_delete_info_userinfo_avatar"),
    ]

    operations = [
        migrations.CreateModel(
            name="Message",
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
                ("sender", models.CharField(max_length=32, verbose_name="发信人")),
                ("content", models.TextField(verbose_name="消息内容")),
                ("created_at", models.DateTimeField(verbose_name="发送时间")),
                (
                    "is_read",
                    models.BooleanField(default=False, verbose_name="是否已读"),
                ),
                (
                    "receiver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="web.order",
                        verbose_name="收信人",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
