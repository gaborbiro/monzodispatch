"""monzodispatch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from monzodispatch.viewclasses import StaticFileView
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register', views.register_fcm_device),
    url(r'^$', views.form),
    url(r'^webhook/(?P<hash>[0-9\-]+)$', views.push),
    url(r'^event/', views.event),
    url(r'^test/', views.test),
    url(r'^investments/', views.investments),
    url(r'^rsssample.rss', StaticFileView.as_view(dir='files', file_name='remoteok.xml'))
]
