import copy
from typing import Optional


class Afd:
    def __init__(self, alfabet: str) -> None:
        self.alfabet = alfabet
        self.sInit = -1
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

    def deleteState(self, state: int):
        if state == self.sInit:
            raise ValueError(
                "Possível problema derivado de se retirar estado inicial padrão!"
            )
        self.states.remove(state)
        if state in self.sFinal:
            self.sFinal.remove(state)

        self.deleteStateTransictions(state)

        return True

    def createTransiction(self, srce: int, dest: int, simbol: str):
        if srce not in self.states or dest not in self.states:
            raise ValueError("{} or {} não faz parte do AFD!".format(srce, dest))
        if len(simbol) != 1 or simbol not in self.alfabet:
            raise ValueError("Simbolo de transição incorreto: {}".format(simbol))
        self.transiction[(srce, simbol)] = dest
        return True

    def deleteStateTransictions(self, state: int):
        delet = list()

        for transict in self.transiction:
            if transict[0] == state:
                delet.append(transict)

        for d in delet:
            del self.transiction[d]

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


def __testAfdComplete(afd: Afd):
    tam = len(afd.alfabet) * len(afd.states)

    if tam == len(afd.transiction):
        return True
    else:
        raise ValueError("AFD Incompleto!")


def __conectivityAfd__(
    afd: Afd, estado: int, letra: str, alcancaveis: set, estadoTestado: dict
):
    dest = afd.transiction[(estado, letra)]
    alcancaveis.add(dest)

    # se alcançáveis for igual ao estado ele é conexo
    if len(alcancaveis) == len(afd.states):
        return True

    # se estado testado[dest existe, soma mais 1 nele]
    if dest in estadoTestado.keys():
        if (estadoTestado[dest] >= 2) or (dest == estado):
            return
        estadoTestado[dest] = estadoTestado[dest] + 1
    # caso contrário, crie-o
    else:
        estadoTestado[dest] = 1

    for letter in afd.alfabet:
        __conectivityAfd__(afd, dest, letter, alcancaveis, estadoTestado)
    return


def __testAfdConexo(afd: Afd):
    alcancaveis = set()
    alcancaveis.add(afd.sInit)
    estadoTestado = dict()
    estadoTestado[afd.sInit] = 1

    for letra in afd.alfabet:
        __conectivityAfd__(afd, afd.sInit, letra, alcancaveis, estadoTestado)

    del_state = list()

    for estado in afd.states:
        # se o estado não foi alcancavel a partir do estado inicial passando por todas as opções possiveis, retire-o
        if estado not in alcancaveis:
            del_state.append(estado)

    for estado in del_state:
        afd.deleteState(estado)

    return


# cria uma tabela [estado][(alfabeto)]
def __tabelaDestinoAlfabeto(afd: Afd) -> list:
    dest = list()

    for estado in afd.states:
        destEstado = list()

        for letra in afd.alfabet:
            destEstado.append(afd.transiction[(estado, letra)])

        dest.append(destEstado)

    return dest


def __searchTableComparison(tableComparison: dict, estado1: int, estado2: int):
    if tableComparison[(estado1, estado2)] is True:
        return True
    elif tableComparison[(estado1, estado2)] is False:
        return False
    else:
        return None


def __searchIncongruency(
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


def __comparaEstados(
    tableAlfabet: list,
    estado1: int,
    estado2: int,
    tableComparison: dict,
    nonCirc: list,
    tableEstadosFinais: list,
):
    # somente para sempre usar estado 1 < 2 na recursão
    if estado1 > estado2:
        aux = estado2
        estado2 = estado1
        estado1 = aux
    # impossivel tirar o proprio estado
    elif estado1 == estado2:
        return True

    # compara os estados na tabela de equivalencia
    comparison = __searchTableComparison(tableComparison, estado1, estado2)

    # verifica dependencia circular: estado1 -> estado2 -> estado1
    if (estado1, estado2) not in nonCirc:
        nonCirc.append((estado1, estado2))
    # se há dependencia circular os estados são equivalentes
    else:
        return True

    # estado em aberto
    if comparison is None:
        # verifica se há alguma incongruência (estado final comparando com estado nao final)
        incongruency = __searchIncongruency(
            tableAlfabet, estado1, estado2, tableEstadosFinais
        )

        # se não há incongruência e a tabela de comparação retornou False
        if incongruency is not None and not incongruency:
            return False

        # verifica para as saidas da 1° letra do alfabeto se são ou não equivalentes
        estadoBool1 = __comparaEstados(
            tableAlfabet,
            tableAlfabet[estado1][0],
            tableAlfabet[estado2][0],
            tableComparison,
            nonCirc,
            tableEstadosFinais,
        )
        # se retorno é None, estado depende de outro estado para definir
        if estadoBool1 is None:
            return None

        estadoBool2 = __comparaEstados(
            tableAlfabet,
            tableAlfabet[estado1][1],
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


# afd = finite automate, comparing = boolean True if comparing "2" automates ("2" because its a merge between 2 automates, but, the function only accept 1 automate)
def mountTableEq(afd: Afd, comparing: bool) -> dict:
    if not comparing:
        # verifica se AFD é conexo, se houver desconexões, retire-as
        __testAfdConexo(afd)
        # verifica se o afd é completo, ou seja, a quantia de transições é igual a tamanho do alfabeto * quantia de estados
        __testAfdComplete(afd)

    estados = list(afd.states)
    equivalence = dict()
    tableAlfabet = __tabelaDestinoAlfabeto(afd)
    final = bool
    stateOpen = list()

    # retira triviais (comparação entre um estado final e não final) e add None em não triviais
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
            retorno = __comparaEstados(
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

    return equivalence


# return True if AFDs are equivalent or False cause not
def verifyAFDEquivalence(afd1: Afd, afd2: Afd) -> bool:
    if afd1.alfabet != afd2.alfabet:
        return False
    merged = Afd(afd1.alfabet)

    idStates = 0
    sInitials = list()

    # cria estados primeiro afd
    for estado in afd1.states:
        if estado == afd1.sInit:
            sInitials.append(idStates)
        if estado in afd1.sFinal:
            merged.createState(idStates, False, True)
        else:
            merged.createState(idStates, False, False)

        idStates += 1

    # salva primeiro id do 2° afd
    diff = idStates

    for transicao in afd1.transiction:
        merged.createTransiction(
            transicao[0], afd1.transiction[transicao], transicao[1]
        )

    # cria estados segundo afd
    for estado in afd2.states:
        if estado == afd2.sInit:
            sInitials.append(idStates)
        if estado in afd2.sFinal:
            merged.createState(idStates, False, True)
        else:
            merged.createState(idStates, False, False)

        idStates += 1

    for transicao in afd1.transiction:
        merged.createTransiction(
            (transicao[0] + diff),
            (afd1.transiction[transicao] + diff),
            transicao[1],
        )

    # Monta tabela de equivalencia de estados
    tabela = mountTableEq(merged, True)

    # verifica se 1° estado de ambos são equivalentes
    if tabela[(sInitials[0], sInitials[1])]:
        return True
    else:
        return False


def copyAfd(afd: Afd) -> Afd:
    return copy.deepcopy(afd)


def minimizeAfd(afd: Afd) -> Afd:
    min = copyAfd(afd)

    equiv = mountTableEq(afd, False)
    duplicates = list()
    stateEq = set()

    # cria lista de lista para salvar a relação de estados
    for i in range(len(afd.states)):
        duplicates.append(list())

    # itera por todos os estados
    for i in range(len(afd.states)):
        for j in range(i + 1, len(afd.states)):
            # se estado for equivalente
            if equiv[(i, j)] is True:
                # evita remover o inicial
                if j == afd.sInit:
                    if i not in duplicates:
                        stateEq.add(i)
                        duplicates[j].append(i)
                        duplicates[i].append(None)
                        duplicates[i].append(j)
                else:
                    if j not in duplicates:
                        # add estado em um set para salvar quais estados são equivalentes no geral
                        stateEq.add(j)
                        # append no estado equivalente na posição:
                        # se 0 equivalente a 1: duplicates[0].append(1)
                        duplicates[i].append(j)
                        # append None em duplicates[1] para definir que o estado 1 é equivalente a um outro estado e será retirado
                        duplicates[j].append(None)
                        # append o estado equivalente, ou seja, append 0 em duplicates[1]
                        duplicates[j].append(i)

    aux = 0
    # Retira transições que vão para estados equivalentes
    for duplicata in duplicates:
        # se há duplicatas remova-as do AFD
        if duplicata:
            for letra in afd.alfabet:
                # verifica se é necessário modificar a transição
                if afd.transiction[(aux, letra)] in stateEq:
                    # verificação extra para nao modificar estados que serão retirados
                    if None not in duplicata:
                        for estado in duplicata:
                            # se o estado a ser retirado loopava em si mesmo, faz com que o que fique tambem loop em si mesmo
                            if afd.transiction[(estado, letra)] == estado:
                                min.transiction[(aux, letra)] = aux
                                break
                            # caso não, veja se este aponte para algum estado que não será retirado
                            elif afd.transiction[(estado, letra)] not in stateEq:
                                min.transiction[(aux, letra)] = afd.transiction[
                                    (estado, letra)
                                ]
                                break
                            # se ele apontar para um estado que será retirado, reaponte para o estado que será mantido
                            else:
                                # pega o valor da saida do estado e coloca ele na 1° posição referente ao estado a ser mantido
                                # levando em conta o padrão onde: 1 e 3 são equivalentes, o de menor id será mantido caso o mesmo nao seja o inicial, se for, troca
                                # como equivalente[2] "Que se refere ao estado 3" na 1° posição: equivalente[2][0] == None refere-se que o mesmo deve ser retirado,
                                # portanto, o proximo valor será referente ao estado que será mantido: equivalente[2][1] == 1
                                min.transiction[(aux, letra)] = duplicates[
                                    afd.transiction[(aux, letra)]
                                ][1]
        # se não há duplicata o estado se mantem, mas pode estar com saidas que apontam para estados futuramente inexistentes
        else:
            for letra in afd.alfabet:
                # se aponta para um estado que será retirado, realoque
                point = afd.transiction[(aux, letra)]
                if point in stateEq:
                    min.transiction[(aux, letra)] = duplicates[point][1]

        aux += 1

    # deleta estados equivalentes e suas transições
    stateEq = list(stateEq)
    for eq in stateEq:
        min.deleteState(eq)

    return min


def get_new_transictions(
    afdResult: Afd,
    afd1: Afd,
    afd2: Afd,
    estado1: int,
    estado2: int,
    letra: str,
    merge_states: dict,
    processed: list,
):
    # verifica se todos os estados foram processados
    if (estado1, estado2, letra) in processed or len(processed) == (
        len(afdResult.states) * len(afdResult.alfabet)
    ):
        return

    transiction1 = afd1.transiction[estado1, letra]
    transiction2 = afd2.transiction[estado2, letra]
    # cria transição para o afd resultante
    afdResult.createTransiction(
        merge_states[estado1, estado2], merge_states[transiction1, transiction2], letra
    )
    # adiciona a transição nos estados já processados
    processed.append((estado1, estado2, letra))
    for letter in afdResult.alfabet:
        get_new_transictions(
            afdResult,
            afd1,
            afd2,
            transiction1,
            transiction2,
            letter,
            merge_states,
            processed,
        )


# retorna o AFD multiplicado e quais estados são referentes aquele estado
def multipAfd(afd1: Afd, afd2: Afd):
    # concatena alfabeto:
    alfabet = afd1.alfabet
    for letter in afd2.alfabet:
        if letter not in alfabet:
            alfabet += letter

    afdResult = Afd(alfabet)
    # cria estado inicial
    afdResult.createState(0, True)

    merge_states = dict()
    merge_states[(afd1.sInit, afd2.sInit)] = 0

    # separa os estados definindo qual se fundiu com qual
    count = 1
    for states1 in afd1.states:
        for states2 in afd2.states:
            if states1 != afd1.sInit or states2 != afd2.sInit:
                merge_states[(states1, states2)] = count
                afdResult.createState(count)
                count += 1

    # lista de transições (srce, dest, simbol)
    processed = list()
    for letter in alfabet:
        get_new_transictions(
            afdResult,
            afd1,
            afd2,
            afd1.sInit,
            afd2.sInit,
            letter,
            merge_states,
            processed,
        )

    return afdResult, merge_states


def operacaoAfd(tipo: int, afd1: Afd, afd2: Optional[Afd] = None):
    """
    tipo - 1: União, 2: intersecção, 3: Complemento, 4: Diferença
    afd1 - Não opcional, necessário para alguma operação
    afd2 - Opicional, necessário para a maioria das operações
    -> retorna um afd referente a operação, ou False em caso de mal uso
    """

    if afd2 is None and tipo != 3:
        print("Passe um segundo afd para realizar interseção, união ou diferença!")
        return False

    # realiza o complemento de um afd passado por parametro e o retorna
    elif afd2 is None and tipo == 3:
        afdResult = copy.deepcopy(afd1)
        finais = afdResult.sFinal
        for estado in afdResult.states:
            if estado in finais:
                afdResult.changsFinal(estado, False)
            else:
                afdResult.changsFinal(estado, True)

        return afdResult
    # se ambos forem passados verifica qual das operacao foi escolhida
    elif afd2 is not None:
        if tipo == 3:
            print("Erro de uso! Passe somente um AFD!")
            return False

        afdResult, merge_states = multipAfd(afd1, afd2)
        if tipo == 1:
            for estado in merge_states:
                if estado[0] in afd1.sFinal or estado[1] in afd2.sFinal:
                    afdResult.changsFinal(merge_states[estado], True)
        elif tipo == 2:
            for estado in merge_states:
                if estado[0] in afd1.sFinal and estado[1] in afd2.sFinal:
                    afdResult.changsFinal(merge_states[estado], True)
        elif tipo == 4:
            for estado in merge_states:
                if (estado[0] in afd1.sFinal) and (estado[1] not in afd2.sFinal):
                    afdResult.changsFinal(merge_states[estado], True)

        afdResult = minimizeAfd(afdResult)
        return afdResult
