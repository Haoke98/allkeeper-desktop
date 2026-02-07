# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/11/28
@Software: PyCharm
@disc:
======================================="""
import random
from datetime import datetime

from django.contrib import admin
from django.db.models import QuerySet
from django.http import JsonResponse
from simplepro.admin import FieldOptions, BaseAdmin
from simplepro.decorators import button
from simplepro.dialog import ModalDialog
from simpleui.admin import AjaxAdmin

from ..models import Service, ServiceUser, ServiceType, ServerNew, OperationSystemImage,ServiceURL, Protocol
from ..forms import ServiceURLForm


@admin.register(ServiceType)
class ServiceTypeAdmin(BaseAdmin):
    list_display = ['id', 'name', 'remark', 'port', 'dashboardPort', 'defaultSuperUsername', 'defaultSuperUserPwd',
                    'official',
                    'code', 'doc', 'updatedAt', 'createdAt',
                    'deletedAt']
    search_fields = ['name', 'remark']
    list_filter = ['port', 'dashboardPort', ]
    actions = ['migrate']
    ordering = ('-updatedAt',)

    def _url(self, obj):
        res = ""
        if obj.system:
            ips = obj.system.server.ips.all()
            for i, ipObj in enumerate(ips):
                print(obj.system, ipObj.ip)
                uri = "http://"
                uri += f"{ipObj.ip}:{obj.port}"
                if len(ips) == 1:
                    res += f"""<a target="_blank" href="{uri}" >入口</a><button>复制</button>"""
                else:
                    res += f"""<a target="_blank" href="{uri}" >入口{i}</a><button>复制</button></br>"""
            return res
        return None

    _url.short_description = "入口"

    def formatter(self, obj, field_name, value):
        # 这里可以对value的值进行判断，比如日期格式化等
        if field_name in ["official", 'code', 'doc']:
            if value:
                return f"""<a href="{value}" target="_blank">点击跳转</a>"""
        return value

    fields_options = {
        'id': FieldOptions.UUID,
        'createdAt': FieldOptions.DATE_TIME,
        'updatedAt': FieldOptions.DATE_TIME,
        'deletedAt': FieldOptions.DATE_TIME,
        'system': {
            'min_width': '320px',
            'align': 'center'
        },
        'name': {
            'min_width': '220px',
            'align': 'left',
            "show_overflow_tooltip": True,
            "resizeable": True,
            "fixed": "left"
        },
        'port': {
            'min_width': "110px",
            'align': 'center'
        },
        'dashboardPort': {
            'min_width': "180px",
            'align': 'center'
        },
        'rootUsername': {
            'min_width': '180px',
            'align': 'center'
        },
        'rootPassword': {
            'min_width': '180px',
            'align': 'center'
        },
        'official': FieldOptions.LINK,
        'doc': FieldOptions.LINK,
        'code': {
            'width': "160px",
            'align': 'center'
        },
        'defaultSuperUsername': FieldOptions.USER_NAME,
        'defaultSuperUserPwd': FieldOptions.PASSWORD,
        'status': {
            'min_width': '180px',
            'align': 'left'
        },
        'remark': {
            'min_width': '240px',
            'align': 'left',
            "resizeable": True,
            "show_overflow_tooltip": True
        },
        'bios': {
            'min_width': '180',
            'align': 'center'
        },
        'cabinet': {
            'min_width': '180',
            'align': 'center'
        },
        'mac': FieldOptions.MAC_ADDRESS
    }

    @button(type='danger', short_description='数据迁移', enable=True, confirm="您确定要生成吗？")
    def migrate(self, request, queryset: QuerySet):

        #     old_id = qs.id
        #     qs.id = str(uuid.uuid4())
        #     print(old_id, ">>>", qs.id)
        #     qs.save()
        #     Service.objects.filter(id=old_id).delete()
        # qs.save()
        return {
            'state': True,
            'msg': f'迁移完成'
        }


class ServiceURLInlineAdmin(admin.TabularInline):
    model = ServiceURL
    form = ServiceURLForm
    extra = 0
    min_num = 0
    fields = ['name', 'protocol', 'domain', 'host', 'port', 'path', 'is_default', 'is_dashboard']
    verbose_name = "访问地址"
    verbose_name_plural = verbose_name

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "protocol":
            kwargs["queryset"] = Protocol.objects.all().order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields['host'].widget.template_name = 'admin/widgets/url_input.html'
        formset.form.base_fields['host'].required = False
        formset.form.base_fields['port'].required = False
        return formset


@admin.register(Protocol)
class ProtocolAdmin(BaseAdmin):
    list_display = ['id', 'name', 'default_port', 'is_web_protocol', 'description', 'updatedAt', 'createdAt']
    search_fields = ['name', 'description']
    list_filter = ['is_web_protocol']
    ordering = ['name']

    fields_options = {
        'id': FieldOptions.UUID,
        'name': {
            'min_width': '120px',
            'align': 'left'
        },
        'default_port': {
            'min_width': '100px',
            'align': 'center'
        },
        'is_web_protocol': {
            'min_width': '100px',
            'align': 'center'
        },
        'description': {
            'min_width': '300px',
            'align': 'left'
        },
        'createdAt': FieldOptions.DATE_TIME,
        'updatedAt': FieldOptions.DATE_TIME,
        'deletedAt': FieldOptions.DATE_TIME
    }


@admin.register(ServiceURL)
class ServiceURLAdmin(BaseAdmin):
    form = ServiceURLForm
    list_display = ['id', 'service', 'name', 'protocol', 'host', 'port', 'path', 'is_default', 'is_dashboard', 'updatedAt', 'createdAt']
    list_filter = ['service', 'protocol', 'is_default', 'is_dashboard']
    search_fields = ['name', 'host', 'path', 'service__system__server__remark']
    ordering = ('-is_default', '-updatedAt',)

    fields_options = {
        'id': FieldOptions.UUID,
        'createdAt': FieldOptions.DATE_TIME,
        'updatedAt': FieldOptions.DATE_TIME,
        'deletedAt': FieldOptions.DATE_TIME,
        'service': {
            'min_width': '320px',
            'align': 'left',
            "resizeable": True,
            "show_overflow_tooltip": True
        },
        'name': {
            'min_width': '200px',
            'align': 'left'
        },
        'protocol': {
            'min_width': '120px',
            'align': 'left'
        },
        'host': {
            'min_width': '200px',
            'align': 'left'
        },
        'port': {
            'min_width': '100px',
            'align': 'center'
        },
        'path': {
            'min_width': '300px',
            'align': 'left'
        },
        'is_default': {
            'min_width': '100px',
            'align': 'center'
        },
        'is_dashboard': {
            'min_width': '100px',
            'align': 'center'
        }
    }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "protocol":
            kwargs["queryset"] = Protocol.objects.all().order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # 添加datalist到模板
        form.template = form.template.replace(
            '{{ field.field }}',
            '''{{ field.field }}
            {% if field.name == "host" %}
            <datalist id="host-list">
                {% for choice in field.field.widget.attrs.datalist %}
                    <option value="{{ choice }}">
                {% endfor %}
            </datalist>
            {% endif %}'''
        )
        return form


class ServiceUserInlineAdmin(admin.TabularInline):
    model = ServiceUser
    extra = 0
    min_num = 0
    fields = ['owner', 'username', 'password', 'hasRootPriority']
    verbose_name = "服务用户"
    verbose_name_plural = verbose_name


@admin.register(Service)
class ServiceAdmin(AjaxAdmin):
    list_display = ['id', '_type', 'system', 'port', '_url', '_user_management', 'remark', 'updatedAt',
                    'createdAt',
                    'deletedAt']
    search_fields = ['system', 'port', 'remark']
    list_filter = ['_type', 'system__image', 'system__server']
    list_filter_multiples = ('_type','system__server',)
    actions = ['migrate', 'test_action', ]
    ordering = ('-updatedAt', '-createdAt',)
    inlines = [ServiceURLInlineAdmin, ServiceUserInlineAdmin]

    def _url(self, obj):
        _full_urls  = {}
        ips = obj.system.server.ips.all()
        for ip_port in ips:
            if ip_port.net is not None:
                if ip_port.net.is_global():
                    prefix = "公网"
                else:
                    prefix = "内网"

        # FIXME:影响列表页的渲染, 增加延迟, 需要改成固定, 让用户在单个item的详情页里进行渲染, 在详情页中选入口/切换入口
        # TODO: 实现通过 lanproxy 的 API 实时创建端口映射关系.
        #  可以先查看有没有和当前服务器处在同一个网段的 lanproxy客户端, 也就是有没有可用的channels
        conn_port = obj.dashboardPort
        port_maps = obj.system.server.right_ports.all()
        host_port_map = {}
        for i, ip_port in enumerate(ips):
            host_port_map[str(ip_port.ip)] = conn_port
        for i, port_map in enumerate(port_maps):
            if port_map.rightPort == conn_port:
                # print(" " * 10, "|", "-" * 10, f"{i}.", port_map)
                _ips = port_map.left.ips.all()
                for ip in _ips:
                    host_port_map[str(ip.ip)] = port_map.leftPort
        for i, (host, port) in enumerate(host_port_map.items()):
            schema = "http"
            if obj.sslOn:
                schema = "https"
            _url = f"{schema}://{host}:{port}"
            if obj.dashboardPath:
                _url = f"{_url}/{obj.dashboardPath}"
            _full_urls[_url] = f"{host}:{port}"

        for url in obj.urls.all():
            _urls = url.get_full_url()
            for net_work_remark,_url in _urls.items():
                if url.name:
                    verbose_name = str(url.name)+f"({net_work_remark})"
                else:
                    verbose_name = net_work_remark
                _full_urls[_url] = verbose_name
        a_tags = []
        for full_url,name in _full_urls.items():
            a_tags.append( f"""<a target="_blank" style="margin-right:10px;" href="{full_url}" >{name or full_url}</a>""")
        return "<br>".join(a_tags)

    _url.short_description = "访问地址"

    def get_layer_config(self, request, queryset):
        print("layer进行了..")
        return {
            # 弹出层中的输入框配置

            # 这里指定对话框的标题
            'title': '异步获取配置的输入框',
            # 提示信息
            'tips': '异步获取配置' + datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            # 确认按钮显示文本
            'confirm_button': '确认提交',
            # 取消按钮显示文本
            'cancel_button': '取消',

            # 弹出层对话框的宽度，默认50%
            'width': '40%',

            # 表单中 label的宽度，对应element-ui的 label-width，默认80px
            'labelWidth': "80px",
            'params': [{
                # 这里的type 对应el-input的原生input属性，默认为input
                'type': 'input',
                # key 对应post参数中的key
                'key': 'name',
                # 显示的文本
                'label': '名称',
                # 为空校验，默认为False
                'require': True,
                'value': random.randint(0, 100)
            }, {
                'type': 'select',
                'key': 'type',
                'label': '类型',
                'width': '200px',
                # size对应elementui的size，取值为：medium / small / mini
                'size': 'small',
                # value字段可以指定默认值
                'value': '0',
                'options': [{
                    'key': '0',
                    'label': '收入'
                }]
            }]
        }

    @button("测试", enable=True, icon="el-icon-view")
    def test_action(self, request, queryset):
        print("TestAction:", queryset)
        return JsonResponse(data={
            'status': 'success',
            'msg': '处理成功！'
        })

    test_action.layer = get_layer_config

    def _user_management(self, obj):
        # count = ServiceUser.objects.filter(service=obj).count()
        modal = ModalDialog()
        modal.width = "1400"
        modal.height = "400"
        # 这个是单元格显示的文本
        modal.cell = f'<el-link type="primary">管理用户</el-link>'
        modal.title = "用户列表"
        # 是否显示取消按钮
        modal.show_cancel = True
        # 这里的url可以写死，也可以用django的反向获取url，可以根据model的数据，传到url中
        # modal.url = reverse('admin:jumpService_serviceuser_changelist') + '?service_id=' + obj.id
        modal.url = '/jump_service/service/users?serviceId=' + obj.id
        return modal
        # return CellAction(text=f'<el-link type="primary">{count}</el-link>', action=self.test_action)

    _user_management.short_description = "用户"

    _user_management.layer = get_layer_config

    def formatter(self, obj, field_name, value):
        # 这里可以对value的值进行判断，比如日期格式化等
        if field_name == "ip":
            if value:
                return BaseAdmin.username(obj.ip)
        if field_name == 'rootPassword':
            if value:
                return BaseAdmin.password(obj.rootPassword)
        if field_name == "bios":
            if value:
                return BaseAdmin.password(obj.bios)
        return value

    fields_options = {
        'id': FieldOptions.UUID,
        'code': {
            'min_width': '88px',
            'align': 'center'
        },
        'createdAt': FieldOptions.DATE_TIME,
        'updatedAt': FieldOptions.DATE_TIME,
        'deletedAt': FieldOptions.DATE_TIME,
        'system': {
            'min_width': '320px',
            'align': 'left',
            "resizeable": True,
            "show_overflow_tooltip": True
        },
        'net': FieldOptions.IP_ADDRESS,
        'image': {
            'min_width': '160px',
            'align': 'center'
        },
        'port': {
            'min_width': '100px',
            'align': 'center'
        },
        'sslPort': {
            'min_width': '140px',
            'align': 'center'
        },
        '_url': {
            'min_width': '180px',
            'align': 'center'
        },
        'hoster': {
            'min_width': '320px',
            'align': 'left'
        },
        '_type': {
            'min_width': '220px',
            'align': 'left'
        },
        'status': {
            'min_width': '180px',
            'align': 'left'
        },
        'remark': FieldOptions.REMARK,
        'bios': {
            'min_width': '180',
            'align': 'center'
        },
        'cabinet': {
            'min_width': '180',
            'align': 'center'
        },
        'mac': FieldOptions.MAC_ADDRESS
    }

    @button(type='danger', short_description='数据迁移', enable=True, confirm="您确定要生成吗？")
    def migrate(self, request, queryset: QuerySet):
        # ess: list[ElasticSearch] = ElasticSearch.objects.all()
        # _type = ServiceType.objects.filter(name="ElasticSearch").first()
        # for es in ess:
        #     obj = Service()
        #     obj._type = _type
        #     system_image = OperationSystemImage.objects.filter(name="CentOS", version="7").first()
        #     server: ServerNew = es.server
        #     system = server.systems.filter(image=system_image).first()
        #     obj.system = system
        #     obj.port = es.port
        #     obj.remark = es.remark
        #     if es.info:
        #         obj.info = es.info + "<br/>"
        #     else:
        #         obj.info = ""
        #     if es.kibanaPwd:
        #         obj.info += "kibana_system:" + es.kibanaPwd + "<br/>"
        #     if es.apmPwd:
        #         obj.info += "apm_system:" + es.apmPwd + "<br/>"
        #     if es.logstashPwd:
        #         obj.info += "logstash_system:" + es.logstashPwd + "<br/>"
        #     if es.beatsPwd:
        #         obj.info += "beats_system:" + es.beatsPwd + "<br/>"
        #     if es.remoteMonitoringPwd:
        #         obj.info += "remote_monitoring_user:" + es.remoteMonitoringPwd + "<br/>"
        #     obj.save()

        return {
            'state': True,
            'msg': f'迁移完成'
        }


@admin.register(ServiceUser)
class ServiceUserAdmin(BaseAdmin):
    list_display = ['id', 'service', 'username', 'password', 'hasRootPriority', 'createdAt', 'updatedAt', 'deletedAt']
    list_filter = ['service', 'service__system__server', 'service__system', 'service___type', 'hasRootPriority']
    search_fields = ['username', 'password', 'service__system__server__remark']
    ordering = ('-updatedAt',)

    def formatter(self, obj, field_name, value):
        # 这里可以对value的值进行判断，比如日期格式化等
        if field_name == "ip":
            if value:
                return BaseAdmin.username(obj.ip)
        if field_name == 'rootPassword':
            if value:
                return BaseAdmin.password(obj.rootPassword)
        if field_name == "bios":
            if value:
                return BaseAdmin.password(obj.bios)
        return value

    fields_options = {
        'id': FieldOptions.UUID,
        'code': {
            'fixed': 'left',
            'min_width': '88px',
            'align': 'center'
        },
        'createdAt': {
            'min_width': '180px',
            'align': 'left'
        },
        'updatedAt': {
            'min_width': '180px',
            'align': 'left'
        },
        'deletedAt': {
            'min_width': '180px',
            'align': 'left'
        },
        'username': {
            'min_width': '200px',
            'align': 'left'
        },
        'password': {
            'min_width': '200px',
            'align': 'left'
        },
        'service': {
            'min_width': '300px',
            'align': 'left',
            "resizeable": True,
            "show_overflow_tooltip": True

        }
    }
