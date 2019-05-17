import os

import django
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin

admin.autodiscover()

urlpatterns = [url(r'^admin/', admin.site.urls)] + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)

IS_DJANGO_20 = django.VERSION >= (2,)

if os.getenv('TEST_WITH_DEBUGTOOLBAR', False) == 'on':
    if IS_DJANGO_20:
        import debug_toolbar
        from django.urls import include, path
        urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    else:
        import debug_toolbar
        from django.conf.urls import include
        urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]
