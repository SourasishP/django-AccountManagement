"""login URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from login import views

urlpatterns = [
    path('admin/', admin.site.urls,name="admin"),
    path('', views.home,name="home"),
    path('register', views.register_page,name="register"),
    path('verify-user', views.verify_user,name="verify_email"),
	path('login', views.login1_page,name="login1"),
	path('login2', views.login2_page,name="login2"),
	path('logout', views.logout_page,name="user_logout"),
	path('home-user', views.home_logged,name="home_logged"),
	path('trnsfr', views.trnsfr,name="trnsfr"),
	path('show-details', views.show,name="show_details"),
	path('profile', views.profile,name="user-profile"),
]
