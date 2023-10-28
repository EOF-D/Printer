from __future__ import annotations

from textwrap import dedent

from lark import Transformer, v_args
from ..nodes import Template, Node, SetVar, Struct, Append

__all__ = ("PrinterTransformer",)


@v_args(inline=True)
class PrinterTransformer(Transformer):
    CNAME = lambda _, token: token.value
    STRING = lambda _, token: token.value[1:-1]
    ANY = lambda _, token: dedent(token.value)

    def set_var(self, name: str, value: str):
        return SetVar(name=name, body=value[1:])

    def stmt(self, body: Node):
        return body

    def struct(self, *directories: str) -> Struct:
        return Struct(fields=directories)

    def append(self, filetype: str, directory: str, filename: str, *to_append: str):
        return Append(
            filetype=filetype,
            directory=directory,
            filename=filename,
            to_append=to_append,
        )

    def template(self, name: str, path: str, *body: Node):
        template = Template(name=name, path=path, body=body)

        for node in template.body:
            if isinstance(node, SetVar):
                node.append(template)

            elif isinstance(node, Struct | Append):
                node.build(template)

        return template
