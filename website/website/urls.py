"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,include
from BookTicket import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.seehome),
    path('homepg/', views.seehomepg),
    path('login/',views.seelogin),
    path('pnr/',views.seepnr),
    path('search/',views.seesearch),
    path('register/',views.seereg),
    path('schedule/',views.seeschedule),
    path('form/',views.seeform),
    path('tickets/',views.seeticket),
    path('trschedule/',views.seetrschedule),
    path('confirm/',views.seeconfirm)
]
