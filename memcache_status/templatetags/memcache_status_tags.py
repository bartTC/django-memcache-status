from django import template
from django.core.cache import cache

register = template.Library()

class CacheStats(template.Node):
    def render(self, context):
        try:
            cache_stats =  sorted(cache._cache.get_stats())
        # The current cache backend does not provide any statistics
        except AttributeError:
            cache_stats = None
        context['cache_stats'] = cache_stats
        return ''

@register.tag
def get_cache_stats(parser, token):
    return CacheStats()