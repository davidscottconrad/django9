# Generated by Django 4.2.10 on 2024-04-18 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ninthdjango', '0007_alter_videometadata_photo_key_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie', models.FileField(upload_to='movies')),
            ],
        ),
    ]
