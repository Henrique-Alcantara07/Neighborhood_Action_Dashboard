# Fila para demandas aguardando analise (FIFO: First In, First Out)
fila_analise = []

# Pilha para registrar as ultimas atualizacoes de status (LIFO: Last In, First Out)
pilha_historico = []

# Dicionario indexado pelo Identificador para acesso rapido O(1)
dicionario_ocorrencias = {}

# Hierarquia: Bairro -> Categoria -> Lista de ocorrencias
hierarquia_bairros = {}

ocorrencias = [
    {"identificador": 1, "categoria": "iluminacao", "descricao": "Poste apagado na rua principal", "local": "Bairro Aurora", "data": "01/11/2026", "situacao": "Aberta"},
    {"identificador": 2, "categoria": "iluminacao", "descricao": "Falta de luz na passarela", "local": "Bairro Horizonte", "data": "03/11/2026", "situacao": "Concluida"},
    {"identificador": 3, "categoria": "acessibilidade", "descricao": "Piso tatil danificado", "local": "Bairro Aurora", "data": "05/11/2026", "situacao": "Em analise"},
    {"identificador": 4, "categoria": "limpeza", "descricao": "Lixo acumulado na esquina", "local": "Bairro Horizonte", "data": "07/11/2026", "situacao": "Concluida"},
    {"identificador": 5, "categoria": "limpeza", "descricao": "Entulho na calcada", "local": "Praca Central", "data": "09/11/2026", "situacao": "Em analise"},
    {"identificador": 6, "categoria": "manutencao", "descricao": "Portao do parque enferrujado", "local": "Bairro Horizonte", "data": "11/11/2026", "situacao": "Em analise"},
    {"identificador": 7, "categoria": "manutencao", "descricao": "Quadra com buracos", "local": "Centro Comunitario", "data": "12/11/2026", "situacao": "Concluida"},
    {"identificador": 8, "categoria": "manutencao", "descricao": "Banco quebrado na praca", "local": "Praca Central", "Data": "10/11/2026", "situacao": "Aberta"},    
    {"identificador": 9, "categoria": "limpeza", "descricao": "Mato alto no terreno publico", "local": "Bairro Aurora", "data": "08/11/2026", "situacao": "Aberta"},    
    {"identificador": 10, "categoria": "acessibilidade", "descricao": "Falta de vaga para cadeirantes", "local": "Centro Comunitario", "data": "06/11/2026", "situacao": "Aberta"},    
    {"identificador": 11, "categoria": "acessibilidade", "descricao": "Lampada piscando na praca", "local": "Praca Central", "data": "04/11/2026", "situacao": "Aberta"},    
    # Registro com campo ausente/inconsistente para testar a validacao logica (Requisito obrigatorio)
    {"identificador": 12, "categoria": "", "descricao": "Rampa sem acesso na calcada", "local": "Praca Central", "data": "02/11/2026", "situacao": "Em analise"}
]

CATEGORIAS = ["iluminacao", "acessibilidade", "limpeza", "manutencao"]

# Inicializacao das estruturas de dados auxiliares com base nos registros iniciais
for oc in ocorrencias:
    dicionario_ocorrencias[oc["identificador"]] = oc
    if oc["situacao"] in ["Aberta", "Em analise"]:
        fila_analise.append(oc["identificador"])
        
    bairro = oc["local"]
    cat = oc["categoria"] if oc["categoria"] else "Indefinida"
    if bairro not in hierarquia_bairros:
        hierarquia_bairros[bairro] = {}
    if cat not in hierarquia_bairros[bairro]:
        hierarquia_bairros[bairro][cat] = []
    hierarquia_bairros[bairro][cat].append(oc["identificador"])


def registrar_ocorrencia():
    while True:
        print("\n---- Cadastro de Ocorrencia ----")
        while True:
            categoria = input("Categoria (iluminacao, acessibilidade, limpeza, manutencao): ").strip().lower()
            if categoria in CATEGORIAS:
                break
            else:
                print("Opcao Invalida! Digite uma das categorias validas.")
        
        descricao = input("Descricao: ").strip()
        local = input("Local generico: ").strip()
        data = input("Data simulada (DD/MM/AAAA): ").strip()

        # Validacao com operadores logicos (AND / NOT / OR)
        if not categoria or not descricao or not local or not data:
            print("Por favor, complete todo o formulario!")
        else:
            identificador = len(ocorrencias) + 1
            nova_oc = {
                "identificador": identificador,
                "categoria": categoria,
                "descricao": descricao,
                "local": local,
                "data": data,
                "situacao": "Aberta"   
            }

            ocorrencias.append(nova_oc)
            dicionario_ocorrencias[identificador] = nova_oc
            fila_analise.append(identificador)
            
            print(f"Ocorrencia ID {identificador} registrada com sucesso!")

        continuar = input("Gostaria de cadastrar outra ocorrencia (y/n)? ").strip().lower()
        if continuar != "y":
            break


def mostrar_todas_ocorrencias():
    if not ocorrencias:
        print("Nenhuma ocorrencia cadastrada.")
        return

    print("\n--- Listagem Geral de Ocorrencias ---")
    for oc in ocorrencias:
        print("-" * 30)
        for chave, valor in oc.items():
            print(f"{chave}: {valor}")


def encontrar_ocorrencia():
    while True:
        entrada = input("Digite o numero do identificador da ocorrencia: ")
        if entrada.isdigit():
            id_busca = int(entrada)
            break
        else:
            print("Digite apenas numeros validos!")

    # Busca O(1) via dicionario
    if id_busca in dicionario_ocorrencias:
        oc = dicionario_ocorrencias[id_busca]
        print("\n--- Ocorrencia Encontrada ---")
        for chave, valor in oc.items():
            print(f"{chave}: {valor}")
    else:
        print("Ocorrencia nao encontrada no sistema.")


def filtrar_ocorrencias():
    print("\n--- Filtrar Ocorrencias ---")
    print("1 - Filtrar por Categoria")
    print("2 - Filtrar por Status")
    opcao_filtro = input("Escolha o tipo de filtro: ")

    if opcao_filtro == '1':
        cat = input("Digite a categoria (iluminacao, acessibilidade, limpeza ou manutencao): ").strip().lower()
        encontrados = 0
        for oc in ocorrencias:
            if oc["categoria"] == cat:
                print(f"ID: {oc['identificador']} | Descricao: {oc['descricao']} | Status: {oc['situacao']}") 
                encontrados += 1 
        if encontrados == 0:
            print("Nenhuma ocorrencia encontrada para esta categoria.")

    elif opcao_filtro == "2":
        status = input("Digite a situacao (Aberta, Em analise, Concluida): ").strip().capitalize()
        encontrados = 0
        for oc in ocorrencias:
            if oc["situacao"] == status:
                print(f"ID: {oc['identificador']} | Categoria: {oc['categoria']} | Descricao: {oc['descricao']}")
                encontrados += 1
        if encontrados == 0:
            print("Nenhuma ocorrencia encontrada para esta situacao.")
    else:
        print("Opcao de filtro invalida.")


def atualizar_situacao_ocorrencia():
    while True:
        entrada = input("Numero do Identificador da Ocorrencia: ")
        if entrada.isdigit():
            id_busca = int(entrada)
            break
        else: 
            print("Digite apenas numeros validos!")

    if id_busca in dicionario_ocorrencias:
        oc = dicionario_ocorrencias[id_busca]
        status_antigo = oc["situacao"]

        print(f"Ocorrencia {id_busca} encontrada. Status atual: {status_antigo}")
        nova_situacao = input("Nova situacao (Aberta / Em analise / Concluida): ").strip().capitalize()

        if nova_situacao in ["Aberta", "Em analise", "Concluida"]:
            if status_antigo == nova_situacao:
                print("A nova situacao e identica a atual. Nenhuma alteracao feita.")
                return

            oc["situacao"] = nova_situacao

            # 1. Empilha no historico (LIFO)
            registro_evento = f"ID {id_busca}: '{status_antigo}' -> '{nova_situacao}'"
            pilha_historico.append(registro_evento)

            # 2. Atualiza a Fila de Analise (FIFO)
            if nova_situacao == "Concluida" and id_busca in fila_analise:
                fila_analise.remove(id_busca)
            elif nova_situacao in ["Aberta", "Em analise"] and id_busca not in fila_analise:
                fila_analise.append(id_busca)

            print(f"Situacao atualizada com sucesso! Registrado na pilha de historico: {registro_evento}")
        else:
            print("Situacao invalida! Escolha entre: Aberta, Em analise ou Concluida.")
    else:
        print("Ocorrencia nao encontrada no sistema.")


def ver_resumo_indicadores():
    total_ocorrencias = len(ocorrencias)
    if total_ocorrencias == 0:
        print("Nenhuma ocorrencia cadastrada.")
        return

    inconsistentes = 0
    for oc in ocorrencias:
        if not oc["categoria"] or oc["categoria"].strip() == "":
            inconsistentes += 1
            print(f"[ALERTA DE VALIDACAO] Ocorrencia ID {oc['identificador']} possui Categoria ausente/inconsistente!")

    cont_situacao = {"Aberta": 0, "Em analise": 0, "Concluida": 0}
    cont_categoria = {cat: 0 for cat in CATEGORIAS}
    cont_categoria["Indefinida"] = 0

    matriz_resumo = {cat: [0, 0, 0] for cat in CATEGORIAS}
    matriz_resumo["Indefinida"] = [0, 0, 0]

    mapa_colunas = {"Aberta": 0, "Em analise": 1, "Concluida": 2}

    for oc in ocorrencias:
        sit = oc["situacao"]
        cat = oc["categoria"] if oc["categoria"] in CATEGORIAS else "Indefinida"

        if sit in cont_situacao:
            cont_situacao[sit] += 1
        if cat in cont_categoria:
            cont_categoria[cat] += 1

        if sit in mapa_colunas:
            col_idx = mapa_colunas[sit]
            matriz_resumo[cat][col_idx] += 1

    print("\n==========================================")
    print("      PAINEL DE INDICADORES (DASHBOARD)   ")
    print("==========================================")
    print(f"Total de ocorrencias cadastradas: {total_ocorrencias}")
    print(f"Registros com dados inconsistentes: {inconsistentes}\n")

    print("--- Indicadores por Situacao ---")
    for sit, qtd in cont_situacao.items():
        porcentagem = (qtd / total_ocorrencias) * 100
        print(f"• {sit}: {qtd} ({porcentagem:.1f}%)")

    print("\n--- Indicadores por Categoria ---")
    for cat, qtd in cont_categoria.items():
        porcentagem = (qtd / total_ocorrencias) * 100
        print(f"• {cat}: {qtd} ({porcentagem:.1f}%)")

    print("\n--- Matriz Sintese (Categoria x Situacao) ---")
    print(f"{'Categoria':<15} | {'Aberta':<8} | {'Em analise':<10} | {'Concluida':<9}")
    print("-" * 50)
    for cat, linha in matriz_resumo.items():
        print(f"{cat:<15} | {linha[0]:<8} | {linha[1]:<10} | {linha[2]:<9}")

    taxa_resolucao = (cont_situacao["Concluida"] / total_ocorrencias) * 100
    print(f"\n--- Indicadores Operacionais Extras ---")
    print(f"• Taxa de Resolucao Comunitaria: {taxa_resolucao:.1f}%")
    print(f"• Demandas Ativas na Fila de Analise: {len(fila_analise)}")
    print(f"• Total de Atualizacoes no Historico (Pilha): {len(pilha_historico)}")
    print("==========================================\n")


# Menu Principal
while True:
    print("\n--------- MENU PRINCIPAL ---------")
    print("1- Registrar uma Ocorrencia") 
    print("2- Mostrar todas as ocorrencias")
    print("3- Atualizar situacao de uma ocorrencia")
    print("4- Encontrar ocorrencia pelo numero")
    print("5- Filtrar ocorrencias")
    print("6- Ver resumo das ocorrencias (Dashboard)")
    print("0- Sair")

    opcao = input("\nEscolha uma opcao: ")

    if not opcao.isdigit():
        print("Digite apenas numeros validos!")
        continue

    opcao = int(opcao)

    if opcao == 1:
        registrar_ocorrencia()
    elif opcao == 2:
        mostrar_todas_ocorrencias()
    elif opcao == 3:
        atualizar_situacao_ocorrencia()
    elif opcao == 4:
        encontrar_ocorrencia()
    elif opcao == 5:
        filtrar_ocorrencias()
    elif opcao == 6:
        ver_resumo_indicadores()
    elif opcao == 0:
        print("Obrigado por usar o Neighborhood Action Dashboard!")
        print("Ate logo!")
        break
    else:
        print("Opcao invalida! Escolha um numero do menu.")