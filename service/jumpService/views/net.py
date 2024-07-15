# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/6/13
@Software: PyCharm
@disc:
======================================="""
import os
from django.shortcuts import render
from django.http import HttpResponse
from ..models import Net, IPAddress, NetDevice
import graphviz


def generate_graphviz_syntax_v1(nets, ip_addresses, devices):
    dot = graphviz.Digraph(comment='Network Topology')

    for net in nets:
        dot.node(f'net{net.id}', f'Net: {net.content}')

    for device in devices:
        dot.node(f'device{device.id}', f'Device: {device.id}')

    for ip in ip_addresses:
        dot.node(f'ip{ip.id}', f'IP: {ip.ip}')
        if ip.net:
            dot.edge(f'net{ip.net.id}', f'ip{ip.id}')
        if ip.device:
            dot.edge(f'ip{ip.id}', f'device{ip.device.id}')

    return dot


def generate_graphviz_syntax_v2(nets, ip_addresses, devices):
    dot = graphviz.Digraph(comment='Network Topology')

    # 添加网段节点
    for net in nets:
        dot.node(f'net{net.id}', f'Net: {net.content}')

    # 添加设备及其IP地址的子图
    for device in devices:
        with dot.subgraph(name=f'cluster_device{device.id}') as subgraph:
            subgraph.attr(label=f'Device: {device.id}')
            subgraph.node(f'device{device.id}', f'Device: {device.id}')
            device_ips = ip_addresses.filter(device=device)
            for ip in device_ips:
                subgraph.node(f'ip{ip.id}', f'IP: {ip.ip}')
                if ip.net:
                    dot.edge(f'net{ip.net.id}', f'ip{ip.id}')
                subgraph.edge(f'device{device.id}', f'ip{ip.id}')
    return dot


def generate_graphviz_syntax_v3(nets, ip_addresses, devices):
    dot = graphviz.Digraph('ER', comment='Network Topology')
    # 添加设备及其IP地址的子图
    for device in devices:
        with dot.subgraph(name=f'cluster_device{device.id}') as subgraph:
            subgraph.attr(label=f'Device: {device.id}')
            device_ips = ip_addresses.filter(device=device)
            for ip in device_ips:
                subgraph.node(f'device_ip{ip.id}', f'DIP: {ip.ip}')

    # 添加网段节点
    # _nets = [nets.first()]
    _nets = nets.all()
    for net in _nets:
        print(net.id)
        with dot.subgraph(name=f'cluster_{net.id}') as subgraph:
            subgraph.attr(style='filled', color='lightgrey')
            subgraph.attr(label=f'Net: {net.content}')
            _ips = ip_addresses.filter(net=net)
            for ip in _ips:
                subgraph.node(f'net_ip{ip.id}', f'NIP: {ip.ip}')
                subgraph.edge(f'net_ip{ip.id}', f'device_ip{ip.id}')
    print(dot)
    return dot


def generate_mermaid_mindmap(nets, ip_addresses, devices):
    mermaid_str = "mindmap\n"

    # 添加网段节点
    for net in nets:
        mermaid_str += f'  {net.content}\n'
        # 添加网段中的IP地址
        net_ips = ip_addresses.filter(net=net)
        for ip in net_ips:
            mermaid_str += f'    {ip.ip}\n'
            # 添加IP地址的设备
            if ip.device:
                mermaid_str += f'      Device: {ip.device.id}\n'

    # 添加设备节点及其IP地址
    for device in devices:
        mermaid_str += f'  Device: {device.id}\n'
        device_ips = ip_addresses.filter(device=device)
        for ip in device_ips:
            mermaid_str += f'    IP: {ip.ip}\n'

    return mermaid_str


def network_topology(request):
    nets = Net.objects.all()
    ip_addresses = IPAddress.objects.all()
    devices = NetDevice.objects.all()
    graph = generate_graphviz_syntax_v3(nets, ip_addresses, devices)
    mermaid_str = generate_mermaid_mindmap(nets, ip_addresses, devices)
    print("===" * 30)
    print(mermaid_str)
    svg_content = graph.pipe(format='svg').decode('utf-8')

    return HttpResponse(svg_content, content_type='image/svg+xml')
