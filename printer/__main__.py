from __future__ import annotations

import argparse, os
import rich

from lark import Lark

from .parser import PrinterTransformer
from printer import __version__, __author__, __license__


def main() -> None:
    parser = argparse.ArgumentParser(prog="printer")
    parser.add_argument("file", type=argparse.FileType("r"))
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"Printer: {__version__} by {__author__} under {__license__}",
    )

    args = parser.parse_args()

    if args.file:
        path = os.path.dirname(__file__)

        with open(f"{path}/parser/grammar.lark", "r") as fp:
            parser = Lark(fp.read(), start="template", lexer="dynamic_complete")

        tree = PrinterTransformer().transform(parser.parse(args.file.read()))

        if args.debug:
            rich.inspect(tree)


if __name__ == "__main__":
    main()
