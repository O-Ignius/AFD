# Documentação de Funções do Módulo AFD

## Funções Auxiliares

- `__testAfdComplete(afd: Afd)`

> Testa se a quantia de transições é igual a multiplicação do tamanho do
> alfabeto vezes os estados

- `__conectivityAfd__(afd: Afd, estado: int, letra: str, alcancaveis: set,
estadoTestado: dict)`

> Verifica se, partindo de um estado(o inicial), quais estados são
> possiveis de alcançar

- `__resetAfd(afd: Afd)`

> Caso seja necessário, troca os estados, imagine que, ao retirar
> estados não conexos tenha ficado os estados, 1, 5 e 7, ele faz
> com que os estados sejam realocados para 1, 2 e 3 e refaz suas
> transições conforme necessário

- `__testAfdConexo(afd: Afd)`

> Partindo do estado inicial, verifica quais estados são alcancaveis
> retira os estados inalcancaveis e, se necessário, usa a \_\_resetAfd para
> consertar o afd resultante

- `__tabelaDestinoAlfabeto(afd: Afd) -> list`

> Cria uma tabela auxiliar que retorna uma lista de listas, onde
> lista\[x \(indo do 1° estado até o ultimo\)\] = lista de destinos para
> determinado estado e lista\[x\]\[y (indo da 1° 'letra' do alfabeto até
> a ultima)\] = estado destino

- `__searchTableComparison(tableComparison: dict, estado1: int, estado2: int)`

> Verifica se na tabela de comparação entre estados, a entrada referente ao
> estado 1 e ao estado 2 é algo diferente de **None**, se sim, retorna o valor
> caso não, retorna **None**

- `__searchIncongruency(tableAlfabet: list, estado1: int, estado2: int,
tableEstadosFinais: list)`

> Verifica se o estado 1 é final e o estado 2 não é final ou vice e versa
> se for, retorna **False** uma vez que um estado final nunca será igual a um
> não final

- `__comparaEstados(tableAlfabet: list, estado1: int, estado2: int,
tableComparison: dict, nonCirc: list, tableEstadosFinais: list)`

> É a função principal, onde os estado são comparados 2 a 2 e, usando
> as funções anteriores, verifica se os estados comparados serão ou não
> equivalentes, se os estados dependenderem entre si, ou seja, há dependencia
> circular, eles são equivalentes

## Tabela de Equivalência

- `mountTableEq(afd: Afd, comparing: bool) -> dict`

> É a função que monta a tabela de equivalência do Afd, usando as
> funções auxiliares anteriores, ela fica ciclando até que todos
> os pares de estados do afd tenham sido comparados

## Operações com AFD

- `verifyAFDEquivalence(afd1: Afd, afd2: Afd) -> bool`

> Ela dá um merge nos 2 Afd's, tanto no alfabeto quanto nos estados e transições
> simulando os 2 Afd's como 1, depois, cria a tabela de equivalência entre os estados,
> após isso, verifica se o estado inicial dos 2 Afd's são equivalentes, se sim,
> os Afd's são equivalentes

- `copyAfd(afd: Afd) -> Afd`

> Retorna um copy.deepcopy do afd

- `minimizeAfd(afd: Afd) -> Afd`

> Monta a tabela de comparação entre estados do Afd, remove os estados equivalentes
> e suas respectivas transições e realoca os estados que ficaram de acordo com
> a necessidade

- `get_new_transictions(afdResult: Afd, afd1: Afd, afd2: Afd, estado1: int,
estado2: int, letra: str, merge_states: dict, processed: list)`

> Passa por todos os estados do afd modificando suas transições após a multiplicação
> de 2 afds, usando como base um dicionario que indica qual os estados ficaram juntos

- `multipAfd(afd1: Afd, afd2: Afd)`

> Concatena as letras do alfabeto se necessário, cria os estados com base na quantia
> de estados dos 2 Afds, chama a função recursiva para criar as transições entre
> os estados do afd multiplicado

- `operacaoAfd(tipo: int, afd1: Afd, afd2: Optional[Afd] = None)`

> Separa qual operacão será feita no Afd, se for realizar algo que exija 2 Afds,
> multiplica-os e, variante a operação, seta os estados finais do Afd multiplicado
> ao final, verifica se é necessário realizar o \_\_resetAfd para reordenar os estados
