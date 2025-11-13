from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import static
from django.urls import include, path
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView


admin.site.site_header = "Dansk Data Science Community"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="home.html")),
    path(
        "favicon.ico", RedirectView.as_view(url=settings.STATIC_URL + "favicon.ico")
    ),
    path("events/", include("events.urls", namespace="events"), name="events"),
    path("news/", include("news.urls", namespace="news"), name="news"),
    path("users/", include("users.urls"), name="users"),
    path("members/", include("members.urls"), name="members"),
    path("polls/", include("polls.urls"), name="polls"),
    path(
        "privacy/",
        TemplateView.as_view(template_name="privacy/privacy.html"),
        name="privacy",
    ),
    path("stats/", include("stats.urls", namespace="stats"), name="stats"),
    path("tinymce/", include("tinymce.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
