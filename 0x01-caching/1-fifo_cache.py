#!/usr/bin/env python3
'''Implements FIFO cache replacement algorithm'''


from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    '''FIFOCache inherits from the BaseCaching class'''

    def __init__(self):
        '''Initialize'''
        super().__init__()
        self.queue = []

    def put(self, key, item):
        '''assign to the dictionary self.cache_data
        the item value for the key key'''
        if key is not None and item is not None:
            self.cache_data[key] = item
            self.queue.append(key)

            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                key = self.queue.pop(0)
                del self.cache_data[key]
                print('DISCARD: {}'.format(key))

    def get(self, key):
        '''Returns: the value in self.cache_data linked to key'''
        value = self.cache_data.get(key)
        if not value:
            return None
        return value
