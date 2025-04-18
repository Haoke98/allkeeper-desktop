# Generated by Django 4.2.20 on 2025-04-15 02:58

from django.db import migrations, models
import django.db.models.deletion
import simplepro.components.fields


class Migration(migrations.Migration):

    dependencies = [
        ('jumpService', '0024_add_initial_protocols'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceurl',
            name='domain',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='域名'),
        ),
        migrations.AlterField(
            model_name='operationsystem',
            name='image',
            field=simplepro.components.fields.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jumpService.operationsystemimage', verbose_name='系统镜像'),
        ),
        migrations.AlterField(
            model_name='service',
            name='system',
            field=simplepro.components.fields.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jumpService.operationsystem', verbose_name='操作系统'),
        ),
        migrations.AlterField(
            model_name='serviceurl',
            name='host',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='主机'),
        ),
        migrations.AlterField(
            model_name='serviceurl',
            name='port',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='端口'),
        ),
    ]
