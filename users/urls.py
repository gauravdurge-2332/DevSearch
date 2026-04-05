from django.urls import path
from . import views

urlpatterns = [
    path("", views.profiles, name="temp"),
    path("loginPage/", views.loginUser, name="login-page"),
    path("logout/", views.logoutuser, name="logout"),
    path("register/", views.registerpage, name="register"),
    path("user-profile/<str:id>/", views.userProfile, name="userProfile"),
    path("useraccount/", views.useraccount, name="account"),
    path("editaccount/", views.editprofile, name="editaccount"),
    path("addskill/", views.createskills, name="addskill"),
    path("updateskill/<str:pk>/", views.updateskills, name="updateskill"),
    path("deleteskill/<str:pk>/", views.deleteskill, name="deleteskill"),
    path("inbox/", views.inbox, name="inbox"),
    path("message/<str:pk>/",views.singleMessage , name="message"),
    path("messageForm/<str:pk>",views.message_write , name="messagewrite"),

]
