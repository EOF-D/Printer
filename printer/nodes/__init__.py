from __future__ import annotations

from typing import Any
import os

from attrs import define, field

__all__ = ("Template",)


@define()
class Node:
    ...


@define(slots=True)
class Template(Node):
    lookup: dict[str, Any] = field(init=False)
    path: str = field()
    name: str = field()
    body: tuple[Node, ...] = field()

    def __attrs_post_init__(self) -> None:
        try:
            os.mkdir(os.path.join(self.path, self.name))
        except FileExistsError:
            pass

        self.lookup = {}
        self.path = os.path.join(self.path, self.name)


@define(slots=True)
class SetVar(Node):
    name: str = field()
    body: str = field()

    def append(self, parent: Template) -> None:
        parent.lookup[self.name] = self.body


@define(slots=True)
class Struct(Node):
    fields: tuple[str, ...] = field()

    def build(self, parent: Template) -> None:
        for field in self.fields:
            try:
                os.mkdir(os.path.join(parent.path, field))
            except FileExistsError:
                pass


@define(slots=True)
class Append(Node):
    directory: str = field()
    filename: str = field()
    to_append: tuple[str, ...] = field()
    filetype: str = field(default="py")

    def build(self, parent: Template) -> None:
        path = f"{parent.path}/{self.directory}/{self.filename}.{self.filetype}"

        with open(path, "a") as fp:
            for line in self.to_append:
                fp.write(parent.lookup[line])
