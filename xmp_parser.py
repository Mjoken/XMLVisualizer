import re
from urllib.request import urlopen
import XMLtree


class XMLParser:

    def __init__(self, path):
        self.path = path
        self.file = None
        self.copy = self.file
        self.tree = None
        try:
            self.file = open(path, 'r', encoding='utf-8')
        except FileNotFoundError:
            print("File not found")

    def open_file(self, path):
        try:
            self.file = open(path, 'r', encoding='utf-8')
            self.copy = self.file
        except FileNotFoundError:
            print("File not found")

    def open_url(self, url):
        try:
            self.file = urlopen(url)
            self.copy = self.file
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
            strs_list = [(re.findall("<[^/?].+?>", i), i.index("<")) for i in lines][1:] # [^/?].+?>.+?</.+?>
            for elem in strs_list:
                for i in elem[0]:
                    if elem[0] and elem[0] != []:
                        match = re.findall(r"<([^?/].+?)[ >]", i)
                        attributes = re.findall(r"(\w+)\s*=\s*\"(\w*[^ >]+)\"", i)
                        text = re.findall(r">(.+?)<", i)
                        print(i, text)
                        for j in match:
                            if j and j != []:
                                node = XMLtree.XMLNode(j, dict(attributes),
                                                       " ".join(f"{word} " for word in text), elem[1])
                                node.print_node()
                                tree.depth_add_node(node)
            self.tree = tree
            tree.print_tree()
        return tree

    def try_to_close(self):
        open = (re.findall("<[^/?].+?>", *self.file.read()))
        closed = (re.findall("</.+?>", *self.file.read()))
        result = list(set(open) - set(closed))
        return result is []
