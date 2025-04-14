import xml.etree.ElementTree as ET
from afd import Afd


class Xml:
    def __init__(self, path: str) -> None:
        self.tree = ET.parse(path)
        self.root = self.tree.getroot()
        self.read()
        self.alfabet = ""
        self.automaton = Afd(self.alfabet)

    def read(self):
        for child in self.root:
            if child.tag == "state":
                id = child.attrib.get("id")
                if not isinstance(id, str):
                    raise ValueError("Value id is not string!")
                id = int(id)
                initial = child.find("initial") is not None
                final = child.find("final") is not None
                self.automaton.createState(id, initial, final)
            elif child.tag == "transition":
                char = child.find("read")
                if char is not None and char not in self.alfabet:
                    self.alfabet += char
