from collections import Counter, defaultdict
from typing import Callable, Iterable
import pandas as pd
import pickle


class DocFilterer:

    def __init__(self, id_attr: str = 'id'):
        self.docs = []
        self.filters = []
        self.id_attr = id_attr

    def add_filter(self, attr_name: str, filter_fct: Callable[[any], bool], attr_fct_kwargs=None, filter_fct_kwargs=None):
        f = {'attr_name': attr_name,
             'filter_fct': filter_fct,
             'attr_fct_kwargs': attr_fct_kwargs or {},
             'filter_fct_kwargs': filter_fct_kwargs or {}
             }

        self.filters.append(f)

    def evaluate_doc(self, doc):
        is_valid = True
        for d in self.filters:
            attr = getattr(doc, d['attr_name'])
            attr_kwargs = d['attr_fct_kwargs']
            filter_fct = d['filter_fct']
            filter_kwargs = d['filter_fct_kwargs']

            if callable(attr):
                is_valid = filter_fct(attr(**attr_kwargs), **filter_kwargs)
            else:
                is_valid = filter_fct(attr, **filter_kwargs)
            if not is_valid:
                break
        if is_valid:
            attr = getattr(doc, self.id_attr)
            self.docs.append(attr if not callable(attr) else attr())

    def to_pickle(self, path):
        pickle.dump(self, open(path, 'wb'))

    @classmethod
    def read_pickle(cls, path):
        return pickle.load(open(path, 'rb'))

    @classmethod
    def filter_in_allowlist(cls, value: any, allowlist):
        return value in allowlist

