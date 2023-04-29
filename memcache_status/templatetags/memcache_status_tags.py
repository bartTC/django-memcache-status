from __future__ import annotations

import logging
from datetime import datetime

from django import template
from django.apps import apps
from django.template import Context

from memcache_status.utils import get_cache_stats

logger = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag(takes_context=True)
def memcache_status(context: Context) -> list:
    request = context.request
    config = apps.get_app_config("memcache_status")

    if not config.show_cache_stats(request):
        logger.debug("Cache stats not shown because user has no permission.")
        return []

    return get_cache_stats()


class PrettyValue:
    """
    Helper class that reformats the value. Looks for a method named
    ``format_<key>_value`` and returns that value. Returns the value
    as is, if no format method is found.
    """
    def decode(self, value: bytes | str) -> str:
        try:
            return value.decode()
        except AttributeError:
            return str(value)

    def format(self, key: str, value: bytes) -> str:
        if hasattr(self, f"format_{key.lower()}_value"):
            return getattr(self, f"format_{key.lower()}_value")(value)
        return self.decode(value)

    def format_limit_maxbytes_value(self, value: bytes) -> str:
        return f"{self.decode(value)} ({self.human_bytes(value)})"

    def format_bytes_read_value(self, value:bytes)->str:
        return f"{self.decode(value)} ({self.human_bytes(value)})"

    def format_bytes_written_value(self, value:bytes)->str:
        return f"{self.decode(value)} ({self.human_bytes(value)})"

    def format_uptime_value(self, value:str)->str:
        return self.fract_timestamp(int(value))

    def format_time_value(self, value:str) ->str:
        return datetime.fromtimestamp(int(value)).strftime("%x %X")

    def fract_timestamp(self, s:int) -> str:
        years, s = divmod(s, 31556952)
        min_, s = divmod(s, 60)
        h, min_ = divmod(min_, 60)
        d, h = divmod(h, 24)
        return f"{years}y, {d}d, {h}h, {min_}m, {s}s"

    def human_bytes(self, bytes_:bytes) -> str:
        bytes_ = float(bytes_)
        if bytes_ >= 1073741824:
            gigabytes_ = bytes_ / 1073741824
            size = "%.2fGB" % gigabytes_
        elif bytes_ >= 1048576:
            megabytes_ = bytes_ / 1048576
            size = "%.2fMB" % megabytes_
        elif bytes_ >= 1024:
            kilobytes_ = bytes_ / 1024
            size = "%.2fKB" % kilobytes_
        else:
            size = "%.2fB" % bytes_
        return size


@register.filter
def memcache_status_pretty_name(name: str) -> str:
    return " ".join([word.capitalize() for word in name.split("_")])


@register.filter
def memcache_status_pretty_value(value: str, key: str) -> str:
    return PrettyValue().format(key, value)
