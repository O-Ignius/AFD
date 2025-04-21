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
            raise ValueError("{} já faz parte do AFD!".format(id))
        self.states.add(id)  # adiciona estado
        if init:
            self.sInit = id
        if final:
            self.sFinal.add(id)

        return True

    def createTransiction(self, srce: int, dest: int, simbol: str):
        if srce not in self.states or dest not in self.states:
            raise ValueError("{} or {} não faz parte do AFD!".format(srce, dest))
        if len(simbol) != 1 or simbol not in self.alfabet:
            raise ValueError("Simbolo de transição incorreto: {}".format(simbol))
        self.transiction[(srce, simbol)] = dest
        return True

    def changsInitial(self, id: int):
        if id not in self.states:
            raise ValueError("id: {} não faz parte dos estados".format(id))
        self.sInit = id
        return True

    def changsFinal(self, id: int, final: bool):
        if id not in self.states:
            raise ValueError("id: {} não faz parte dos estados".format(id))
        if final:
            self.sFinal.add(id)
        else:
            self.sFinal.remove(id)

    def move(self, chain: str):
        for simbol in chain:
            if simbol not in self.alfabet:
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


def testAfdComplete(afd: Afd):
    tam = len(afd.alfabet) * len(afd.states)

    if tam == len(afd.transiction):
        return True
    else:
        raise ValueError("AFD Incompleto!")


# cria uma tabela [estado][(alfabeto)]
def tabelaDestinoAlfabeto(afd: Afd) -> list:
    dest = list()

    for estado in afd.states:
        destEstado = list()

        for letra in afd.alfabet:
            destEstado.append(afd.transiction[(estado, letra)])

        dest.append(destEstado)

    return dest


def searchTableComparison(tableComparison: dict, estado1: int, estado2: int):
    if tableComparison[(estado1, estado2)] is True:
        return True
    elif tableComparison[(estado1, estado2)] is False:
        return False
    else:
        return None


def searchIncongruency(
    tableAlfabet: list, estado1: int, estado2: int, tableEstadosFinais: list
):
    if (
        tableAlfabet[estado1][0] in tableEstadosFinais
        and tableAlfabet[estado2][0] not in tableEstadosFinais
    ) or (
        tableAlfabet[estado1][0] not in tableEstadosFinais
        and tableAlfabet[estado2][0] in tableEstadosFinais
    ):
        return False
    elif (
        tableAlfabet[estado1][1] in tableEstadosFinais
        and tableAlfabet[estado2][1] not in tableEstadosFinais
    ) or (
        tableAlfabet[estado1][1] not in tableEstadosFinais
        and tableAlfabet[estado2][1] in tableEstadosFinais
    ):
        return False
    else:
        return None


def comparaEstados(
    tableAlfabet: list,
    estado1: int,
    estado2: int,
    tableComparison: dict,
    nonCirc: list,
    tableEstadosFinais: list,
):
    if estado1 > estado2:
        aux = estado2
        estado2 = estado1
        estado1 = aux
    # impossivel tirar o proprio estado
    elif estado1 == estado2:
        return False

    comparison = searchTableComparison(tableComparison, estado1, estado2)

    # se estados são finais, verifica se ele loopa em si mesmo
    if estado1 in tableEstadosFinais and estado2 in tableEstadosFinais:
        if (
            tableAlfabet[estado1][0] == tableAlfabet[estado2][0]
            and tableAlfabet[estado1][1] == tableAlfabet[estado2][1]
        ) or (
            (
                tableAlfabet[estado1][0] == tableAlfabet[estado1][1]
                and tableAlfabet[estado1][0] == estado1
            )
            and (
                tableAlfabet[estado2][0] == tableAlfabet[estado2][1]
                and tableAlfabet[estado2][0] == estado2
            )
        ):
            return True
    if (estado1, estado2) not in nonCirc:
        nonCirc.append((estado1, estado2))
    else:
        return None

    # estado em aberto
    if comparison is None:
        # verifica se há alguma incongruência (estado final comparando com estado nao final)
        incongruency = searchIncongruency(
            tableAlfabet, estado1, estado2, tableEstadosFinais
        )
        if incongruency is not None and not incongruency:
            return False

        estadoBool1 = comparaEstados(
            tableAlfabet,
            tableAlfabet[estado1][0],
            tableAlfabet[estado1][1],
            tableComparison,
            nonCirc,
            tableEstadosFinais,
        )
        if estadoBool1 is None:
            return None

        estadoBool2 = comparaEstados(
            tableAlfabet,
            tableAlfabet[estado2][0],
            tableAlfabet[estado2][1],
            tableComparison,
            nonCirc,
            tableEstadosFinais,
        )
        if estadoBool2 is None:
            return None

        if estadoBool1 == estadoBool2 and estadoBool1 is True:
            return True
        else:
            return False
    elif comparison is True:
        aux = nonCirc[0]
        nonCirc.clear()
        nonCirc.append(aux)
        return True
    else:
        aux = nonCirc[0]
        nonCirc.clear()
        nonCirc.append(aux)
        return False


def mountTableEq(afd: Afd) -> dict:
    testAfdComplete(afd)

    estados = list(afd.states)
    equivalence = dict()
    tableAlfabet = tabelaDestinoAlfabeto(afd)
    final = bool
    stateOpen = list()

    print(tableAlfabet)

    # retira triviais e add None em não triviais
    for i in range(len(estados)):
        final = True if estados[i] in afd.sFinal else False
        for j in range(i + 1, len(estados)):

            if (final and estados[j] not in afd.sFinal) or (
                not final and estados[j] in afd.sFinal
            ):
                equivalence[(estados[i], estados[j])] = False
            else:
                equivalence[(estados[i], estados[j])] = None
                stateOpen.append((estados[i], estados[j]))

    # enquanto houver abertos verifica se é ou não equivalente
    while True:
        if not stateOpen:
            break

        for aberto in stateOpen:
            nonCirc = list()
            retorno = comparaEstados(
                tableAlfabet,
                aberto[0],
                aberto[1],
                equivalence,
                nonCirc,
                list(afd.sFinal),
            )
            if retorno is not None:
                equivalence[(aberto[0], aberto[1])] = retorno
                stateOpen.remove(aberto)

    print(equivalence)
    return equivalence


def multipAfd(afd1: Afd, afd2: Afd):
    alfabet = afd1.alfabet
    for letter in afd2.alfabet:
        if letter not in alfabet:
            alfabet += letter
    afdResult = Afd(alfabet)
    afdResult.createState(
        0,
        True,
    )
