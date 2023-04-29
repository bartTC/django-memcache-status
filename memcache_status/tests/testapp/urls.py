import os

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import re_path

admin.autodiscover()

urlpatterns = [re_path(r"^admin/", admin.site.urls)] + static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT,
)

if os.getenv("TEST_WITH_DEBUGTOOLBAR", "off") == "on":
    import debug_toolbar
    from django.urls import include, path

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
