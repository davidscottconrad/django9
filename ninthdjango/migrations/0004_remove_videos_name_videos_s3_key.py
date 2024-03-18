# Generated by Django 4.2.10 on 2024-03-10 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ninthdjango', '0003_videos_description_videos_title_videos_uploaded_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videos',
            name='name',
        ),
        migrations.AddField(
            model_name='videos',
            name='s3_key',
            field=models.CharField(default='', max_length=500),
        ),
    ]