from django.urls import path

from task import views

urlpatterns = [
    path("", views.task_collection, name="task-list"),
    path("<int:task_id>/", views.task_resource, name="task-detail"),
]
