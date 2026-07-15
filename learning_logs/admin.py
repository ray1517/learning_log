from django.contrib import admin
from .models import Topic, Entry

# 全局分页基类，统一分页配置
class BaseAdmin(admin.ModelAdmin):
    list_per_page = 20       # 每页20条，优化分页
    list_max_show_all = 100
    show_full_result_count = False  # 大数据量提速，不统计总条数

# 主题管理配置
class TopicAdmin(BaseAdmin):
    # 列表展示字段 + 后台中文表头
    list_display = ("text", "owner", "public", "date_added")
    # 右侧筛选栏
    list_filter = ("owner", "public")
    # 顶部搜索框
    search_fields = ("text",)
    # 编辑页横向排版
    fieldsets = [
        ("主题信息", {"fields": ["text", "public"]}),
        ("归属信息", {"fields": ["owner"]}),
    ]

# 笔记管理配置
class EntryAdmin(BaseAdmin):
    list_display = ("text", "topic", "date_added")
    list_filter = ("topic",)
    search_fields = ("text",)
    fieldsets = [
        ("笔记内容", {"fields": ["text"]}),
        ("所属主题", {"fields": ["topic"]}),
    ]

admin.site.register(Topic, TopicAdmin)
admin.site.register(Entry, EntryAdmin)