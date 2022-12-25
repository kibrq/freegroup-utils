# freegroup-utils
Utilities to work with free groups

## Installation

Make sure that `pip`, `setuptools`, `pybind11` are installed.

Then just run
`python3 -m pip install .`

## Usage

```python3

from freegroup import core as fgroup

fgroup.normalize([1, 2, 3, -3])
>>> [1, 2]
```

```python3

from freegroup import derivatives as d
import numpy as np

word = np.array([1, 2, 3])

d.magnus_coefficients(word.reshape(1, 1), n_generators = 3, modulo = 8) # all methods accepts 2d-shape arrays as inputs
>>> ...
```

`freegroup.sampling` operates with infinite iterables. There are some utils to work with and factories to create such iterables.

```python3
from freegroup import sampling as smp

g = smp.FreeGroupGenerator(n_generators = 3, length_fn = smp.constant(10))
# `g` produces words from F<3> of constant length 10

g = filter(lambda x: x[0] == 1, g)
# `g` produces words with `1` as their first symbol

g = smp.unique(g)
# `g` produces unique words

from itertools import islice
from tqdm import tqdm

n_samples = 100
g = islice(g, n_samples)
g = tqdm(g, total=n_samples)
sampled = list(g)
# sampled contains 100 words from free group and nice progress bar is shown.
```

```python3
from freegroup import sampling as smp, core

gs = [smp.NormalClosureGenerator([i], 3, smp.constant(10)) for i in range(1, 3 + 1)]
gs += [smp.NormalClosureGenerator([1, 2, 3], 3, smp.constant(5))]
g = smp.join(*gs)
# `g` produces list of words `w`, where w[0] from <x>, w[1] from <y>, ..., w[-1] from <xyz>

g = smp.shuffle(g)
g = smp.reduce(core.commutator, g)
# `g` produces words from symmetric commutator of <x>, <y>, <z>, <xyz>

g = map(core.normalize, g)
g = filter(lambda x: 0 < len(x), g)
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

g = smp.join(repeat(g, 5))
g = smp.subset(g)
g = smp.reduce(core.multiply, g)
# `g` produces words multiplications of several words from symmetric commutator
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

g = smp.join(repeat(g, 5))
g = smp.subset(g)
g = smp.append(repeat([1, 2, -1]), g)
g = smp.shuffle(g)
# `g` produces words like w_{i_1}..w_{i_k} u w_{j_1}...w_{j_s}, where u = [1, 2, -1], w_{i} from symmetric commutator, and `k` and `s` may be zeros. 
```


