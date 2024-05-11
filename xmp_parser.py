import re
from urllib.request import urlopen
import XMLtree


class XMLParser:
    path = ""
    file = None

    def __init__(self, path):
        self.path = path
        try:
            self.file = open(path, 'r', encoding='utf-8')
        except FileNotFoundError:
            print("File not found")

    def open_file(self, path):
        try:
            self.file = open(path, 'r', encoding='utf-8')
        except FileNotFoundError:
            print("File not found")

    def open_url(self, url):
        try:
            self.file = urlopen(url)
        except ValueError:
            print("It's not correct url: ", url)

    def print_file(self):
        file = self.file
        if file:
            print(*file)

    def parse(self):
        tree = XMLtree.XMLTree()
        file = self.file
        if file:
            lines = file.readlines()
            strs_list = [(re.findall("<[^/?].+?>", i), i.index("<")) for i in lines][1:]
            for elem in strs_list:
                for i in elem[0]:
                    if elem[0] and elem[0] != []:
                        match = re.findall(r"<([^?/].+?)[ >]", i)
                        attributes = re.findall(r"(\w+)\s*=\s*\"(\w*[^ >]+)\"", i)
                        # print(attributes)
                        for j in match:
                            if j and j != []:
                                node = XMLtree.XMLNode(j, dict(attributes), None, elem[1])
                                # node.print_node()
                                tree.depth_add_node(node)
            # tree.print_tree()
        return tree
