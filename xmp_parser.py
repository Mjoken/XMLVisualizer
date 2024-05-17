import re
from urllib.request import urlopen
import XMLtree


def text_spliter(text: str, delta):
    i = 0
    res = ""
    # delta = 20
    #while text.find('  '):
        #text.replace('  ', ' ')
    while i < len(text):
        res += text[i:i+delta]+'\n'
        i += delta
    return res


class XMLParser:

    def __init__(self, path):
        self.path = path
        self.file = None
        self.tree = None
        try:
            self.file = open(path, 'r', encoding='utf-8')
        except FileNotFoundError:
            print("File not found")

    def open_file(self, path):
        try:
            self.file = open(path, 'r', encoding='utf-8')
        except FileNotFoundError:
            print("File not found")

    def read_file(self):
        try:
            return open(self.path, 'r', encoding='utf-8')
        except FileNotFoundError:
            print("File not found")
    def write_file(self):
        try:
            return open(self.path, 'w', encoding='utf-8')
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

    def formating(self):
        file = self.read_file()
        text = file.read()
        file.close()
        separator = -1
        i = 0
        text = list(text)
        print(text)
        while i < len(text):
            if text[i] == '\n':
                separator = i
                i += 1
                while text[i] == ' ':
                    i += 1
                if text[i] != '<' and separator >= 0:
                    for j in range(separator, i):
                        text[j] = ''
                    text[separator] = ' '
            i += 1
        #text = str(text)
        text = ''.join(text)
        file = self.write_file()
        file.write(text)
        file.close()

    def parse(self):
        tree = XMLtree.XMLTree()
        file = self.file
        if file:
            lines = file.readlines()
            strs_list = [(re.findall(r"<[^/?].+?>.*?[<\n]", i), i.index("<")) for i in lines][1:]
            # print(strs_list)
            for elem in strs_list:
                for i in elem[0]:
                    if elem[0] and elem[0] != []:
                        match = re.findall(r"<([^?/].+?)[ >]", i)
                        attributes = re.findall(r"(\w+)\s*=\s*\"(\w*[^ >]+)\"", i)
                        text = re.findall(r">(.+?)<", i)
                        # print(i, text)
                        for j in match:
                            if j and j != []:
                                node = XMLtree.XMLNode(j, dict(attributes),
                                                       text_spliter(" ".join(f"{word} " for word in text), len(j))
                                                       , elem[1])
                                # node.print_node()
                                tree.depth_add_node(node)
            self.tree = tree
            # tree.print_tree()
        return tree

    def try_to_close(self):
        copy = self.read_file().read()
        open_tags = (re.findall(r"<([^?/].+?)[ >]", copy))
        closed_tags = (re.findall(r"</(.+?)>", copy))
        result = list(set(open_tags) - set(closed_tags))
        return result
