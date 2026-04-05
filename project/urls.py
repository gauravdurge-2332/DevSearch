from django.urls import path

from . import views

urlpatterns = [
    path("project_view/", views.homepage, name="project"),
    path("project/<uuid:id>/", views.project, name="project_det"),
    path("project-creation/", views.project_creation, name="create_project"),
    path("update-project/<uuid:pk>/", views.update_creation, name="update_project"),
    path("delete-project/<uuid:pk>/", views.delete_creation, name="delete_project"),
    path("allProfile_projects" , views.allProjectsMade , name="projectshowcase")
]
