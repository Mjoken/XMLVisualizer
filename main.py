import XMLtree
import xmp_parser
if __name__ == "__main__":
    parser = xmp_parser.XMLParser("test.xml")
    parser.parse().draw_tree()
