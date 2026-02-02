from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LoginView, LogoutView

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from labzero import views as labzero_views


def get_urlpatterns():
    """
    Returns default URL patterns for labzero projects.
    """
    urlpatterns = [
        path("", labzero_views.dashboard, name="dashboard"),
        path(
            "login/",
            labzero_views.LoginView.as_view(),
            name="login",
        ),
        path("logout/", labzero_views.LogoutView.as_view(), name="logout"),
        path("admin/", admin.site.urls),
        path("cms/", include(wagtailadmin_urls)),
        path("documents/", include(wagtaildocs_urls)),
        path("pages/", include(wagtail_urls)),
    ]

    if settings.DEBUG:
        import debug_toolbar

        urlpatterns = [
            path("__debug__/", include(debug_toolbar.urls)),
        ] + urlpatterns

    return urlpatterns
