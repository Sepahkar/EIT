"""Config URL Configuration

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
import os.path

from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from Systems.views import RedirectToLoadSystem

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectToLoadSystem),
    path('AuthUser', RedirectToLoadSystem),
    path('AuthUser/', RedirectToLoadSystem),
    path('Portal/', include('Systems.urls')),
    path('Cartable/', include('Cartable.urls')),

]