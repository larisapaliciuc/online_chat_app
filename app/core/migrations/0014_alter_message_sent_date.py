# Generated by Django 3.2.16 on 2023-01-23 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_message_sent_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='sent_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]