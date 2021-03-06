# Generated by Django 3.2.7 on 2021-12-08 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0016_auto_20211208_2324'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='object_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.PositiveSmallIntegerField(choices=[(0, 'announcement'), (10, 'like'), (20, 'comment'), (30, 'follow'), (40, 'subscribe')], default=4),
        ),
    ]
