from numpy import random
from typing import List, Iterable, Callable
from functools import reduce as freduce
from itertools import islice
from tqdm import tqdm

from ..core import Word


def unique(iterable: Iterable[Word]) -> Iterable[Word]:
    seen = set()
    for el in iterable:
        if not tuple(el) in seen:
            seen.add(tuple(el))
            yield el


def subset(iterable: Iterable[List[Word]]) -> Iterable[List[Word]]:
    for el in iterable:
        result, subset = [], random.randint(0, 2 ** (len(el)))
        for i, w in enumerate(el):
            if subset & (1 << i):
                result.append(w)
        yield result


def shuffle(iterable: Iterable[List[Word]]) -> Iterable[List[Word]]:
    for el in iterable:
        result = list(el)
        random.shuffle(result)
        yield result


def join(*iterables: Iterable[Word]) -> Iterable[List[Word]]:
    return map(list, zip(*iterables))


def append(iterable: Iterable[Word], iterables: Iterable[List[Word]]) -> Iterable[List[Word]]:
    for els, el in zip(iterables, iterable):
        els.append(el)
        yield els


def reduce(fn: Callable[[Word, Word], Word], iterables: Iterable[List[Word]]) -> Iterable[Word]:
    return map(lambda l: freduce(fn, l) if l else [], iterables)


def take_unique(take: int, iterable: Iterable[Word], verbose = False) -> Iterable[Word]:
    iterable = islice(unique(iterable), take)
    return tqdm(iterable, total=take) if verbose else iterable
