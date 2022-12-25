from numpy import random
from typing import List, Iterable, Callable
from functools import reduce as freduce

from ..core import Word


def unique(iterable: Iterable[Word]):
    seen = set()
    for el in iterable:
        if not tuple(el) in seen:
            seen.add(tuple(el))
            yield el


def subset(iterable: Iterable[List[Word]]):
    for el in iterable:
        result, subset = [], random.randint(0, 2 ** (len(el)))
        for i, w in enumerate(el):
            if subset & (1 << i):
                result.append(w)
        yield result


def shuffle(iterable: Iterable[List[Word]]):
    for el in iterable:
        result = list(el)
        random.shuffle(result)
        yield result


def join(*iterables: Iterable[Word]):
    return map(list, zip(*iterables))


def append(iterable: Iterable[Word], iterables: Iterable[List[Word]]):
    for els, el in zip(iterables, iterable):
        els.append(el)
        yield els


def reduce(fn: Callable[[Word, Word], Word], iterables: Iterable[List[Word]]):
    return map(lambda l: freduce(fn, l), iterables)
