class Afd:
    def __init__(self, alfabet: str) -> None:
        self.alfabet = alfabet
        self.sInit = None
        self.sFinal = set()
        self.states = set()
        self.transiction = dict()

    def __clean__(self):
        self.__err = False
        self.__errMessage = None
        self.__eNow = self.sInit

    def __error__(self):
        return (self.__err, self.__errMessage)

    def currentState(self):
        return self.__eNow

    def finalState(self, id):
        return id in self.sFinal

    def createState(self, id: int, init: bool = False, final: bool = False):
        if id in self.states:
            return False  # já faz parte do AFD
        self.states.add(id)  # adiciona estado
        if init:
            self.sInit = id
        if final:
            self.sFinal.add(id)

        return True

    def createTransiction(self, srce: int, dest: int, simbol: str):
        if not srce in self.states or not dest in self.states:
            return False
        if len(simbol) != 1 or not simbol in self.alfabet:
            return False
        self.transiction[(srce, simbol)] = dest
        return True

    def changsInitial(self, id: int):
        if not id in self.states:
            return False
        self.sInit = id
        return True

    def changsFinal(self, id: int, final: bool):
        if not id in self.states:
            return False
        if final:
            self.sFinal.add(id)
        else:
            self.sFinal.remove(id)

    def move(self, chain: str):
        for simbol in chain:
            if not simbol in self.alfabet:
                self.__err = True
                self.__errMessage = "Simbol doesn't exists in alfabet!"
            if (self.__eNow, simbol) in self.transiction.keys():
                newState = self.transiction[(self.__eNow, simbol)]
                self.__eNow = newState
            else:
                self.__err = True
                self.__errMessage = "Simbol doesn't exists in transictions!"

    def __str__(self) -> str:
        s = "AFD(E, A, T, i, F): \n"
        s += "\tE = { "
        for e in self.states:
            s += "{}, ".format(str(e))
        s += " }\n"
        s += "\tA = { "
        for a in self.alfabet:
            s += "'{}', ".format(a)
        s += " } \n"
        s += "\tT = { "
        for e, a in self.transiction.keys():
            d = self.transiction[(e, a)]
            s += "({}, '{}') --> {}, ".format(e, a, d)
        s += " }\n"
        s += "\ti = {}\n".format(self.sInit)
        s += "F = { "
        for e in self.sFinal:
            s += "{}, ".format(str(e))
        s += " }\n"

        return s
