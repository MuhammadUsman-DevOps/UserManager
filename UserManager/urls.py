"""UserManager URL Configuration

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
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from UserManager import views, settings

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),

    path('permissions/', views.permissions, name='permissions'),
    path('assign/permission/', views.assign_permission, name='assign_permission'),
    path('edit/user/permission/<int:id>/', views.edit_user_permission, name='edit_user_permission'),
    path('update/user/permission/<int:id>/', views.update_user_permissions, name='update_user_permission'),

    path('users/', views.users, name='users'),
    path('user/update', views.update_user, name='update_user'),
    path('user/delete/<int:id>/', views.delete_user, name='delete_user'),
]

urlpatterns += staticfiles_urlpatterns()



