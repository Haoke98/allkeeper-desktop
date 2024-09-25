# Generated by Django 4.2.3 on 2024-08-02 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jumpService', '0008_alter_systemuser_options'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='systemuser',
            constraint=models.UniqueConstraint(fields=('system', 'username'), name='unique_judge_by_system'),
        ),
    ]
