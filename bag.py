from operator import attrgetter, itemgetter
from typing import TypeVar, Generic, Any, Callable, Type, Optional, cast

T = TypeVar('T')


class Unset:
    pass


class Bag(Generic[T]):

    _value: T | Unset = Unset()
    _source: Callable[[], T]
    _op: Optional[Callable[[T], Any]] = None

    def __init__(self, value_or_source: T | Callable[[], T]) -> None:
        if callable(value_or_source):
            self._source = value_or_source
        else:
            self._value = value_or_source

    def get(self) -> T:
        if isinstance(self._value, Unset):
            self._value = self._source()
        value = self._value

        if self._op is not None:
            value = self._op(value)

        return value

    def __getattr__(self, name: str) -> 'Bag[Any]':
        bag = Bag[Any](self.get)
        bag._op = attrgetter(name)
        return bag

    def __getitem__(self, name: str) -> 'Bag[Any]':
        bag = Bag[Any](self.get)
        bag._op = itemgetter(name)
        return bag
