# Generated by Django 5.1.1 on 2024-10-11 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jumpService', '0013_delete_sshservice'),
    ]

    operations = [
        migrations.AddField(
            model_name='bt',
            name='ssl',
            field=models.BooleanField(blank=True, default=False, verbose_name='SSL'),
        ),
    ]
