from __future__ import unicode_literals

from django.test import TestCase


class MemcacheStatusSanityTests(TestCase):
    def setUp(self):
        from django.contrib.auth.models import User

        self.user = User.objects.create_superuser(
            'test', 'test@test.com', 'password'
        )
        self.client.login(username=self.user.username, password='password')

    def test_admin_accessible(self):
        response = self.client.get('/admin/')
        self.assertEqual(200, response.status_code)

    def test_cache_stats_included(self):
        response = self.client.get('/admin/')
        self.assertIn('cache-stats', str(response.content))


class MemcacheStatusPermissionsTests(TestCase):
    def test_non_superuser_cant_see_stats(self):
        from django.contrib.auth.models import User

        self.user = User.objects.create_user(
            'test', 'test@test.com', 'password'
        )
        self.client.login(username=self.user.username, password='password')
        response = self.client.get('/admin/')
        self.assertNotIn('cache-stats', str(response.content))
