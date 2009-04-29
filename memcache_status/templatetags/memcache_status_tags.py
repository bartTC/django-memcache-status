from django import template
from django.core.cache import cache

register = template.Library()

class CacheStats(template.Node):
    def render(self, context):
        context['cache_stats'] = sorted(cache._cache.get_stats())
        return ''

@register.tag
def get_cache_stats(parser, token):
    return CacheStats()