from __future__ import unicode_literals

import os

from django.test import TestCase


class MemcacheStatusSanityTests(TestCase):
    def setUp(self):
        from django.contrib.auth.models import User

        self.user = User.objects.create_superuser(
            'test', 'test@test.com', 'password'
        )
        self.client.login(username=self.user.username, password='password')

    def test_admin_accessible(self):
        """
        First simple check to make sure the /admin/ page is accessible at
        all and we don't hit any 500 error e.g. with the cache or
        with debug toolbar.
        """
        response = self.client.get('/admin/')
        self.assertEqual(200, response.status_code)

    def test_cache_stats_included(self):
        """
        Make sure that the memcache-status template is rendered within
        the admin index page. This makes sure that at least one cache
        backend provided stats and none of them fail.
        """
        # Not all backends we test do provide stats. In that case
        # memcache-status wont render at all, so we can skip the test.
        # The check whether the backend breaks or not is done above.
        from django.conf import settings
        if settings.CACHES['default']['TEST_PROVIDES_STATS'] is False:
            self.skipTest('cache backend does not provide stats')

        response = self.client.get('/admin/')
        self.assertIn(
            '<div class="cache-stats">',
            str(response.content),
            '`div class="cache-stats"` tag not found in HTML',
        )

    def test_debugtoolbar_visible(self):
        """
        This checks that the debug toolbar is visible. We had some race
        conditions with the debug toolbar and it's cache panel in the past.
        """
        if os.getenv('TEST_WITH_DEBUGTOOLBAR', False) != 'on':
            self.skipTest('debug-toolbar is disabled, no need to test.')

        response = self.client.get('/admin/')
        self.assertIn(
            'id="djDebug"',
            str(response.content),
            '`id="djDebug"` tag not found in HTML',
        )


class MemcacheStatusPermissionsTests(TestCase):
    def test_non_superuser_cant_see_stats(self):
        """
        Onlu users with is_superuser permission can see memcache stats
        by default.
        :return:
        """
        from django.contrib.auth.models import User

        self.user = User.objects.create_user(
            'test', 'test@test.com', 'password'
        )
        self.client.login(username=self.user.username, password='password')
        response = self.client.get('/admin/')
        self.assertNotIn(
            '<div class="cache-stats">',
            str(response.content),
            '`div class="cache-stats"` FOUND in HTML but should be forbidden',
        )
