"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path

from tantantang import views

urlpatterns = [
    path('user-configs', views.get_user_configs, name='get_user_configs'),
    path('user-configs/create', views.create_user_config, name='create_user_config'),
    path('user-configs/<int:user_id>/update', views.update_user_config, name='update_user_config'),
    path('user-configs/<int:user_id>/delete', views.delete_user_config, name='delete_user_config'),
    path('user-configs/<int:user_id>/start', views.start_bargain, name='delete_user_config'),
]
