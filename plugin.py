from typing import Callable, Optional, cast

from mypy.nodes import SymbolTableNode, MemberExpr
from mypy.plugin import Plugin, AttributeContext
from mypy.types import Type, Instance


def plugin(version: str) -> type[Plugin]:
    return BagPlugin


def bag_attribute(ctx: AttributeContext) -> Type:
    info = ctx.type
    assert isinstance(info, Instance), type(info)
    attr_context = ctx.context
    assert isinstance(attr_context, MemberExpr), type(attr_context)
    concrete_type = info.args[0]
    assert isinstance(concrete_type, Instance), type(concrete_type)
    arg_info = concrete_type.type.names[attr_context.name]
    assert isinstance(arg_info, SymbolTableNode), type(arg_info)
    assert arg_info.type is not None
    return Instance(info.type, [arg_info.type])


class BagPlugin(Plugin):

    def get_attribute_hook(self, fullname: str) -> Optional[Callable[[AttributeContext], Type]]:
        if fullname.startswith('bag.Bag.'):
            attr = fullname.rsplit('.', 1)[-1]
            if not attr.startswith('_'):
                return bag_attribute
        return None
