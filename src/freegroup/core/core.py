from typing import List, Iterable
from functools import reduce


Word = List[int]


def reciprocal(word: Word) -> Word:
    return [-factor for factor in word[::-1]]


def conjugation(word: Word, conjugator: Word) -> Word:
    return reciprocal(conjugator) + word + conjugator


def commutator(x: Word, y: Word) -> Word:
    return reciprocal(x) + reciprocal(y) + x + y


def iterable_commutator(words: List[Word]): 
    return reduce(commutator, words)


def __check_is_sublist__(t: List, s: List):
    if len(s) == 0:
        return False
    for i in range(len(s) - len(t)):
        if all(map(lambda v: v[0] == v[1], zip(t, s[i:i+len(t)]))):
            return True
    return False


def iterable_normal_closure_embedding(base: Word, word: Word):
    reduced = []
    d_base, di_base = base * 2, reciprocal(base) * 2
    for f in word:
        reduced.append(f)
        if len(reduced) >= 2 and reduced[-2] == -reduced[-1]:
            del reduced[-2:]
        if len(reduced) >= len(base) and \
            (__check_is_sublist__(reduced[-len(base):], d_base) or \
                __check_is_sublist__(reduced[-len(base):], di_base)):
            del reduced[-len(base):]
        yield reduced


def normal_closure_embedding(base: Word, word: Word):
    result = None
    for f in iterable_normal_closure_embedding(base, word):
        result = f
    return result


def normalize(word: Word):
    return normal_closure_embedding(base = [], word = word)


from numpy import array, pad

def to_numpy(words: Iterable[Word]):
    words = list(words)
    max_length = max(map(len, words))
    return array(list(map(lambda v: pad(v, (0, max_length - len(v))), words)))


def to_str(word: Word) -> str:
    letters = 'xyzpqrstnmst'

    if max(map(abs, word)) - 1 > len(letters):
        raise ValueError('There are too many generators')

    s = [letters[abs(f) - 1] for f in word]
    s = [c.upper() if f < 0 else c for f, c in zip(word, s)]
    return ''.join(s)
