# Generated by Django 3.2.7 on 2021-12-16 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0020_alter_sharepost_sharer'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='position',
            field=models.IntegerField(default=0),
        ),
    ]
