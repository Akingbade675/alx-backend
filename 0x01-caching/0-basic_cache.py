#!/usr/bin/env python3
'''defines a BasicCache class'''


from base_caching import BaseCaching


class BasicCache(BaseCaching):
    '''BasicCache inherits from BaseCaching'''

    def __init__(self):
        '''Initialize'''
        super().__init__()

    def put(self, key, item):
        '''assign to the dictionary self.cache_data
        the item value for the key key'''
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        '''Returns: the value in self.cache_data linked to key'''
        value = self.cache_data.get(key)
        if not value:
            return None
        return value
