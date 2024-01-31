#!/usr/bin/env python3
"""2. LIFO Caching"""
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """"a caching system using LIFO replacement policies"""

    def __init__(self):
        """Initializes LIFOCache instance"""
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
            else:
                self.__tracking.append(self.__tracking.pop(
                    self.__tracking.index(key)
                ))
            return

        # cache filled up
        if key not in self.__tracking:
            popped_key = self.__tracking.pop()
            self.cache_data.pop(popped_key)
            print('DISCARD: {}'.format(popped_key))
            self.__tracking.append(key)
        return

    def get(self, key):
        """Returns a value for a matching key in cache,
        or None if not exists"""
        return self.cache_data.get(key, None)
