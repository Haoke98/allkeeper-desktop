# Generated by Django 4.2.20 on 2025-04-15 01:54

from django.db import migrations
from simplepro.lib import pkHelper


def add_initial_protocols(apps, schema_editor):
    Protocol = apps.get_model('jumpService', 'Protocol')
    protocols = [
        {
            'name': 'http',
            'default_port': 80,
            'is_web_protocol': True,
            'description': 'HTTP协议'
        },
        {
            'name': 'https',
            'default_port': 443,
            'is_web_protocol': True,
            'description': 'HTTPS安全协议'
        },
        {
            'name': 'ssh',
            'default_port': 22,
            'is_web_protocol': False,
            'description': 'SSH远程连接协议'
        },
        {
            'name': 'tcp',
            'default_port': None,
            'is_web_protocol': False,
            'description': 'TCP协议'
        },
        {
            'name': 'udp',
            'default_port': None,
            'is_web_protocol': False,
            'description': 'UDP协议'
        },
        {
            'name': 'ftp',
            'default_port': 21,
            'is_web_protocol': False,
            'description': 'FTP文件传输协议'
        },
        {
            'name': 'sftp',
            'default_port': 22,
            'is_web_protocol': False,
            'description': 'SFTP安全文件传输协议'
        },
        {
            'name': 'ldap',
            'default_port': 389,
            'is_web_protocol': False,
            'description': 'LDAP目录访问协议'
        },
        {
            'name': 'ldaps',
            'default_port': 636,
            'is_web_protocol': False,
            'description': 'LDAPS安全目录访问协议'
        }
    ]

    for protocol_data in protocols:
        protocol = Protocol(
            id=pkHelper.uuid_generator(),
            **protocol_data
        )
        protocol.save()


def remove_initial_protocols(apps, schema_editor):
    Protocol = apps.get_model('jumpService', 'Protocol')
    Protocol.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('jumpService', '0023_protocol_remove_serviceurl_url_serviceurl_host_and_more'),
    ]

    operations = [
        migrations.RunPython(add_initial_protocols, remove_initial_protocols),
    ]
