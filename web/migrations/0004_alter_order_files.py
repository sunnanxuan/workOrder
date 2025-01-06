# Generated by Django 5.1.1 on 2025-01-06 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0003_alter_order_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="files",
            field=models.JSONField(
                blank=True, default=list, null=True, verbose_name="附件"
            ),
        ),
    ]
