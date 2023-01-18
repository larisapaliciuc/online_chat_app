# Generated by Django 3.2.16 on 2023-01-18 19:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_membership'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='members',
            field=models.ManyToManyField(through='core.Membership', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='channel',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='creator_of', to=settings.AUTH_USER_MODEL),
        ),
    ]
