from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
# 导入学习日志的全局分页基类
from learning_logs.admin import BaseAdmin

# 自定义用户管理：继承分页基类 + 原生UserAdmin
class CustomUserAdmin(BaseAdmin, UserAdmin):
    # 可额外自定义用户列表展示字段，示例：
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "is_active")
    # 用户列表筛选条件
    list_filter = ("is_staff", "is_active", "groups")
    # 用户搜索框
    search_fields = ("username", "email", "first_name", "last_name")

# 先注销默认User管理，再注册自定义版本
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)