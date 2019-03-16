from __future__ import unicode_literals

from django.apps import AppConfig


class MemcacheStatusConfig(AppConfig):
    name = 'memcache_status'
    verbose_name = "MemcacheStatus"

    def show_cache_stats(self, request):
        """
        Memcache stats are only displayed to Users with `is_superuser`
        permission. You can overwrite this behavior using your custom
        AppConfig.

        :param request: Django View Request
        :return bool: Whether to show cache stats for the current request/user.
        """
        return request.user.is_superuser
