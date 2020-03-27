"""project_2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from django.conf.urls import include, url
from django.conf import settings
from . import views
from django.conf.urls.static import static
from . import scheduler

app_name = 'project_2'
urlpatterns = [
    #기본 홈화면
    url(r'^$', views.Project_main.as_view(), name='project_2'),

    #추가
    path('add', views.add, name='add'),
    
    #수정 
    path('<int:idx>/edit', views.edit, name='edit'),

    #스케줄러 on
    path('<int:idx>/on', views.on, name='on'),

    #스케줄러 off
    path('<int:idx>/off', views.off, name='off'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
