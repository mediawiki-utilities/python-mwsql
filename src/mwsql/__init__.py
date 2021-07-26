# This file is licensed under the terms of the MIT License.
# See the LICENSE file in the root of this repository
# for complete details.

# type: ignore

from .about import (
    __author__,
    __copyright__,
    __email__,
    __license__,
    __summary__,
    __title__,
    __url__,
    __version__,
)
from .dump import Dump
from .utils import head, load

__all__ = [
    "head",
    "load",
    "Dump",
    "__title__",
    "__summary__",
    "__url__",
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "__copyright__",
]
