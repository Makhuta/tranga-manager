from django.urls import path

from . import views

urlpatterns = [
    path("ping/<int:pk>/", views.ping, name="ping"),
    path("test", views.test, name="test"),
    path("jobs/monitor/<int:pk>/", views.jobs_monitor, name="jobs_monitor"),
    path("jobs/running/<int:pk>/", views.jobs_running, name="jobs_running"),
    path("jobs/waiting/<int:pk>/", views.jobs_waiting, name="jobs_waiting"),
    path("manga/cover", views.manga_cover, name="manga_cover"),
    path("manga/search", views.manga_search, name="manga_search"),
    path("manga/monitor", views.manga_monitor, name="manga_monitor"),
    path("connectors/<int:pk>", views.connectors, name="connectors"),
    path("connectors/<int:pk>/languages", views.connectors_languages, name="connectors_languages"),
    path("language", views.language_name, name="language_name"),
    path("api/<int:pk>/manga/start", views.start_manga, name="manga_start"),
    path("api/<int:pk>/manga/cancel", views.cancel_manga, name="manga_cancel"),
    path("api/<int:pk>/manga/delete", views.delete_manga, name="manga_delete"),
    path("api/<int:pk>/manga/chapters", views.chapters, name="manga_chapters"),
]