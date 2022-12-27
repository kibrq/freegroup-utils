# freegroup-utils
Utilities to work with free groups

## Installation

Note: you need `pip` for this. Run the following commands:
- 
    ```
    git clone https://github.com/kibrq/freegroup-utils.git
    python3 -m pip install setuptools pybind11 ./freegroup-utils
    ```

## Usage

```python3

from freegroup import core as fgroup

fgroup.normalize([1, 2, 3, -3])
>>> [1, 2]
```

```python3

from freegroup import derivatives as d
from freegroup import core
import numpy as np

word = [1, 2, 3]

d.magnus_coefficients(core.to_numpy([word]), n_generators = 3, modulo = 8) # all methods accepts 2d-shape arrays as inputs
>>> ...
```

`freegroup.sampling` operates with infinite iterables. There are some utils and factories to work with and create such iterables.

The typical workflow with these iterables is the following:
- Create base iterables either `FreeGroupGenerator` or `NormalClosureGenerator`
- Apply transformations to these iterables
- Gather elements with `take_unique`

```python3
from freegroup import sampling as smp

g = smp.FreeGroupGenerator(n_generators = 3, length_fn = smp.constant(10))
# `g` produces words from F<3> of constant length 10

g = filter(lambda x: x[0] == 1, g)
# `g` produces words with `1` as their first symbol

g = smp.take_unique(100, g, verbose=True)
sampled = list(g)
# sampled contains 100 unique words from free group and nice progress bar is shown.
```
 

```python3
from freegroup import sampling as smp, core

gs = [smp.NormalClosureGenerator([i], 3, smp.constant(10)) for i in range(1, 3 + 1)]
gs += [smp.NormalClosureGenerator([1, 2, 3], 3, smp.constant(5))]
# `gs[0]` is an infinite iterable of words from <x>^F, `gs[1]` from <y>^F, ..., `gs[-1]` from <xyz>^F 
g = smp.join(*gs)
# `g` produces list of words `w`, where w[0] from <x>, w[1] from <y>, ..., w[-1] from <xyz>

g = smp.shuffle(g)
# `g` produces list of random permutations of words from <x>, <y>, <z>, <xyz>
g = smp.reduce(core.commutator, g)
# reduce this permutation with commutator, so
# `g` produces words from symmetric commutator of <x>, <y>, <z>, <xyz>

g = map(core.normalize, g)
# apply normalization to each element of this infinite iterable
g = filter(lambda x: 0 < len(x), g)
# filter zero words, so
# `g` produces nonzero words
```

```python3
from freegroup import sampling as smp, core
from itertools import repeat

gs = [smp.NormalClosureGenerator([i], 3, smp.constant(10)) for i in range(1, 3 + 1)]
gs += [smp.NormalClosureGenerator([1, 2, 3], 3, smp.constant(5))]
g = smp.join(*gs)
# `g` produces list of words `w`, where w[0] from <x>, w[1] from <y>, ..., w[-1] from <xyz>

g = smp.shuffle(g)
g = smp.reduce(core.commutator, g)
# `g` produces words from symmetric commutator of <x>, <y>, <z>, <xyz>

g = smp.join(*repeat(g, 5))
# `g` produces list of words with 5 elements from symmetric commutator
g = smp.subset(g)
# `g` produces list of words with random number (from 0 to 5) of elements from symmetric commutator
g = smp.reduce(core.multiply, g)
# `g` produces multiplications of several words from symmetric commutator
```

```python3
from freegroup import sampling as smp, core
from itertools import repeat

gs = [smp.NormalClosureGenerator([i], 3, smp.constant(10)) for i in range(1, 3 + 1)]
gs += [smp.NormalClosureGenerator([1, 2, 3], 3, smp.constant(5))]
g = smp.join(*gs)
# `g` produces list of words `w`, where w[0] from <x>, w[1] from <y>, ..., w[-1] from <xyz>

g = smp.shuffle(g)
g = smp.reduce(core.commutator, g)
# `g` produces words from symmetric commutator of <x>, <y>, <z>, <xyz>

g = smp.join(*repeat(g, 5))
g = smp.subset(g)
g = smp.append(repeat([1, 2, -1]), g)
g = smp.shuffle(g)
# `g` produces words like w_{i_1}..w_{i_k} u w_{j_1}...w_{j_s}, where u = [1, 2, -1], w_{i} from symmetric commutator, and `k` and `s` may be zeros. 
```


