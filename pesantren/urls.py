"""pesantren URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib.auth.decorators import login_required


admin.site.login = login_required(admin.site.login, login_url='../../admin/login')
admin.site.site_header  =  "Administrasi"  
admin.site.site_title  =  "Administrasi"
admin.site.index_title  =  ""

urlpatterns = [
    path('admin/', include('django.contrib.auth.urls')),
    path('users/', admin.site.urls),
    path('pegawai/', include('kepegawaian.urls')),
    path('', include('kepegawaian.urls')),
]
