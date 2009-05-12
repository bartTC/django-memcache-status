from django import template
from django.core.cache import cache

register = template.Library()

class CacheStats(template.Node):
    
    def render(self, context):
        try:
            cache_stats = cache._cache.get_stats()
            cache_stats_sorted = []
            for server, stats_dict in sorted(cache_stats):
                cache_stats_sorted.append((server, self.reformat_stats(stats_dict)))
            cache_stats = cache_stats_sorted
        # The current cache backend does not provide any statistics
        except AttributeError:
            cache_stats = None
        context['cache_stats'] = cache_stats
        return ''
    
    def reformat_stats(self, stats_dict):
        # Reformat stat values
        formatted_stats = {}
        for key in stats_dict.keys():
            value = stats_dict[key]
            try:
                func = getattr(self, 'format_%s_value' % key.lower())
                formatted_stats[key] = func(value)
            except AttributeError:
                formatted_stats[key] = value
        return formatted_stats
    
    def format_uptime_value(self, value):
        return self.fractTimestamp(int(value))

    def fractTimestamp(self, s):
        years, s = divmod(s, 31556952)
        min, s = divmod(s, 60)
        h, min = divmod(min, 60)
        d, h = divmod(h, 24)
        return '%sy, %sd, %sh, %sm, %ss' % (years, d, h, min, s)


@register.tag
def get_cache_stats(parser, token):
    return CacheStats()

@register.filter
def prettyname(name):
    return ' '.join([word.capitalize() for word in name.split('_')])