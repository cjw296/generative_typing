from dataclasses import dataclass

from bag import Bag

bag_bad_init: Bag[int] = Bag[int](23.0)
bag_bad_var_type: Bag[int] = Bag[float](23.0)


@dataclass
class MyThing:
    foo: int
    bar: str


bag_dataclass: Bag[MyThing] = Bag[MyThing](MyThing(foo=1, bar='x'))
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
