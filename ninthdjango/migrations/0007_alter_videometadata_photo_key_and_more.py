# Generated by Django 4.2.10 on 2024-04-18 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ninthdjango', '0006_videometadata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videometadata',
            name='photo_key',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='videometadata',
            name='video_key',
            field=models.TextField(blank=True, null=True),
        ),
    ]
