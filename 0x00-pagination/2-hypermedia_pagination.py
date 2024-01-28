#!/usr/bin/env python3
"""2. Hypermedia pagination"""

import csv
import math
from typing import List, Tuple, Dict, Any


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Returns a tuple of size two containing a start index
    and an end index corresponding to the range of indexes"""
    return ((page - 1) * page_size, page * page_size)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Returns appropriated paginated data based on inputs"""
        assert all([isinstance(page, int), isinstance(page_size, int)])
        assert page > 0 and page_size > 0
        start_index, end_index = index_range(page, page_size)
        return self.dataset()[start_index: end_index]

    def get_hyper(self,
                  page: int = 1,
                  page_size: int = 10) -> Dict[str, Any]:
        """Returns a dictionary containing hypermedia pagination"""
        data = self.get_page(page, page_size)
        next_page = None if len(self.get_page(
            page + 1, page_size)) else page + 1
        prev_page = None if page - 1 <= 0 else page - 1
        total_pages = len(self.dataset()) / page_size

        return {
            'page_size': len(data),
            'page': page,
            'data': data,
            'next_page': next_page,
            'prev_page': prev_page,
            'total_pages': math.ceil(total_pages)
        }
