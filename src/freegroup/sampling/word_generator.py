from numpy import random
from typing import List, Tuple, Callable
import math

from ..core import Word, reciprocal


def constant(v):
    return lambda: v

def uniform(low, high):
    return lambda: random.randint(low, high)

def uniform_hyperbolic(radius):
    return lambda: max(1, int(round(math.acosh(1 + random.random() * (math.cosh(radius) - 1)))))


class Generator:
    def __init__(self): pass
    
    def __iter__(self): return self
    
    def __next__(self) -> Word: raise NotImplementedError

class FreeGroupGenerator(Generator):
    def __init__(self, n_generators: int, length_fn: Callable[[], int]):
        self.n_generators = n_generators
        self.length_fn = length_fn

    def __next__(self):
        word, length = [], self.length_fn()
        generators = list(range(-self.n_generators, self.n_generators + 1))
        generators.remove(0)

        for _ in range(length):
            word.append(random.choice(generators))
            generators.remove(word[-1])
            if len(word) > 1:
                generators.append(word[-2])
        
        return word


def random_bracket_sequence(n):
    """Generates a balanced sequence of n +1s and n -1s corresponding to correctly nested brackets."""
    # "Generating binary trees at random", Atkinson & Sack, 1992

    # Generate a randomly shuffled sequence of n +1s and n -1s
    # These are steps 1 and 2 of the algorithm in the paper
    seq = [-1, 1] * n
    random.shuffle(seq)

    # This now corresponds to a balanced bracket sequence (same number of
    # opening and closing brackets), but it might not be well-formed
    # (brackets closed before they open). Fix this up using the bijective
    # map in the paper (step 3).
    prefix = []
    suffix = []
    word = []
    partial_sum = 0
    for s in seq:
        word.append(s)
        partial_sum += s
        if partial_sum == 0: # at the end of an irreducible balanced word
            if s == -1: # it was well-formed! append it.
                prefix += word
            else:
                # it was not well-formed! fix it.
                prefix.append(1)
                suffix = [-1] + [-x for x in word[1:-1]] + suffix
            word = []

    return prefix + suffix


def random_from_identities(n_param: int, identites: List[Tuple[Word, Word]]):
    seq = random_bracket_sequence(n_param)

    match, stack = [None] * len(seq), []

    for i, c in enumerate(seq):
        stack.append((i, c))
        if len(stack) < 2:
            continue
        (i1, c1), (i2, c2) = stack[-2], stack[-1]
        if c1 == -c2:
            del stack[-2:]
            match[i1] = i2
            match[i2] = i1

    sampled = [None] * len(seq)

    for idx, match_idx in enumerate(match):
        sampled[idx], sampled[match_idx] = identites[random.choice(len(identites))]
        if random.random() > 0.5:
            sampled[idx], sampled[match_idx] = sampled[match_idx], sampled[idx]
    
    return sum(sampled, [])


def create_identites_from_normal_closure(n_generators: int, base: Word):
    identities = [([-x], [x]) for x in range(1, n_generators + 1)]
    i_base = reciprocal(base)
    for t in range(0, len(base)):
        identities.append((base[:t], base[t:]))
        identities.append((i_base[:t], i_base[t:]))
    return identities


class NormalClosureGenerator(Generator):
    def __init__(self, base: Word, n_generators: int, depth_fn: Callable[[], int]):
        self.identities = create_identites_from_normal_closure(n_generators, base)
        self.depth_fn = depth_fn

    def __next__(self): return random_from_identities(self.depth_fn(), self.identities)
