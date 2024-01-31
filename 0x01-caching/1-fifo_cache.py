#!/usr/bin/env python3
"""1. FIFO caching"""
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """"a caching system using FIFO replacement policies"""

    def __init__(self):
        """Initializes FIFOCache instance"""
        super().__init__()
        self.__tracking = []

    def put(self, key, item):
        """Inserts a new key, value pair into cache"""
        if not all([key, item]):
            return
        self.cache_data.update({key: item})

        if len(self.cache_data) <= self.MAX_ITEMS:  # cache not filled
            if key not in self.__tracking:
                self.__tracking.append(key)
            return

        # cache filled up
        if key not in self.__tracking:
            popped_key = self.__tracking.pop(0)
            self.cache_data.pop(popped_key)
            print('DISCARD: {}'.format(popped_key))
            self.__tracking.append(key)
        return

    def get(self, key):
        """Returns a value for a matching key in cache,
        or None if not exists"""
        return self.cache_data.get(key, None)
