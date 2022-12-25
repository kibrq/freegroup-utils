from typing import List

def is_sublist(t: List, s: List):
    if len(s) == 0:
        return False
    for i in range(len(s) - len(t)):
        if all(map(lambda v: v[0] == v[1], zip(t, s[i:i+len(t)]))):
            return True
    return False

