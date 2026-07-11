"""
URL configuration for ll_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    # 语言切换接口必须保留
    path('i18n/', include('django.conf.urls.i18n')),
]
# 所有页面路由包裹在 i18n_patterns 内，才会自动带上 /zh-hans/ /en/ 前缀
urlpatterns += i18n_patterns(
    path('', include('learning_logs.urls')),
    path('accounts/', include('accounts.urls')),
)