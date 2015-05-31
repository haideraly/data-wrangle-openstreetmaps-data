import xml.etree.ElementTree as ET
import pprint

def count_tags(filename):
        tag_dict = {}
        it_tree = ET.iterparse(filename)
        for i in it_tree:
            if i[1].tag.strip() not in tag_dict:
                tag_dict[i[1].tag.strip()] = 1
            else:
                tag_dict[i[1].tag.strip()] += 1
        return tag_dict