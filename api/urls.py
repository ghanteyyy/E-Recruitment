"""
URL configuration for E_Recruitment project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from . import views


urlpatterns = [
    path('api/login', views.Login.as_view(), name='login'),
    path('api/register', views.Register.as_view(), name='register'),
    path('api/profile/image', views.UpdateProfileImage.as_view(), name='profile_image'),
    path('api/user/documents', views.User_Document_view.as_view(), name='documents'),
    path('api/recruiter', views.Recruiter_view.as_view(), name="recruiters"),
    path('api/job', views.Job_view.as_view(), name="jobs"),
]
