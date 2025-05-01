import xml.etree.ElementTree as ET
from afd import Afd


class Xml:
    def getAlfabet(self) -> str:
        alfabet = ""
        for transition in self.transitions:
            char = transition.findtext("read") or ""
            if char != "" and char not in alfabet:
                alfabet += char
        return alfabet

    # return a list of dicts who has an id, bool for initial and bool for final
    def getStates(self) -> list:
        states = []
        seen = set()
        for state in self.states:

            if state.get("id") in seen:
                raise ValueError("Erro de estados no arquivo!")
            id = state.get("id")
            if id is None:
                raise ValueError(
                    "Erro ao tentar obter estados do documento | id is None"
                )
            seen.add(id)
            init = state.find("initial") is not None
            final = state.find("final") is not None

            states.append({"state": int(id), "init": init, "final": final})

        return states

    # return a list of dicts who has all transictions
    def getTransictions(self) -> list:
        transitions = []
        for transition in self.transitions:
            src = int(transition.findtext("from") or -1)
            dest = int(transition.findtext("to") or -1)
            simbol = str(transition.findtext("read") or "")

            if src >= 0 and dest >= 0 and simbol != "":
                transitions.append({"source": src, "destiny": dest, "simbol": simbol})
            else:
                raise ValueError("Erro de transições no arquivo")

        return transitions

    def createAFDXml(
        self,
        path: str,
        states: list,
        statesFinal: list,
        stateInitial: int,
        transictions: dict,
    ):
        x = 0
        y = 0
        aux = 0
        root = ET.Element("structure")
        ET.SubElement(root, "type").text = "fa"
        automaton = ET.SubElement(root, "automaton")

        for state in states:
            st = ET.SubElement(automaton, "state", id=str(state), name=("q" + str(aux)))
            ET.SubElement(st, "x").text = str(x)
            ET.SubElement(st, "y").text = str(y)
            if state in statesFinal:
                ET.SubElement(st, "final")
            if state == stateInitial:
                ET.SubElement(st, "initial")
            x += 50
            y += 50
            aux += 1

        for transiction in transictions:
            tr = ET.SubElement(automaton, "transition")
            ET.SubElement(tr, "from").text = str(transiction[0])
            ET.SubElement(tr, "to").text = str(transictions[transiction])
            ET.SubElement(tr, "read").text = str(transiction[1])

        tree = ET.ElementTree(root)
        tree.write(path, encoding="utf-8", xml_declaration=True)

    def __init__(self, path: str) -> None:
        tree = ET.parse(path)
        root = tree.getroot()
        automaton = root.find("automaton")

        if automaton is None:
            raise ValueError("automaton not found in archive!")

        self.states = automaton.findall("state")
        self.transitions = automaton.findall("transition")


def createAFDXML(path: str) -> Afd:
    arq = Xml(path)
    afd = Afd(arq.getAlfabet())
    temp = arq.getStates()
    for t in temp:
        afd.createState(t["state"], t["init"], t["final"])
    temp = arq.getTransictions()
    for t in temp:
        afd.createTransiction(int(t["source"]), int(t["destiny"]), str(t["simbol"]))

    return afd
