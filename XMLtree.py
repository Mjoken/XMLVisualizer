import matplotlib.pyplot as plt
import networkx as nx
import math

class XMLNode:
    def __init__(self, tag, attributes=None, text=None, depth=0):
        self.tag = tag
        self.closed = False
        self.depth = depth or 0
        self.attributes = attributes or {}
        self.text = text or ''
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __str__(self):
        return (f"XMLNode(tag={self.tag}, attributes={self.attributes}, text={self.text},"
                f" children={self.children}, depth={self.depth})")

    def print_node(self):
        print(self.__str__())

    def childrens_max_depth(self):
        maximum = 0
        for i in self.children:
            maximum = max(maximum, i.depth)
        return maximum


class XMLTree:
    def __init__(self):
        self.root = None
        self.plt = None

    # DFS add root
    def depth_add_node(self, node: XMLNode, curnode: XMLNode = None):
        if node is not None:
            if self.root is None:
                self.root = node
                return
            if curnode is None:
                curnode = self.root
            if ((curnode is self.root or node.depth > curnode.depth) and
                    (len(curnode.children) == 0 or node.depth <= curnode.childrens_max_depth())):
                curnode.add_child(node)
                return
            elif node.depth > curnode.depth:
                self.depth_add_node(node, curnode.children[-1])
            elif node.depth < curnode.depth:
                return

    def find_nodes(self, node, name, found_nodes):
        if node.tag == name:
            found_nodes.append(node)
        for child in node.children:
            self.find_nodes(child, name, found_nodes)

    def find_by_name(self, name):
        found_nodes = []
        self.find_nodes(self.root, name, found_nodes)
        return found_nodes

    def print_tree(self, node=None, indent=0):
        if not node:
            node = self.root
        if node:
            attributes_str = ', '.join([f"{key}={value}" for key, value in node.attributes.items()])
            text_str = node.text.strip()
            indent_str = '  ' * indent
            if text_str:
                print(indent_str + f"Element: {node.tag}, Attributes: {attributes_str}, Text: {text_str}")
            else:
                print(indent_str + f"Element: {node.tag}, Attributes: {attributes_str}")
            for child in node.children:
                self.print_tree(child, indent + 1)

    def to_networkx(self):
        G = nx.DiGraph()

        def add_nodes_edges(node):
            attributes_str = '\n'.join([f"{key}={value}" for key, value in node.attributes.items()])
            label = f"{node.tag}\n Attributes:\n {attributes_str} \n Text:\n {node.text}\n"
            G.add_node(node.tag, label=label)
            for child in node.children:
                G.add_edge(node.tag, child.tag)
                add_nodes_edges(child)

        add_nodes_edges(self.root)
        return G
    def get_plt(self):
        return self.plt
    # This function do things:)
    # We convert our tree to networkx graph and use layout
    def draw_tree(self):
        G = self.to_networkx()
        pos = nx.drawing.nx_agraph.graphviz_layout(G, prog="dot", root=self.root.tag)
        labels = nx.get_node_attributes(G, 'label')  # Получаем метки узлов
        node_sizes = [len(label) * 250 for label in labels.values()]
        nx.draw(G, pos, with_labels=True, node_size=node_sizes, node_color='skyblue', font_size=8, font_weight='bold',
                labels=labels, node_shape="s", linewidths=2, edge_color="gray", width=1.5, arrowsize=10)
        self.plt = plt
        plt.show()
