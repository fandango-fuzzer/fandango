# Helper class to visualize trees
# Use as:
# tree = Tree('<foo>', Tree('"bar"'), Tree('<baz>', Tree('"qux"')))
# tree.visualize()

from graphviz import Digraph
from IPython.display import display_svg, display_png


class Tree:
    id_counter = 1
    dot = None

    def __init__(self, symbol, *children, sources=[]):
        self.symbol = symbol
        self._children = children
        self._sources = sources

    def children(self):
        return self._children

    def sources(self):
        return self._sources

    def visualize(self, title="Derivation Tree"):
        """Display as PNG. (PNG works with HTML and PDF books, SVG does not)"""
        # https://graphviz.org/doc/info/lang.html
        Tree.dot = Digraph(comment=title, format="png")
        Tree.dot.attr("node", shape="none", fontname="courier-bold", fontsize="18pt")
        Tree.dot.attr("graph", rankdir="TB", tooltip=title)
        Tree.dot.attr("edge", penwidth="2pt")
        Tree.id_counter = 1
        self._visualize()
        display_png(self.dot)

    def _visualize(self):
        name = f"node-{Tree.id_counter}"
        Tree.id_counter += 1
        if str(self.symbol).startswith("<"):
            label = self.symbol
        else:
            label = repr(self.symbol)

        # https://graphviz.org/doc/info/colors.html
        # Colors checked against color vision deficiency
        if isinstance(self.symbol, int):
            color = "bisque4"
        elif isinstance(self.symbol, bytes):
            color = "darkblue"
        elif self.symbol.startswith("<"):
            color = "firebrick"
        else:
            color = "olivedrab4"

        label = label.replace("<", "\\<")
        label = label.replace(">", "\\>")
        assert Tree.dot is not None
        Tree.dot.node(name, label, fontcolor=color)

        for child in self.children():
            child_name = child._visualize()
            Tree.dot.edge(name, child_name)

        for source in self.sources():
            source_name = source._visualize()
            Tree.dot.edge(name, source_name, style="dotted", color="gray", dir="both")

        return name
