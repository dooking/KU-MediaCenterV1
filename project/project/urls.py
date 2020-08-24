"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # 0-Admin

    # 1-Startpage
    path('', views.main, name="main"),

    # 2-Introduce
    path('introduce/', views.introduce, name="introduce"),

    # 3-Borrow
    path('borrow/', views.step1, name="borrow"),
    path('borrow/step2', views.borrow_step2, name="borrow_step2"),
    path('borrow/finish', views.borrow_finish, name="borrow_finish"),

    path('accounts/', include('allauth.urls')),
    # registration
    # path('registration/signup',views.signup,name="signup"),
    # path('registration/login',views.login,name="login"),
    # path('registration/logout',views.logout,name="logout"),
]
