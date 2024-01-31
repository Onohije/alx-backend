#!/usr/bin/env python3
"""100. LFU Caching"""
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """"a caching system using LFU replacement policies"""

    def __init__(self):
        """Initializes LFUCache instance"""
        super().__init__()
        self.__tracking = []

    def index(self, key):
        """Return the index of a key in cache or None"""
        i = 0
        for saved_key, count in self.__tracking:
            if saved_key == key:
                return i
            i += 1
        return None

    def hit(self, key):
        """Update hit count of the matching key"""
        index = self.index(key)
        if index is None:
            return
        _key, count = self.__tracking[index]
        self.__tracking[index] = (_key, count + 1)

    def pop(self):
        """Removes tracking for a matching key, return key"""
        from functools import reduce
        match = reduce(lambda x, y: x if x[1] <= y[1] else y,
                       self.__tracking)
        _key, count = self.__tracking.pop(self.__tracking.index(match))
        return _key

    def put(self, key, item):
        """Inserts a new key, value pair into cache"""
        if not all([key, item]):
            return
        self.cache_data.update({key: item})

        if len(self.cache_data) <= self.MAX_ITEMS:  # cache not filled
            if self.index(key) is None:
                self.__tracking.append((key, 0))
            else:
                self.hit(key)
            return

        # cache filled up
        if self.index(key) is None:
            popped_key = self.pop()
            self.cache_data.pop(popped_key)
            print('DISCARD: {}'.format(popped_key))
            self.__tracking.append((key, 0))
        return

    def get(self, key):
        """Returns a value for a matching key in cache,
        or None if not exists"""
        self.hit(key)
        return self.cache_data.get(key, None)
