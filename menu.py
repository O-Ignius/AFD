from afd import Afd, operacaoAfd, minimizeAfd, verifyAFDEquivalence
from wXml import export_afd_xml, generate_afd_using_xml


def import_arquivo(afd: Afd, operacao: str):
    print("\tAFD " + operacao + " :")

    while True:
        print("Deseja importar para um arquivo XML o resultado?")
        op = input("1- Sim   2- Não")

        if op == 1:
            arq = input("Digite o nome do arquivo: ")
            if ".xml" not in arq:
                arq += ".xml"
            export_afd_xml(afd, arq)
        elif op == 2:
            print(afd)
            break
        else:
            print("Opção inválida!")


def menu_operacoes():
    while True:
        print("\n=== MENU - Operações entre AFDs ===")
        print("1. Importar AFDs")
        print("2. União")
        print("3. Interseção")
        print("4. Complemento (de um único AFD)")
        print("5. Diferença")
        print("0. Voltar ao menu principal")

        escolha = input("Escolha uma opção: ")
        afd = None
        afd2 = None

        if int(escolha) < 0 or int(escolha) > 5:
            print("Opção inválida. Tente novamente.")
        elif escolha == "1":
            path = input("Digite o nome do arquivo XML que contenha o 1° AFD: ")
            afd = generate_afd_using_xml(path)
            path = input("Digite o nome do arquivo XML que contenha o 2° AFD: ")
            afd2 = generate_afd_using_xml(path)
        elif escolha == "0":
            break
        elif afd is not None:
            if escolha == "2":
                result = operacaoAfd(1, afd, afd2)
                import_arquivo(result, "após união")
            elif escolha == "3":
                result = operacaoAfd(2, afd, afd2)
                import_arquivo(result, "após intersecção")
            elif escolha == "4":
                result = operacaoAfd(3, afd)
                import_arquivo(result, "após complemento")
            elif escolha == "5":
                result = operacaoAfd(4, afd, afd2)
                import_arquivo(result, "após diferença")
        else:
            print("Importe no mínimo 1 AFD")


def menu_principal():
    while True:
        print("\n=== MENU - Operações com AFD ===")
        print("1. Importar AFD de arquivo .xml")
        print("2. Minimizar AFD")
        print("3. Calcular equivalência entre 2 AFDs")
        print("4. Operações entre AFDs")
        print("0. Sair")

        escolha = input("Escolha uma opção: ")
        afd = None

        if escolha == "1":
            path = input("Digite o nome do arquivo XML que contenha o AFD: ")
            afd = generate_afd_using_xml(path)
            import_arquivo(afd, "após importação")
        elif escolha == "2":
            if afd is not None:
                minimized = minimizeAfd(afd)
                import_arquivo(minimized, "após minimização")
            else:
                print("Primeiro importe um AFD!")
        elif escolha == "3":
            if afd is not None:
                op = input("Deseja usar o afd importado anteriormente?  1- Sim  2- Não")
                if op == 1:
                    path = input("Digite o nome do arquivo XML que contenha o 2° AFD: ")
                    afd2 = generate_afd_using_xml(path)
                else:
                    path = input("Digite o nome do arquivo XML que contenha o 1° AFD: ")
                    afd = generate_afd_using_xml(path)
                    path = input("Digite o nome do arquivo XML que contenha o 2° AFD: ")
                    afd2 = generate_afd_using_xml(path)

            else:
                path = input("Digite o nome do arquivo XML que contenha o 1° AFD: ")
                afd = generate_afd_using_xml(path)
                path = input("Digite o nome do arquivo XML que contenha o 2° AFD: ")
                afd2 = generate_afd_using_xml(path)

                if verifyAFDEquivalence(afd, afd2) is True:
                    print("Os AFD's importados são equivalentes!")
                else:
                    print("Os AFD's importados não são equivalentes")

        elif escolha == "4":
            menu_operacoes()
        elif escolha == "0":
            print("Encerrando o programa.")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu_principal()
