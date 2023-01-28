# Generated by Django 3.2.16 on 2023-01-28 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_alter_membership_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='permissions',
            field=models.IntegerField(choices=[(1, 'Read'), (2, 'Write'), (3, 'Admin')], default=1, max_length=255),
        ),
    ]