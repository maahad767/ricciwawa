# Generated by Django 3.2.7 on 2021-12-08 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0017_auto_20211208_2338'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]