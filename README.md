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



