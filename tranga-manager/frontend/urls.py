from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("accounts/login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("accounts/logout/", views.my_logout, name="logout"),
    path("", views.index, name="index"),
    path("api/add/", views.add_api, name="api_add"),
    path("api/<int:pk>/delete/", views.delete_api, name="api_delete"),
    path("api/<int:pk>/monitor/", views.monitor_api, name="api_monitor"),
    path("api/<int:pk>/", views.view_api, name="api"),
    path("api/<int:pk>/manga", views.view_api, name="manga"),
]