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
        if key is not None and item is not None:
            self.cache_data[key] = item

            # adding or modifying an item means it is the most recently used
            # the item is added to the end of the queue
            if key in self.queue:
                index = self.queue.index(key)
                self.queue.pop(index)
            self.queue.append(key)
            self.freq_table[key] = self.freq_table[key] + 1 if self.freq_table.get(key) else 1

            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                # the least recently used item is at the front of the queue
                # the the first item is popped
                freq = sorted(self.freq_table.items(), key=lambda x:x[1])
                key = self.queue.pop(freq[0][1] if freq[0][1] != freq[1][1] else 0)
                del self.cache_data[key]
                del self.freq_table[key]
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




my_cache = LFUCache()
my_cache.put("A", "Hello")
my_cache.put("B", "World")
my_cache.put("C", "Holberton")
my_cache.put("D", "School")
my_cache.print_cache()
print(my_cache.get("B"))
my_cache.put("E", "Battery")
my_cache.print_cache()
my_cache.put("C", "Street")
my_cache.print_cache()
print(my_cache.get("A"))
print(my_cache.get("B"))
print(my_cache.get("C"))
my_cache.put("F", "Mission")
my_cache.print_cache()
my_cache.put("G", "San Francisco")
my_cache.print_cache()
my_cache.put("H", "H")
my_cache.print_cache()
my_cache.put("I", "I")
my_cache.print_cache()
print(my_cache.get("I"))
print(my_cache.get("H"))
print(my_cache.get("I"))
print(my_cache.get("H"))
print(my_cache.get("I"))
print(my_cache.get("H"))
my_cache.put("J", "J")
my_cache.print_cache()
my_cache.put("K", "K")
my_cache.print_cache()
my_cache.put("L", "L")
my_cache.print_cache()
my_cache.put("M", "M")
my_cache.print_cache()