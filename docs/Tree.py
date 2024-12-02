# Helper class to visualize trees
# Use as:
# tree = Tree('<foo>', Tree('"bar"'), Tree('<baz>', Tree('"qux"')))
# tree.visualize()

from graphviz import Digraph
from IPython.display import display_svg, display_png

class Tree:
    id_counter = 1
    dot = None

    def __init__(self, symbol, *children):
        self.symbol = symbol
        self._children = children

    def children(self):
        return self._children

    def visualize(self, title="Derivation Tree"):
        """Display as PNG. (PNG works with HTML and PDF books, SVG does not)"""
        # https://graphviz.org/doc/info/lang.html
        Tree.dot = Digraph(comment=title, format='png')
        Tree.dot.attr('node', shape='none', fontname='courier-bold', fontsize='18pt')
        Tree.dot.attr('graph', rankdir='TB', tooltip=title)
        Tree.dot.attr('edge', penwidth='2pt')
        Tree.id_counter = 1
        self._visualize()
        display_png(self.dot)

    def _visualize(self):
        name = f"node-{Tree.id_counter}"
        Tree.id_counter += 1
        label = self.symbol

        # https://graphviz.org/doc/info/colors.html
        if self.symbol.startswith('<'):
            color = 'firebrick'
        else:
            color = 'darkblue'

        label = label.replace('<', '\\<')
        label = label.replace('>', '\\>')
        Tree.dot.node(name, label, fontcolor=color)

        for child in self.children():
            child_name = child._visualize()
            Tree.dot.edge(name, child_name)

        return name
