# Generated by Django 3.2.7 on 2021-11-06 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0007_alter_multiplechoicequestionattempt_selected_choices'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inputanswerquestionattempt',
            name='points_achieved',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='multiplechoicequestionattempt',
            name='points_achieved',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
