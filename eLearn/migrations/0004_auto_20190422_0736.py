# Generated by Django 2.1.7 on 2019-04-22 07:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eLearn', '0003_auto_20190422_0628'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='video_id',
            new_name='videoid',
        ),
    ]
