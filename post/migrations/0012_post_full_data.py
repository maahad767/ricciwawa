# Generated by Django 3.2.7 on 2021-11-29 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0011_auto_20211122_1836'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='full_data',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
