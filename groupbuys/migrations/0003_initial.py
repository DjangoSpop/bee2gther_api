# Generated by Django 4.2.6 on 2024-07-03 15:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groupbuys', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupbuy',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]