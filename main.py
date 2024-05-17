import XMLtree
import xmp_parser

if __name__ == "__main__":
    parser = xmp_parser.XMLParser("test.xml")
    error = parser.try_to_close()
    if error is not None and len(error) > 0:
        print("Can't parse file, this argument(s) haven't closed: ", *error)
    parser.formating()
    parser.parse().draw_tree()
