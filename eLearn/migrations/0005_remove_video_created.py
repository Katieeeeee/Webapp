# Generated by Django 2.1.7 on 2019-04-22 09:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eLearn', '0004_auto_20190422_0736'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='created',
        ),
    ]
