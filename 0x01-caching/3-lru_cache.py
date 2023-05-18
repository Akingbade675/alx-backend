#!/usr/bin/env python3
'''Implements Least Recently Used (LRU) cache replacement algorithm'''


from base_caching import BaseCaching


class LRUCache(BaseCaching):
    '''LRUCache inherits from the BaseCaching class'''
    
    def __init__(self):
        '''Initialize'''
        super().__init__()

        # a queue that tracks the use time of items
        # the least recntly used item is removed first
        self.queue = []

    def put(self, key, item):
        '''assign to the dictionary self.cache_data
        the item value for the key key'''
        if key is not None and item is not None:
            self.cache_data[key] = item

            # adding or modifying an item means it is the most recently used
            # the item is added to the end of the queue
            if key in self.queue:
                index = self.queue.index(key)
                self.queue.pop(index)
            self.queue.append(key)

            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                # the least recently used item is at the front of the queue
                # the the first item is popped
                key = self.queue.pop(0)
                del self.cache_data[key]
                print('DISCARD: {}'.format(key))

    def get(self, key):
        '''Returns: the value in self.cache_data linked to key'''
        value = self.cache_data.get(key)
        if not value:
            return None

        # reading an item means it is the most recently used
        # the item is added to the end of the queue
        index = self.queue.index(key) # gets the index of the MRU item
        self.queue.pop(index)
        self.queue.append(key)

        return value
