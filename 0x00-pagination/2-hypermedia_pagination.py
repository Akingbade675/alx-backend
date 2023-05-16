#!/usr/bin/env python3
'''ALX backend - Pagination'''


import csv
import math
from typing import Tuple, List, Dict, Union


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    '''
    Return: a tuple of size two containing a start index and
    an end index corresponding to the range of indexes to return
    in a list for those particular pagination parameters.
    '''
    return ((page - 1) * page_size, page * page_size)


class Server:
    '''Server class to paginate a database of popular baby names.
    '''
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        '''Cached dataset
        '''
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        '''use index_range to find the correct indexes to paginate
        the dataset correctly and return the appropriate page of the
        dataset (i.e. the correct list of rows).
        '''
        assert type(page) == int and page > 0
        assert type(page_size) == int and page > 0

        # find the correct indexes to paginate the dataset correctly
        offset, limit = index_range(page, page_size)
        return self.dataset()[offset:limit]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict[]:
        '''Returns: a dictionary'''
        data = self.get_page(page, page_size)
        total_data = len(self.dataset())
        start_index, end_index = index_range(page + 1, page_size)

        return {
            "page_size": 0 if data == [] else page_size,
            "page": page,
            "data": data,
            "next_page": page + 1 if start_index < total_data else None,
            "prev_page": page - 1 if page > 1 else None,
            "total_pages": math.ceil(total_data / page_size)
          }
