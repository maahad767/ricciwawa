# Generated by Django 3.2.7 on 2022-01-24 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0003_auto_20220124_0004'),
    ]

    operations = [
        migrations.RenameField(
            model_name='versioninfo',
            old_name='latest_build_number',
            new_name='latest_version_number',
        ),
        migrations.RenameField(
            model_name='versioninfo',
            old_name='min_build_number',
            new_name='min_version_number',
        ),
    ]
