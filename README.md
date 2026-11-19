# Neighborhood Action Dashboard | CitizenTech

**FIAP · Ciência da Computação · Global Solution 2026.2 · Fase 4**

O **Neighborhood Action Dashboard** é um protótipo em Python que simula um painel comunitário de ocorrências. Ele permite registrar demandas de melhoria em bairros (iluminação, acessibilidade, limpeza e manutenção de espaços coletivos), consultar e filtrar os registros, atualizar a situação de cada demanda com histórico e acompanhar indicadores simples.

O programa roda no terminal, com menu interativo, e usa apenas Python básico. Não há bibliotecas externas, banco de dados, APIs nem integração com órgãos públicos. O projeto também inclui um **notebook Jupyter** com o mesmo código, explicações passo a passo e demonstrações prontas.

## Equipe


| Integrante | RM | Curso |
| --- | --- | --- |
| Henrique Floriano Alcantara | 575651 | Ciência da Computação |
| Nicolas França | 575343 | Ciência da Computação |
| Joao Pedro Candido Souza | 575884 | Ciência da Computação |
| Katia Regina Bispo | 576044 | Ciência da Computação |
| Yago Souza Araujo | 575343 | Ciência da Computação |

## Comunidade simulada, problema e público beneficiado

A comunidade é **fictícia**: quatro locais genéricos (Bairro Aurora, Bairro Horizonte, Praça Central e Centro Comunitário) que reúnem problemas comuns do dia a dia, como poste apagado, piso tátil danificado, entulho na calçada e quadra com buracos.

**Problema:** relatos dispersos dificultam enxergar quais demandas continuam abertas, quais categorias aparecem mais e onde os problemas se concentram. Os moradores também têm dificuldade de saber em que pé está cada solicitação.

**Público beneficiado:** moradores que registram e acompanham demandas, e grupos comunitários que precisam de uma visão organizada para conversar sobre prioridades. O sistema **não** promete atendimento de nenhuma demanda.

## Estrutura do repositório

```text
.
├── README.md
├── Sistema_NAD_Notebook.ipynb   # notebook com o mesmo código e explicações
├── src/
│   └── sistema.py               # programa principal
└── docs/
    └── uso_ia.md                # registro do uso de IA (a ser preenchido pela equipe)
```

## Como executar

É necessário apenas o **Python 3**. Na pasta do projeto, execute:

```bash
python src/sistema.py
```

Se o seu ambiente usa `python3`, troque o comando. Para o notebook, abra `Sistema_NAD_Notebook.ipynb` no Jupyter, VS Code ou Google Colab e execute as células em ordem. A última célula abre o mesmo menu interativo do terminal.

## O que o programa faz

| Opção | Função |
| --- | --- |
| 1 | Registrar uma ocorrência (com validação) |
| 2 | Mostrar todas as ocorrências em tabela |
| 3 | Atualizar a situação de uma ocorrência (com histórico) |
| 4 | Encontrar ocorrência pelo número |
| 5 | Filtrar por categoria, por situação ou pelos dois |
| 6 | Ver o painel de indicadores (dashboard) |
| 7 | Ver o histórico recente (pilha) |
| 8 | Ver a fila de análise (FIFO) |
| 9 | Ver a hierarquia bairro → categoria |
| 0 | Sair |

### Campos de uma ocorrência

| Campo | Obrigatório | Origem |
| --- | --- | --- |
| `identificador` | Sim | Gerado pelo sistema (único, sequencial) |
| `categoria` | Sim | `iluminacao`, `acessibilidade`, `limpeza` ou `manutencao` |
| `descricao` | Sim | Texto breve |
| `local` | Sim | Local genérico (sem endereço exato) |
| `data` | Sim | Data simulada de abertura, `DD/MM/AAAA` |
| `situacao` | Sim | Gerada como `Aberta` no cadastro |

### Situações e seus significados

| Situação | Significado |
| --- | --- |
| `Aberta` | Demanda registrada, ainda não examinada |
| `Em analise` | Demanda já examinada, aguardando solução |
| `Concluida` | Demanda resolvida |

### Dados simulados iniciais

Os registros são inicializados no próprio código (sem arquivo externo). O pacote contém:

- **12 ocorrências** distribuídas pelas quatro categorias e por quatro locais genéricos;
- **3 situações distintas**: 5 abertas, 4 em análise e 3 concluídas;
- **10 eventos de histórico** já empilhados (mudanças de status entre 04/11 e 14/11/2026);
- **1 registro inconsistente de propósito**: a ocorrência 12 está sem categoria e é detectada pela regra de validação, aparecendo no painel como `Indefinida`.

## Estruturas de dados e justificativas

| Estrutura | Variável | Por que foi escolhida |
| --- | --- | --- |
| **Lista** | `ocorrencias` | Guarda todos os registros em ordem de cadastro e permite percorrê-los em listagens, filtros e indicadores. |
| **Fila (FIFO)** | `fila_analise` | Demandas ativas (`Aberta` ou `Em analise`) seguem a ordem de registro: a mais antiga fica na frente. Quando uma demanda é concluída, sai da fila. |
| **Pilha (LIFO)** | `pilha_historico` | O evento mais recente fica no topo, então a consulta "últimas atualizações" lê a pilha de trás para frente. |
| **Dicionário** | `dicionario_ocorrencias` | Mapeia `identificador → ocorrência`, o que dá acesso direto por código sem percorrer a lista. |
| **Hierarquia** | `hierarquia_bairros` | Organiza `bairro → categoria → IDs`, mostrando de relance que tipos de problema aparecem em cada local. |
| **Matriz** | dentro de `calcular_indicadores()` | Lista de listas (linhas = categorias, colunas = situações) que resume as quantidades em uma tabela. |

Exemplo da hierarquia com os dados iniciais (saída da opção 9):

```text
Bairro Aurora
  +-- iluminacao: IDs [1]
  +-- acessibilidade: IDs [3]
  +-- limpeza: IDs [9]
Bairro Horizonte
  +-- iluminacao: IDs [2]
  +-- limpeza: IDs [4]
  +-- manutencao: IDs [6]
Praca Central
  +-- limpeza: IDs [5]
  +-- manutencao: IDs [8]
  +-- iluminacao: IDs [11]
  +-- Indefinida: IDs [12]
Centro Comunitario
  +-- manutencao: IDs [7]
  +-- acessibilidade: IDs [10]
```

> **Observação:** a fila mantém tanto `Aberta` quanto `Em analise`, pois ambas ainda dependem de uma solução. Se uma demanda volta de `Concluida` para outra situação, ela entra no **fim** da fila.

## Regras lógicas

### Cadastro e validação

A função `validar_ocorrencia()` aplica três verificações, nesta ordem:

1. algum campo obrigatório vazio → recusa: *"Por favor, complete todo o formulario!"*;
2. categoria fora da lista padronizada → recusa: *"Categoria invalida!"*;
3. data fora do formato `DD/MM/AAAA` → recusa: *"Data invalida!"*.

**Expressão booleana documentada:**

```python
if not categoria or not descricao or not local or not data:
    # recusa o cadastro
```

Cada `not x` é verdadeiro quando o campo está vazio (string vazia é falsa em Python). Com `or`, basta **um** campo vazio para a expressão inteira ser verdadeira e o cadastro ser bloqueado. Por isso, mesmo com categoria, descrição e local preenchidos, deixar a data em branco produz a mensagem de formulário incompleto. A condição equivale, por De Morgan, a exigir que **todos** os campos estejam preenchidos.

### Onde cada operador lógico aparece

| Operador | Condição no código | Efeito |
| --- | --- | --- |
| `not` + `or` | `not categoria or not descricao or not local or not data` | Bloqueia cadastro com campo vazio |
| `and` | `nova_situacao == "Concluida" and id_busca in fila_analise` | Só remove da fila se a demanda estiver nela |
| `and` | `nova_situacao in ["Aberta", "Em analise"] and id_busca not in fila_analise` | Só reinsere na fila se ela ainda não estiver |
| `and` | `passa_categoria and passa_situacao` | No filtro combinado, o registro precisa atender às duas condições |
| `or` | `categoria is None or oc["categoria"] == categoria` | Sem filtro de categoria, todos passam |
| `and` | `continuar != "y" and continuar != "s"` | Só encerra o cadastro se a resposta não for "y" nem "s" |

### Atualização de situação

A função `atualizar_situacao()` verifica, em ordem:

| Condição | Resposta |
| --- | --- |
| Identificador não existe no dicionário | "Ocorrencia nao encontrada no sistema." |
| Situação fora de `Aberta`, `Em analise`, `Concluida` | "Situacao invalida!" |
| Nova situação igual à atual | "Nenhuma alteracao feita." |
| Demais casos | Atualiza, empilha o evento no histórico e ajusta a fila |

### Consulta e filtro

- **Busca por código:** usa `id in dicionario_ocorrencias`; se o código não existe, informa que não foi encontrado.
- **Filtro:** por categoria, por situação ou pelas duas juntas. Entradas inválidas geram mensagem clara, e filtros sem resultado informam que nada foi encontrado.
- **Menu:** entradas que não são números são recusadas com `isdigit()` antes de qualquer ação.

## Indicadores

Os indicadores são calculados com laços e operações simples em `calcular_indicadores()` e exibidos na opção 6, com a regra de cálculo impressa junto dos resultados.

| Indicador | Fórmula |
| --- | --- |
| Proporção por situação | `quantidade da situação / total × 100` |
| Proporção por categoria | `quantidade da categoria / total × 100` |
| Matriz categoria × situação | contagem por par (categoria, situação) |
| Taxa de resolução | `concluídas / total × 100` |
| Pendências | `Aberta + Em analise` |
| Tempo médio simulado das pendências | `soma(dias desde a abertura) / pendências` |

O tempo é medido a partir de uma **data de referência simulada** (`DATA_REFERENCIA = "15/11/2026"`). A conversão usa meses de 30 dias, o que é uma aproximação suficiente para a simulação.

### Resultado com os dados iniciais

```text
Total de ocorrencias cadastradas: 12
Registros com dados inconsistentes: 1

--- Indicadores por Situacao ---
- Aberta: 5 (41.7%)
- Em analise: 4 (33.3%)
- Concluida: 3 (25.0%)

--- Indicadores por Categoria ---
- iluminacao: 3 (25.0%)
- acessibilidade: 2 (16.7%)
- limpeza: 3 (25.0%)
- manutencao: 3 (25.0%)
- Indefinida: 1 (8.3%)

--- Matriz Sintese (Categoria x Situacao) ---
Categoria       | Aberta   | Em analise | Concluida
--------------------------------------------------
iluminacao      | 2        | 0          | 1
acessibilidade  | 1        | 1          | 0
limpeza         | 1        | 1          | 1
manutencao      | 1        | 1          | 1
Indefinida      | 0        | 1          | 0

--- Indicadores Operacionais Extras ---
- Taxa de resolucao = concluidas / total x 100 = 25.0%
- Pendencias (Aberta + Em analise): 9
- Tempo medio simulado das pendencias: 8.8 dias
- Atualizacoes no historico (pilha): 10
```

### Interpretação

Com este conjunto simulado, as demandas se distribuem de forma equilibrada entre iluminação, limpeza e manutenção (3 cada), com acessibilidade logo atrás (2). **Três de cada quatro demandas (75%) ainda estão pendentes**, e a taxa de resolução é de 25%. Em média, as pendências estão abertas há cerca de 9 dias simulados. Por local, a Praça Central concentra 4 das 9 pendências, e nenhuma de suas demandas está concluída. Os números sugerem que o foco de atenção da comunidade simulada seria a Praça Central e a redução do acúmulo de demandas abertas. Como os dados são fictícios e poucos, isso é uma leitura da simulação, não uma conclusão sobre uma comunidade real.

## Exemplo de uso

**Cadastro** (opção 1):

```text
Categoria (iluminacao, acessibilidade, limpeza, manutencao): iluminacao
Descricao: Poste queimado na quadra
Local generico: Praca Central
Data simulada (DD/MM/AAAA): 14/11/2026
Ocorrencia ID 13 registrada com sucesso!
```

**Cadastro inválido** (campo vazio):

```text
Por favor, complete todo o formulario!
```

**Alteração de status** (opção 3):

```text
Ocorrencia 13 encontrada. Status atual: Aberta
Nova situacao (Aberta / Em analise / Concluida): em analise
Situacao atualizada! Historico: [15/11/2026] ID 13: 'Aberta' -> 'Em analise'
```

**Consulta por código** (opção 4, ID 99): `Ocorrencia nao encontrada no sistema.`

**Filtro combinado** (opção 5 → 3, iluminação e Aberta):

```text
ID: 1 | Categoria: iluminacao | Local: Bairro Aurora | Status: Aberta | Poste apagado na rua principal
ID: 11 | Categoria: iluminacao | Local: Praca Central | Status: Aberta | Lampada piscando na praca
Total encontrado: 2
```

**Histórico recente** (opção 7, topo da pilha primeiro):

```text
[15/11/2026] ID 13: 'Aberta' -> 'Em analise'
[14/11/2026] ID 12: 'Aberta' -> 'Em analise'
[14/11/2026] ID 7: 'Em analise' -> 'Concluida'
[13/11/2026] ID 7: 'Aberta' -> 'Em analise'
[12/11/2026] ID 6: 'Aberta' -> 'Em analise'
```

**Saída** (opção 0):

```text
Obrigado por usar o Neighborhood Action Dashboard!
Ate logo!
```

Todas as saídas acima foram geradas executando o próprio programa.

## Acessibilidade, inclusão e privacidade

- **Privacidade:** todos os dados são fictícios e o programa não pede nome, telefone, e-mail nem endereço. O campo de local é genérico, e o cadastro exibe um aviso para não informar dados pessoais. Nada é gravado em arquivo: ao fechar o programa, tudo volta ao estado inicial.
- **Acessibilidade:** a interface de texto é compatível com leitores de tela, porque não depende de cor, imagem ou mouse. As mensagens são curtas e indicam o que fazer para corrigir um erro. O texto do código não usa acentos para evitar problemas de codificação em terminais diferentes.
- **Inclusão:** a categoria **acessibilidade** é tratada como tema de primeira classe (piso tátil, vaga para cadeirantes, rampas). Os termos usados nas telas são simples, e o significado de cada situação está documentado.
- **Responsabilidade:** o sistema não promete atendimento, não prioriza demandas automaticamente e deixa claro que os números descrevem dados simulados.

## Vídeo de apresentação

[Link do vídeo no YouTube (não listado)](https://youtube.com/) — _substituir pelo link real antes da entrega._

## Conclusões, limitações e aprendizados

**Conclusões.** O protótipo cumpre o ciclo completo: cadastrar com validação, organizar em estruturas adequadas, consultar, atualizar com histórico e resumir em indicadores. A divisão do código entre **lógica** (calcula e retorna), **interface** (mostra e lê) e **menu** (controla o fluxo) facilitou os testes, inclusive no notebook, onde as funções são chamadas sem digitar nada.

**Limitações.**

- Os dados não são salvos: o programa não mantém histórico entre execuções.
- O conjunto inicial é pequeno e fictício, então os indicadores servem como demonstração.
- A data é tratada como texto validado por formato. Não verifica, por exemplo, se o dia 31 existe no mês, e o tempo usa meses de 30 dias.
- Não há controle de usuários nem de quem alterou cada status.
- O identificador é sequencial (`tamanho da lista + 1`), o que funciona porque o sistema não permite excluir registros.

**Aprendizados e evoluções possíveis.** A equipe praticou a escolha da estrutura certa para cada finalidade (a mesma ocorrência aparece na lista, no dicionário, na fila e na hierarquia, cada uma servindo a uma consulta diferente). Como evolução, seria possível salvar os registros em arquivo CSV, validar datas de forma mais completa, registrar a data real de conclusão para medir o tempo entre abertura e fechamento, e permitir "desfazer" a última alteração usando a pilha.

## Uso de inteligência artificial

O uso de IA e a forma como os resultados foram verificados devem ser registrados em [`docs/uso_ia.md`](./docs/uso_ia.md), conforme o enunciado.

---

**Projeto acadêmico em equipe · FIAP · Ciência da Computação · Global Solution 2026.2 · CitizenTech**
