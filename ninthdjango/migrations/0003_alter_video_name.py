# Generated by Django 4.2.10 on 2024-03-26 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ninthdjango', '0002_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='name',
            field=models.CharField(),
        ),
    ]
