# Generated by Django 4.0.4 on 2022-05-29 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0003_alter_user_bio_alter_user_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="bio",
        ),
        migrations.AlterField(
            model_name="user",
            name="name",
            field=models.CharField(max_length=200, null=True),
        ),
    ]
