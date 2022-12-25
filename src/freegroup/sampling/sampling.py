from numpy.random import choice, shuffle, randint
from typing import List, Callable

from ..core import iterable_commutator, Word
from .utils import create_identites_from_normal_closure, random_from_identities


class WordGenerator:
    def __init__(self): pass
    
    def __iter__(self): return self
    
    def __next__(self) -> Word: raise NotImplementedError


class NormalClosureGenerator(WordGenerator):

    @staticmethod
    def constant_depth(base: Word, n_generators: int, depth: int):
        return NormalClosureGenerator(base, n_generators, lambda: depth)

    @staticmethod
    def uniform_depth(base: Word, n_generators: int, min_depth: int, max_depth: int):
        return NormalClosureGenerator(base, n_generators, lambda: randint(low=min_depth, high=max_depth))

    def __init__(self, base: Word, n_generators: int, depth_fn: Callable[[], int]):
        self.identities = create_identites_from_normal_closure(n_generators, base)
        self.depth_fn = depth_fn

    def __next__(self): return random_from_identities(self.depth_fn(), self.identities)


class JoiningGenerator(WordGenerator):

    @staticmethod
    def random_order_commutator(generators: List[WordGenerator]):
        def _reduce(xs: List[Word]):
            shuffle(xs)
            return iterable_commutator(xs)
        return JoiningGenerator(generators, _reduce)
    
    @staticmethod
    def commutator(generators: List[WordGenerator]):
        return JoiningGenerator(generators, iterable_commutator)

    @staticmethod
    def random_choice(generators: List[WordGenerator]):
        return JoiningGenerator(generators, lambda xs: xs[choice(len(xs))])

    def __init__(self, generators: List[WordGenerator], reduce_fn: Callable[[List[Word]], Word]):
        self.generators = generators
        self.reduce_fn = reduce_fn

    def __next__(self): return self.reduce_fn([next(g) for g in self.generators])
        