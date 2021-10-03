# Generated by Django 3.2.7 on 2021-10-03 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("testapp", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="customer",
            old_name="name",
            new_name="first_name",
        ),
        migrations.AddField(
            model_name="customer",
            name="last_name",
            field=models.CharField(default="", max_length=255),
            preserve_default=False,
        ),
    ]
