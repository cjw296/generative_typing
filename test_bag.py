from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict

from testfixtures import compare

from bag import Bag
from mypy import api as mypy_api

MYPY_CONFIG = Path(__file__).parent / 'mypy.ini'


def test_simple() -> None:
    bag: Bag[int] = Bag[int](23)
    value: int = bag.get()
    compare(value, expected=23)


def test_dataclass() -> None:

    @dataclass
    class MyThing:
        foo: int
        bar: str

    bag: Bag[MyThing] = Bag[MyThing](MyThing(foo=1, bar='x'))
    foo = bag.foo
    foo_value: int = foo.get()
    compare(foo_value, expected=1)
    bar = bag.bar
    bar_value: str = bar.get()
    compare(bar_value, expected='x')


def test_typed_dict() -> None:

    class MyThing(TypedDict):
        foo: int
        bar: str

    bag: Bag[MyThing] = Bag[MyThing]({'foo': 1, 'bar': 'x'})
    foo = bag['foo']
    foo_value: int = foo.get()
    compare(foo_value, expected=1)
    bar = bag['bar']
    bar_value: str = bar.get()
    compare(bar_value, expected='x')


def test_typing() -> None:
    stdout, stderr, exitcode = mypy_api.run([
        "--config-file", str(MYPY_CONFIG), 'bag.py', 'test_bag.py', 'plugin.py'
    ])
    compare(exitcode, expected=0, suffix=stdout)


def test_typing_examples() -> None:
    result = mypy_api.run([
        '--show-traceback', "--config-file", str(MYPY_CONFIG), 'typing_examples.py'
    ])
    stdout = '\n'.join((
        'typing_examples.py:6: error: Argument 1 to "Bag" has incompatible type "float"; expected "int | Callable[[], int]"  [arg-type]',
        'typing_examples.py:7: error: Incompatible types in assignment (expression has type "Bag[float]", variable has type "Bag[int]")  [assignment]',
        'typing_examples.py:25: error: Incompatible types in assignment (expression has type "int", variable has type "str")  [assignment]',
        'typing_examples.py:26: error: Incompatible types in assignment (expression has type "str", variable has type "int")  [assignment]',
        'typing_examples.py:42: error: Incompatible types in assignment (expression has type "int", variable has type "str")  [assignment]',
        'typing_examples.py:43: error: Incompatible types in assignment (expression has type "str", variable has type "int")  [assignment]',
        'typing_examples.py:44: error: Incompatible types (expression has type "str", TypedDict item "foo" has type "int")  [typeddict-item]',
        'typing_examples.py:44: error: Incompatible types (expression has type "int", TypedDict item "bar" has type "str")  [typeddict-item]',
        'Found 8 errors in 1 file (checked 1 source file)',
    )) + '\n'
    stderr = ''
    exitcode = 1
    compare(result, expected=(stdout, stderr, exitcode))
