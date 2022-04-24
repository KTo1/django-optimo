"""geekshop URL Configuration

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

from django.urls import path
from authapp.views import LogoutTemplateView, LoginTemplateView, RegisterTemplateView, ProfileTemplateView


app_name = 'authapp'
urlpatterns = [
    path('login', LoginTemplateView.as_view(), name='login'),
    path('logout', LogoutTemplateView.as_view(), name='logout'),
    path('register', RegisterTemplateView.as_view(), name='register'),
    path('profile/<int:pk>', ProfileTemplateView.as_view(), name='profile'),
]
