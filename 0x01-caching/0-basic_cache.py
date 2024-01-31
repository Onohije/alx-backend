#!/usr/bin/env python3
"""0. Basic dictionary"""
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """a caching system class definition"""

    def put(self, key, item):
        """Inserts a new key, value pair into cache"""
        if not all([key, item]):
            return
        self.cache_data.update({key: item})

    def get(self, key):
        """Returns a value for a matching key in cache,
        or None if not exists"""
        return self.cache_data.get(key, None)
