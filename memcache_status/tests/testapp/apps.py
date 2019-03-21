from __future__ import unicode_literals

from django.apps import AppConfig

lorem = """
Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod 
tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At 
vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, 
no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit 
amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut 
labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam 
et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata 
sanctus est Lorem ipsum dolor sit amet.
"""


class MemcacheStatusTestAppConfig(AppConfig):
    name = 'memcache_status.tests.testapp'
    verbose_name = "MemcacheStatus Testapp"

    def ready(self):
        """
        Add some arbitraty data to the cache to have _some_ statistics.
        """
        from django.contrib import admin
        admin.site.index_template = 'memcache_status/admin_index.html'

        from django.core.cache import cache

        # Set 100 items. Generate 200 GET Hits. Generate 50 DELETE hits.
        for i in range(1, 100):
            key = 'TEST_VALUE_{0}'.format(i)
            cache.set(key, lorem)
            cache.get(key)
            cache.get(key)
            if i % 2 == 0:
                cache.delete(key)

        # Generate 100 GET misses and 50 DELETE misses.
        for i in range(100, 200):
            key = 'TEST_VALUE_{0}'.format(i)
            cache.get(key)
            if i % 2 == 0:
                cache.delete(key)




