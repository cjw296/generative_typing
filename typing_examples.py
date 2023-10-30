from dataclasses import dataclass
from typing import TypedDict

from bag import Bag

bag_bad_init: Bag[int] = Bag[int](23.0)
bag_bad_var_type: Bag[int] = Bag[float](23.0)


@dataclass
class MyDataClass:
    foo: int
    bar: str


bag_dataclass: Bag[MyDataClass] = Bag[MyDataClass](MyDataClass(foo=1, bar='x'))
# Happy path examples
bag_dataclass_foo: Bag[int] = bag_dataclass.foo
foo: int = bag_dataclass.foo.get()
foo_: int = bag_dataclass_foo.get()
bag_dataclass_bar: Bag[str] = bag_dataclass.bar
bar: str = bag_dataclass.bar.get()
bar_: str = bag_dataclass_bar.get()
# unhappy
foo_bad: str = bag_dataclass.foo.get()
bar_bad: int = bag_dataclass.bar.get()


class MyTypedDict(TypedDict):
    foo: int
    bar: str

bag_typeddict: Bag[MyTypedDict] = Bag[MyTypedDict]({'foo': 1, 'bar': 'x'})
# Happy path examples
bag_typeddict_foo: Bag[int] = bag_typeddict.foo
dfoo: int = bag_typeddict.foo.get()
dfoo_: int = bag_typeddict_foo.get()
bag_typeddict_bar: Bag[str] = bag_typeddict.bar
dbar: str = bag_typeddict.bar.get()
dbar_: str = bag_typeddict_bar.get()
# unhappy
dfoo_bad: str = bag_typeddict.foo.get()
dbar_bad: int = bag_typeddict.bar.get()
bag_typeddict_bad: Bag[MyTypedDict] = Bag[MyTypedDict]({'foo': 'x', 'bar': 1})
