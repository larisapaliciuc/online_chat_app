# Generated by Django 3.2.16 on 2023-01-19 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20230119_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.TextField(max_length=1024),
        ),
    ]
