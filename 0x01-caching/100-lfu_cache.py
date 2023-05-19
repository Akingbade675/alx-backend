#!/usr/bin/env python3
'''Implements Least Frequently Used (LFU) cache algorithm'''


from base_caching import BaseCaching


class LFUCache(BaseCaching):
    '''LFUCache inherits from the BaseCaching class'''

    def __init__(self):
        '''Initialize'''
        super().__init__()

        # a queue that tracks the use time of items
        # the least recntly used item is removed first
        self.queue = []
        self.freq_table = {}

    def put(self, key, item):
        '''assign to the dictionary self.cache_data
        the item value for the key key'''
        if key is None or item is None:
            return

        self.cache_data[key] = item

        # check if cache is full
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            # the least recently used item is at the front of the queue
            # the the first item is popped

            # Find the least frequency used items
            min_frequency = min(self.freq_table.values())
            least_frequent_keys = [
                                    k for k, v in self.freq_table.items()
                                    if v == min_frequency]

            # If there are multiple least frequent items, use LRU algorithm
            lru_key = self.queue[
                                min([self.queue.index(key)
                                    for key in least_frequent_keys])]
            del self.cache_data[lru_key]
            del self.freq_table[lru_key]
            print('DISCARD: {}'.format(lru_key))

        # adding or modifying an item means it is the most recently used
        # the item is added to the end of the queue
        if key in self.queue:
            index = self.queue.index(key)
            self.queue.pop(index)
        self.queue.append(key)
        self.freq_table[key] = (self.freq_table[key] + 1
                                if self.freq_table.get(key) else 1)

    def get(self, key):
        '''Returns: the value in self.cache_data linked to key'''
        value = self.cache_data.get(key)
        if not value:
            return None

        # reading an item means it is the most recently used
        # the item is added to the end of the queue
        index = self.queue.index(key)  # gets the index of the MRU item
        self.queue.pop(index)
        self.queue.append(key)
        self.freq_table[key] += 1

        return value
