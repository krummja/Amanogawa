from __future__ import annotations
from typing import *
if TYPE_CHECKING:
    pass

from collections.abc import KeysView
from collections.abc import ValuesView
from collections.abc import ItemsView


K = TypeVar("K")
V = TypeVar("V")


class Iteritems(Generic[K, V], Protocol):
    def __call__(self, data: dict[K, V]) -> Iterable[tuple[K, V]]:
        ...

class SortedIteritems(Generic[K, V], Protocol):
    def __call__(self, data: dict[K, V]) -> list[tuple[K, V]]:
        ...


def sorted_iteritems(data: dict[K, V]) -> list[tuple[K, V]]:
    return sorted(data.items())

def iteritems(data: dict[K, V]) -> Iterable[tuple[K, V]]:
    return iter(data.items())

def iterkeys(data: dict[K, Any]) -> Iterable[K]:
    return iter(data.keys())


class ShortKeyError(KeyError):
    """Raised when a given key is a prefix of a longer key"""


_SENTINEL = object()


class Node:

    def __init__(self) -> None:
        self.children = {}
        self.value = _SENTINEL

    def iterate(self, path, shallow, iteritems):
        node = self
        stack = []

        while True:
            if node.value is not _SENTINEL:
                yield path, node.value

            if not (shallow or node.value is _SENTINEL) and node.children:
                stack.append(iter(iteritems(node.children)))
                path.append(None)

            while True:
                try:
                    step, node = next(stack[-1])
                    path[-1] = step
                    break
                except StopIteration:
                    stack.pop()
                    path.pop()
                except IndexError:
                    return

    def traverse(self, node_factory, path_conv, path, iteritems):
        def children():
            """Recursively traverses all children of node."""
            for step, node in iteritems(self.children):
                yield node.traverse(node_factory, path_conv, path + [step], iteritems)

        args = [path_conv, tuple(path), children()]
        if self.value is not _SENTINEL:
            args.append(self.value)
        return node_factory(*args)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Node):
            return False

        a, b = self, other
        stack = []
        while True:
            if a.value != b.value or len(a.children) != len(b.children):
                return False
            if a.children:
                stack.append((iteritems(a.children), b.children))

            while True:
                try:
                    key, a = next(stack[-1][0])
                    b = stack[-1][-1].get(key)
                    if b is None:
                        return False
                    break
                except StopIteration:
                    stack.pop()
                except IndexError:
                    return True

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __bool__(self) -> bool:
        return bool(self.value is not _SENTINEL or self.children)

    def __nonzero__(self) -> bool:
        return self.__bool__()

    def __hash__(self) -> None:
        return


NONE_PAIR = type(
    "NonePair",
    (tuple,),
    {
        "__nonzero__": lambda _: False,
        "__bool__": lambda _: False,
        "__slots__": (),
    }
)((None, None))


class Trie(MutableMapping[K, V]):

    def __init__(self, *args, **kwargs):
        self._root = Node()
        self._sorted = False
        self.update(*args, **kwargs)

    def iteritems(self) -> Iteritems[K, V] | SortedIteritems[K, V]:
        return sorted_iteritems if self._sorted else iteritems

    def enable_sorting(self, enabled: bool = True) -> None:
        self._sorted = enabled

    def clear(self) -> None:
        self._root = Node()

    def update(self, *args: tuple[Trie], **kwargs) -> None:
        if len(args) > 1:
            raise ValueError(
                f"`update()` takes at most one positional argument, {len(args)} given."
            )

        super().update(*args, **kwargs)
