#!/usr/bin/env python

import argparse
import os
import platform
import re
import string
import sys
from enum import Enum
from typing import Optional

from py010parser import c_ast, parse_file

from fandango.converters.FandangoConverter import FandangoConverter


class BitfieldOrder(Enum):
    LeftToRight = 0
    RightToLeft = 1


class Endianness(Enum):
    LittleEndian = 0
    BigEndian = 1


class BTFandangoConverterVisitor(c_ast.NodeVisitor):
    def __init__(
        self,
        *,
        start_symbol: str = "<start>",
        use_regexes: bool = False,
        bitfield_order: BitfieldOrder = BitfieldOrder.LeftToRight,
        endianness: Endianness = Endianness.BigEndian,
    ):
        self.bitfield_order: BitfieldOrder = bitfield_order
        self.endianness: Endianness = endianness
        self.start_symbol = start_symbol
        self.use_regexes = use_regexes

        self.defs: dict[str, str] = {}
        self.forced_elems: list[str] = []
        self.forced_complements: list[str] = []
        self.forced_vars: list[str] = []
        self.seen: set[str] = set()
        self.context: list[str] = []
        self.constraints: list[str] = []
        self.not_handled: list[str] = []
        self.vars: dict[Optional[str], str] = {}
        self.renames: dict[str, str] = {}
        self.in_code = False

    def cond(self):
        return " and ".join(self.context)

    def _char(self, c):
        if c in string.printable:
            return c
        return f"\\x{ord(c):02x}"

    def char(self, c):
        if c in string.printable:
            return "b" + repr(c)
        return f"b'{self._char(c)}'"

    def not_char(self, c):
        if self.use_regexes:
            return f"br'[^{self._char(c)}]'"
        chars = []
        for i in range(256):
            if chr(i) != c:
                chars.append(self.char(chr(i)))
        return "(" + " | ".join(chars) + ")" + "  # not " + self.char(c)

    def not_short(self, value):
        low_byte = self._char(chr(ord(value) % 256))
        high_byte = self._char(chr(ord(value) // 256))
        return f"(/[^{low_byte}]./ | /[{low_byte}][^{high_byte}]/)"

    def spec(self, symbol: Optional[str] = None, indent=0) -> str:
        if symbol is None:
            symbol = self.start_symbol
        if indent == 0:
            self.seen = set()
        if symbol not in self.defs or symbol in self.seen:
            return ""
        self.seen.add(symbol)  # avoid infinite recursion

        expansion = self.defs[symbol]
        s = "  " * indent + f"{symbol} ::= {expansion}\n"
        nonterminals = re.findall(r"(<[^>]+>)", expansion)
        for nonterminal in nonterminals:
            s += self.spec(nonterminal, indent + 1)

        if indent == 0:
            if self.constraints:
                s += "\n"
            for constraint in self.constraints:
                s += f"where {constraint}\n"
            if self.not_handled:
                s += "\n"
            for not_handled in self.not_handled:
                s += f"# FIXME: {not_handled}\n"
        return s

    def visit(self, node):
        # print("Visiting", node.__class__.__name__)
        method_name = "visit_" + node.__class__.__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def add_def(self, base_name, members):
        for rename in self.renames.keys():
            members = members.replace(rename, self.renames[rename])

        i = 1
        name = base_name
        while name in self.defs:
            name = f"<{base_name[1:-1]}_{i}>"
            i += 1

        if name != base_name:  # record the rename
            self.renames[base_name] = name

        # print(f"Adding {name} ::= {members}")
        self.defs[name] = members

    def add_constraint(self, constraint):
        for rename in self.renames.keys():
            constraint = constraint.replace(rename, self.renames[rename])
        self.constraints.append(constraint)

    def generic_visit(self, node) -> str:
        print("Ignoring", node.__class__.__name__)
        for _, child in node.children():
            self.visit(child)
        return ""

    def generic_join(self, node, sep: str = " ") -> str:
        s = ""
        for _, child in node.children():
            member = self.visit(child)
            if s and member:
                s += sep
            if member:
                s += member
        return s

    def visit_ID(self, node: c_ast.ID) -> str:
        return node.name

    def visit_BinaryOp(self, node: c_ast.BinaryOp) -> str:
        left = self.visit(node.left)
        right = self.visit(node.right)
        return f"{left} {node.op} {right}"

    def visit_UnaryOp(self, node: c_ast.UnaryOp) -> str:
        expr = self.visit(node.expr)
        return f"{node.op}{expr}"

    def visit_ExprList(self, node: c_ast.ExprList) -> str:
        return self.generic_join(node)

    def visit_TypeDecl(self, node: c_ast.TypeDecl) -> str:
        return self.generic_join(node)

    def visit_FuncCall(self, node: c_ast.FuncCall) -> str:
        if self.in_code:
            return ""

        self.in_code = True
        name = self.visit(node.name)
        self.in_code = False

        if name == "BitfieldLeftToRight":
            self.bitfield_order = BitfieldOrder.LeftToRight
            return ""
        if name == "BitfieldRightToLeft":
            self.bitfield_order = BitfieldOrder.RightToLeft
            return ""

        if name == "LittleEndian":
            self.endianness = Endianness.LittleEndian
            return ""
        if name == "BigEndian":
            self.endianness = Endianness.BigEndian
            return ""

        if name == "RequiresVersion":
            return ""
        if name == "Warning":
            return ""

        self.not_handled.append(f"{name}()")
        return ""

    def visit_FuncDef(self, node: c_ast.FuncDef) -> str:
        if self.in_code:
            return ""

        self.in_code = True
        decl = self.visit(node.decl)
        self.not_handled.append(f"{decl}()")
        self.in_code = False
        return ""

    def visit_Compound(self, node: c_ast.Compound) -> str:
        return self.generic_join(node)

    def visit_StructRef(self, node: c_ast.StructRef) -> str:
        name = self.visit(node.name)
        field = self.visit(node.field)
        return f"<{name}>.<{field}>"

    def visit_FileAST(self, node: c_ast.FileAST) -> str:
        members = self.generic_join(node)
        self.add_def(self.start_symbol, members)
        return ""

    def visit_EmptyStatement(self, node: c_ast.EmptyStatement) -> str:
        return ""

    def visit_Typedef(self, node: c_ast.Typedef) -> str:
        members = self.generic_join(node)
        if node.name:
            self.add_def(f"<{node.name}>", members)
        return ""

    def visit_Struct(self, node: c_ast.Struct) -> str:
        members = []
        is_bitfield = True
        for _, child in node.children():
            if hasattr(child, "bitsize") and child.bitsize:
                bitsize = eval(self.visit(child.bitsize))
                if bitsize > 0:
                    continue

            is_bitfield = False
            break

        for _, child in node.children():
            value = None
            var: Optional[str] = None
            if self.forced_elems and self.forced_complements:
                value = self.forced_elems[0]
                self.forced_elems = self.forced_elems[1:]
                self.forced_complements = self.forced_complements[1:]
            elif self.forced_elems:
                value = self.forced_elems[0]
                self.forced_elems = self.forced_elems[1:]
            elif self.forced_complements:
                value = self.forced_complements[0]
                self.forced_complements = self.forced_complements[1:]

            if self.forced_vars:
                var = self.forced_vars[0]
                self.forced_vars = self.forced_vars[1:]

            elem = self.visit(child)
            if value:
                self.add_def(f"<{child.name}>", value)
                self.vars[var] = f"<{child.name}>"

            if elem:
                members.append(elem)

        if is_bitfield and self.bitfield_order == BitfieldOrder.RightToLeft:
            members.reverse()

        members_str = " ".join(members)

        # if is_bitfield:
        #     print(f"Bitfield {node.name} = {members_str}")
        # else:
        #     print(f"Struct {node.name} = {members_str}")

        if node.name:
            self.add_def(f"<{node.name}>", members_str)
            return f"<{node.name}>"

        return members_str

    def visit_Decl(self, node: c_ast.Decl):
        if self.in_code:
            return node.name

        if "local" in node.quals:
            # treat like an assignment
            if node.init:
                init = self.visit(node.init)
                self.vars[node.name] = node.init
                self.not_handled.append(f"{node.name} = {init}")
            return ""

        if node.bitsize:
            bitsize = eval(self.visit(node.bitsize))
            if bitsize == 1:
                m = "<bit>"
            else:
                m = f"<bit>{{{bitsize}}}"
        else:
            type_ = node.type
            if isinstance(type_, c_ast.ArrayDecl):
                array_decl: c_ast.ArrayDecl = type_
                type_name = self.visit(array_decl.type)
                dim = self.visit(array_decl.dim)
                if dim in self.vars and isinstance(self.vars[dim], str):
                    symbol = self.vars[dim]
                    constraint = f"len(<{node.name}>) == ord(str({symbol}))"
                    m = f"{type_name}*  # {constraint}; see below"
                    self.add_constraint(constraint)
                else:
                    try:
                        dim_n = int(dim)
                        m = f"{type_name}{{{dim_n}}}"
                    except ValueError:
                        m = f"{type_name}*  # FIXME: must be {{{dim}}}"
            else:
                m = self.visit(type_)

        self.add_def(f"<{node.name}>", m)
        return f"<{node.name}>"

    def visit_ArrayDecl(self, node: c_ast.ArrayDecl) -> str:
        type_ = self.visit(node.type)
        dim = self.visit(node.dim)
        try:
            dim_n = int(dim)
            return f"{type_}{{{dim_n}}}"
        except ValueError:
            pass
        return f"{type_}*  # FIXME: must be {{{dim}}}"

    def visit_Constant(self, node: c_ast.Constant) -> str:
        return f"{node.value}"

    def visit_Return(self, node: c_ast.Return) -> str:
        # We assume an early return, i.e. return -1
        self.add_constraint(f"not ({self.cond()})")
        return ""

    def visit_IdentifierType(self, node: c_ast.IdentifierType) -> str:
        name = "_".join(node.names)
        if self.in_code:
            return name
        else:
            return f"<{name}>"

    def visit_Assignment(self, node: c_ast.Assignment) -> str:
        lvalue = self.visit(node.lvalue)
        rvalue = self.visit(node.rvalue)
        self.vars[lvalue] = node.rvalue
        self.not_handled.append(f"{lvalue} = {rvalue}")
        return ""

    def force_elems(self, cond, iftrue=True):
        # Convert lookaheads into expected bytes
        # as in `if (ReadUShort(FTell()) == 0x0121) ...`
        if not isinstance(cond, c_ast.BinaryOp):
            return

        binary_op: c_ast.BinaryOp = cond
        complement = (
            binary_op.op == "==" and not iftrue or binary_op.op == "!=" and iftrue
        )

        left = binary_op.left
        right = binary_op.right
        var = None

        # Replace variable names by the last recorded expression
        if isinstance(left, c_ast.ID):
            left = self.vars.get(binary_op.left.name)
            if left is None:
                return
            var = binary_op.left.name
        elif isinstance(binary_op.right, c_ast.ID):
            right = self.vars.get(binary_op.right.name)
            if right is None:
                return
            var = binary_op.right.name

        # Identify the function call
        funccall: Optional[c_ast.FuncCall] = None
        if isinstance(left, c_ast.FuncCall):
            funccall = left
        elif isinstance(right, c_ast.FuncCall):
            funccall = right

        if not funccall:
            return

        # Identify the constant value
        value = None
        if isinstance(left, c_ast.Constant):
            value = eval(left.value)
        elif isinstance(right, c_ast.Constant):
            value = eval(right.value)

        if value is None:
            return
        if isinstance(value, int):
            value = chr(value)

        func = funccall.name
        if not isinstance(func, c_ast.ID):
            return

        name = func.name
        if name == "ReadUByte":
            if complement:
                self.forced_complements += [self.not_char(value)]
            else:
                self.forced_elems += [self.char(value)]
            if var:
                self.forced_vars += [var]

        elif name == "ReadUShort":
            if self.endianness == Endianness.BigEndian:
                next_bytes = [chr(ord(value) // 256), chr(ord(value) % 256)]
            else:  # LittleEndian
                next_bytes = [chr(ord(value) % 256), chr(ord(value) // 256)]

            if complement:
                # Too complex at this point; should be something like
                # self.forced_complements += [not_short(value)]
                # Here's a simpler alternative, only checking for one byte
                self.forced_complements += [self.not_char(next_bytes[0])]
            else:
                self.forced_elems += [
                    self.char(next_bytes[0]),
                    self.char(next_bytes[1]),
                ]

    def visit_While(self, node: c_ast.While | c_ast.For) -> str:
        if self.in_code:
            return ""

        cond = self.visit(node.cond)

        self.force_elems(node.cond, iftrue=True)
        self.context.append(cond)
        body = self.visit(node.stmt)
        self.context.pop()

        self.force_elems(node.cond, iftrue=False)
        if not body:
            return ""
        return f"({body})*"

    def visit_For(self, node: c_ast.For) -> str:
        return self.visit_While(node)

    def visit_If(self, node: c_ast.If) -> str:
        if self.in_code:
            return ""

        self.force_elems(node.cond, iftrue=True)

        cond = self.visit(node.cond)
        self.context.append(cond)
        iftrue = self.visit(node.iftrue)
        self.context.pop()

        if len(node.children()) <= 2:
            if not iftrue:
                return ""
            return f"{iftrue}?"

        self.force_elems(node.cond, iftrue=False)

        self.context.append("not " + cond)
        iffalse = self.visit(node.iffalse)
        self.context.pop()

        if iftrue and iffalse:
            return f"{iftrue} | {iffalse}"
        if iftrue:
            return iftrue
        if iffalse:
            return iffalse
        return ""


class BTFandangoConverter(FandangoConverter):
    """Convert a binary template to a Fandango specification."""

    def __init__(self, filename: str):
        super().__init__(filename)

        try:
            if platform.system() == "Darwin":
                ast = parse_file(filename, cpp_args="-xc++")
            else:
                ast = parse_file(filename)
            self.ast = ast
        finally:
            try:
                # The 010 parser leaves behind some temporary files
                os.remove("lextab.py")
                os.remove("yacctab.py")
            except FileNotFoundError:
                pass

    def to_fan(
        self,
        start_symbol: str = "<start>",
        use_regexes: bool = True,
        bitfield_order: BitfieldOrder = BitfieldOrder.LeftToRight,
        endianness: Endianness = Endianness.BigEndian,
    ) -> str:
        visitor = BTFandangoConverterVisitor(
            start_symbol=start_symbol,
            use_regexes=use_regexes,
            bitfield_order=bitfield_order,
            endianness=endianness,
        )
        visitor.visit(self.ast)
        header = f"""# Automatically generated from {self.filename!r}.
#
"""
        return header + visitor.spec()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert a binary template to a Fandango specification"
    )
    parser.add_argument(
        "--no-regexes",
        action="store_false",
        dest="use_regexes",
        default=True,
        help="do not use regexes",
    )
    parser.add_argument(
        "--endianness", choices=["little", "big"], help="set endianness"
    )
    parser.add_argument(
        "--bitfield-order",
        choices=["left-to-right", "right-to-left"],
        help="set bitfield order",
    )
    parser.add_argument(
        "filename", nargs="+", type=str, help=".bt binary template file"
    )

    args = parser.parse_args(sys.argv[1:])
    if args.endianness == "little":
        endianness = Endianness.LittleEndian
    else:
        endianness = Endianness.BigEndian
    if args.bitfield_order == "left-to-right":
        bitfield_order = BitfieldOrder.LeftToRight
    else:
        bitfield_order = BitfieldOrder.RightToLeft

    for filename in args.filename:
        converter = BTFandangoConverter(filename)
        fan = converter.to_fan(
            start_symbol="<start>",
            use_regexes=args.use_regexes,
            bitfield_order=bitfield_order,
            endianness=endianness,
        )
        print(fan)
