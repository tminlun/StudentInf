# _*_ encoding:utf-8 _*_
__author__: ''
__date__: '2019/11/28 0028 21:20'


import xadmin
from xadmin import views



# 配置adminx
class BaseSetting(object):
    # 开启主题功能
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = '后台管理界面'
    site_footer = '学生管理系统'
    menu_style = 'accordion'


xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)#views.(点)
