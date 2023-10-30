from typing import Callable, Optional, cast

from mypy.nodes import SymbolTableNode, MemberExpr
from mypy.plugin import Plugin, AttributeContext
from mypy.types import Type, Instance, TypeAliasType, TypedDictType


def plugin(version: str) -> type[Plugin]:
    return BagPlugin


def bag_attribute(ctx: AttributeContext) -> Type:
    info = ctx.type
    assert isinstance(info, Instance), type(info)
    attr_context = ctx.context
    assert isinstance(attr_context, MemberExpr), type(attr_context)
    attr_name = attr_context.name
    concrete_type = info.args[0]
    if isinstance(concrete_type, Instance):
        arg_info = concrete_type.type.names[attr_name]
        assert isinstance(arg_info, SymbolTableNode), type(arg_info)
        assert arg_info.type is not None
        attr_type = arg_info.type
    elif isinstance(concrete_type, TypeAliasType):
        assert concrete_type.alias is not None
        dict_type = concrete_type.alias.target
        assert isinstance(dict_type, TypedDictType)
        attr_type = dict_type.items[attr_name]
    else:
        raise TypeError(f"Don't know how to check {concrete_type}")
    return Instance(info.type, [attr_type])


class BagPlugin(Plugin):

    def get_attribute_hook(self, fullname: str) -> Optional[Callable[[AttributeContext], Type]]:
        if fullname.startswith('bag.Bag.'):
            attr = fullname.rsplit('.', 1)[-1]
            if not attr.startswith('_'):
                return bag_attribute
        return None
