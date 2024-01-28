#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self,
                        index: int = None, page_size: int = 10) -> Dict:
        """Returns an indexed hypermedia pagination"""
        assert all([isinstance(index, int), isinstance(page_size, int)])
        assert index <= len(self.indexed_dataset()) and index >= 0
        data = []
        cursor = index
        while len(data) < page_size:
            data_from_index = self.indexed_dataset().get(cursor, None)
            if data_from_index is not None:
                data.append(data_from_index)
            cursor += 1
        return {
            'index': index,
            'data': data,
            'page_size': page_size,
            'next_index': cursor
        }
