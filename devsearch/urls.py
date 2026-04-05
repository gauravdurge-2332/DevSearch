"""
URL configuration for devsearch project.

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

from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("users.urls")),
    path('api/' , include("api.urls")),
    path("projects/", include("project.urls")),
    

    #This is all Djangos inbuilt mechanism the Class have all the system set already we have to jsut use it properly.....
    #for revision purpose go to the Documentation and search Django Auth the Go down and search the Auth_views the things wil be explained properly
    # but this all are inbuilt and there is thing to just change the template of the template......

    path("reset_password/" , auth_views.PasswordResetView.as_view(template_name="reset_password.html") , name="reset_password"),
    path("reset_password_sent/" , auth_views.PasswordResetDoneView.as_view(template_name="reset_password_sent.html") , name="password_reset_done") , 
    
    #This is all present in the above module..
    path("reset/<uidb64>/<token>/" , auth_views.PasswordResetConfirmView.as_view(template_name="reset.html") , name="password_reset_confirm"),

    path("reset_password_complete/" , auth_views.PasswordResetCompleteView.as_view(template_name="reset_password_complete.html") , name="password_reset_complete"),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
