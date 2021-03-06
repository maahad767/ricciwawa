# Generated by Django 3.2.7 on 2021-12-21 08:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_alter_user_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blockuser',
            name='by_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocked_users', to=settings.AUTH_USER_MODEL, verbose_name='blocked/ignored by'),
        ),
    ]
