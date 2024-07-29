import pandas as pd  #Importando a biblioteca pandas
import numpy as np #Importando numpy
import itertools #Importa uma biblioteca que ajuda a criar tabelas
import os #importa para limpar tela
import operator #importa para negar uma tabela interia

# Funções 
def define_variaveis()  :                                                                                    
  """
    Sumário: define quantas e quais são as variáveis, criando também a 
    tabela-verdade geral e depois separando em uma lista a tabela-verdade de 
    cada variável
    
    Params: N/D
    
    Retorno: Mostra para o usuário a tabela-verdade criada 
  """
  os.system("clear")

  # Try exception para trativa de erro caso o usuário digite algo dif de número
  while True:
    try: # Se digitado um int sai do loop
      print("-------------------- Definir Variáveis --------------------\n")
      qtdevar = int(input("Informe quantas variáveis você deseja usar: "))
      break
    except: # Se não continua no loop
      print("\nOps! Não entendi o que você quis dizer, por favor tente novamente\n")


  # Pede para o usuário digitar o nome de cada variável
  for i in range(qtdevar):
    confirmacaoInt = 0
    while confirmacaoInt != 1:
      var = input("\nInforme o nome da "+ str(i+1) +"ª variável: ")
      if var == '' or var == ' ':
        print("\nOps! Não foi informado o nome da variável!")
        confirmacaoInt = 1
      vars.append(var)
      confirmacaoInt = 1


  # Cria tabela-verdade das variáveis
  valTabelaVars = list(itertools.product([False, True],repeat=len(vars)))

  # Cria a lista dos valores de cada variável separada
  for z in range(len(vars)):
    tabelaIsoladaVars.append([])

  for variavel in valTabelaVars:
    j = 0
    for valor in variavel:
      tabelaIsoladaVars[j].append(valor)
      j += 1

  # Converte a lista para DataFrame, forma mais acessível para o usuário visualizá-la
  tabelaVerdadeVariaveis = pd.DataFrame(np.transpose(tabelaIsoladaVars), columns=vars)
  print("\nTabela-verdade das variaveis informadas:\n" + tabelaVerdadeVariaveis.to_string()) 

  print("\nAs variáveis foram definidas com sucesso! Aperte 'Enter' para continuar")
  confirmacaoUsuario = input('').split(" ")[0]

def calculo_senteca(variaveis, descricaoTabela, tabelaVars): 
  """
    Sumário:  Método (Função), que realiza o calculo da sentença, tendo como base de início
    as variáveis definidas e seus nomes no método (definir_variaveis), de escolha de MENU 1
    é necessário que o usuário tenha feito o método (definir_variaveis) para dar continuidade no programa.

    Params: variaveis, descricaoTabela, tabelavars.
    
    Retorno:  Tabela verdade com nova coluna de resultados da sentença já calculados.
    Incluindo arvore gerada de resultados TRUE-FALSE
  """
  
  tabelaResultado = tabelaVars
  confirmacaoStr = ''
  while confirmacaoStr != 's':
    # Limpa a tela
    os.system("clear")
    while True:
      print("-------------------- Cálculo de Sentença --------------------")
      print("\nOperadores:\n  OU: +;\n  E: *;\n  negação: !;\n  condicional(se ... então): ->;\n  implicação lógica: =>;\n  ()\nVariáveis:")
      for i in variaveis:
        if i == variaveis[-1]: print(f"  {i}")
        else: print(f"  {i};")

      sentenca = input("\nDescreva a sentença que deseja calcular utilizando os operadores e as variáveis acima: ")
      if sentenca == '' or sentenca == ' ': 
        print("\nOps! Não foi encontrado uma sentença, por favor tente novamente")
        confirmacaoUsuario = input('').split(" ")[0]
      else: break
    
    confirmacaoStr = input("\nA sentença foi digitada corretamente? (s - sim e n - não): ")
  
  tokens = []
  for i in range(0, len(sentenca)):
    confirmacaoNum = 0
    char=sentenca[i]

    if char == '(': 
      for j in range(0, len(sentenca)):
        if confirmacaoNum == 0 and char == ')':
          tokens.append(list())
    elif char == ')': tokens.append(['PARENTESES','FECHA',None,None])
    elif char == '+': tokens.append(['OPERADOR','OU',None,None])
    elif char == '*': tokens.append(['OPERADOR','E',None,None])
    elif char == '-': tokens.append(['OPERADOR','CONDICIONAL',None,None])
    elif char == '=': tokens.append(['OPERADOR','IMPLICACAO',None,None])
    elif char != '>' and char != '!': 
      if sentenca[i-1] == '!': tokens.append(['VARIAVEL',char,True,True])
      else: tokens.append(['VARIAVEL',char,True,False])

  arvore = []
 
  descricaoTabela.append(sentenca)

  for z in range(len(tabelaVars[0])):
    j = 0
    for i in vars:
      for token in tokens:
        if token[0] == 'VARIAVEL' and token[1] == i: token[2] = tabelaVars[j][z]
      j +=1
    arvore.append(calculaValorArvore(criaArvore(tokens)))
  tabelaResultado.append(arvore)

  
  print("descricaTabela: ",descricaoTabela)
  print("Tabela Resultado: ", tabelaResultado)
  tabelaVerdadeCompleta = pd.DataFrame(np.transpose(tabelaResultado), columns=descricaoTabela)

  tautologia = True
  for x in tabelaResultado[-1]:
    if x == False: tautologia = False
  if tautologia == True: print("\nA sentença informada é uma tautologia!\nTabela-verdade: \n" + tabelaVerdadeCompleta.to_string()) 
  else: print("\nA sentença informada não é uma tautologia!\nTabela-verdade: \n" + tabelaVerdadeCompleta.to_string()) 

def calculaOperador(operador,valor_1,valor_2):
  """
    Sumário: Calcula o resultado dos operadores lógicos 'ou', 'e', 'condicional'
    e 'implicação' da tabela verdade

    Params: operador, valor_1, valor_2
    
    Retorno:  'False' or 'True'
  """

  if operador=='OU': return(valor_1 or valor_2)
  elif operador=='E': return(valor_1 and valor_2)
  elif (operador=='CONDICIONAL') or (operador=='IMPLICACAO') : 
    if (valor_2 == False) and (valor_1 == True): return(False)
    else: return(True)
  

def calculaValorArvore(arvore):
  """
    Sumário: Calcula o valor da sentença lógica feita com tokens dispostos 
    em uma árvore.

    Params: arvore

    Retorno: Retorna valor de resposta
  """

  if type(arvore)==list: 
    valor_1 = calculaValorArvore(arvore[1])
    valor_2 = calculaValorArvore(arvore[2])
    return(calculaOperador(arvore[0],valor_1,valor_2))
  else: return(arvore)   

def criaArvore(tokens): 
  """
    Sumário:  Entrada em parametro Tokens (Fração da Sentença), para análise e criação
    da arvore de condicionais, após o método calculaValorArvore estar completo...

    Params: Tokens

    Retorno: Arvore Condicional.
  """

  i=0
  for token in tokens:
    if token[0] == 'PARENTESES': 
      posFecha = tratamentoParenteses(tokens)
      if posFecha == len(tokens): # Não tem nada depois do fecha parênteses
        return(criaArvore(tokens[1:posFecha])) 
      else: # Tem alguma coisa depois
        arvoreEsquerda = criaArvore(tokens[1:posFecha])
        arvoreDireita = criaArvore(tokens[posFecha+1:])
        return([tokens[posFecha][1],arvoreEsquerda,arvoreDireita]) 

    elif token[0] == 'OPERADOR':
      arvoreEsquerda = criaArvore(tokens[0:i])
      arvoreDireita = criaArvore(tokens[i+1:])
      return([token[1],arvoreEsquerda,arvoreDireita])

    elif (token[0] == 'VARIAVEL') & (len(tokens) <= 2): 
      if token[3] == True: 
        if token[2] == False: return(True)
        else: return(False)
      else: return(token[2]) # Retorna o valor da variável
    i += 1

def tratamentoParenteses(tokens):
  """
    Sumário:  Pega a sentença de entrada do usuário, realiza a verificação (IF-ELSE), encontra os operadores da entrada.
    Define os operadores e realiza o calculo de acordo com os parenteses, prioridade.

    Params: Tokens (Praticamente a sentença fracionada em CHARs), para verificação de sentenças e caractereres
    
    Retorno:  Aberto - Fechado, leitura de senteça
    Exemplo: Sentença A+!B*(A=>B)
    Saída: Variável OU Negação Variável E Parênteses Variável Implicação Variável

    Diria que em modo Verbose
  """

  i=1
  pilha=['(']
   
  while len(pilha)>0:
    token=tokens[i]
    if token[1]=='FECHA': 
      pilha.pop() # Se o token é um 'fecha' parenteses, desempilha
    if token[1]=='ABRE': 
      pilha.append('(') # Se o token é um 'abre' parenteses, empilha
    i=i+1
  del tokens[i-1]   
  return(i-1)




#Menu inicial do Programa
menu = -1
vars = []
tabelaIsoladaVars = []
descricaoTabela = []

while menu != 0:
  os.system("clear")

  # Try exception para trativa de erro caso o usuário digite algo dif de número
  while True:
    try:
      print("--------------------  Menu Inicial --------------------")                           #Menu Inicial
      menu = int(input("\n0 - Sair\n1 - Definir variáveis\n2 - Calcular sentença\n3 - Sobre\n"))
      break
    except: print("Ops! Não entendi o que você quis dizer, por favor tente novamente\n")

  
  # opção Sair
  # Se o usuário não deseja sair da aplicação, volta ao loop no menu principal, 
  # se ele deseja, não faz nada saindo assim dos loops
  if menu == 0:
    sair = "" 
    while (sair != "s" and sair != "n"): 
      sair = input("\nTem certeza que deseja sair? (s - sim e n - não): ")

      if sair == "n": menu = -1 
      elif sair != "s": print("\nOps! Não entendi o que você quis dizer, por favor tente novamente") 

  # opção Definir Variáveis
  # Chama a função define_variáveis 
  elif menu == 1:
    vars = []
    tabelaIsoladaVars = []
    define_variaveis()
    descricaoTabela = vars.copy()

  # opção Calcular sentença
  # se as variáveis já foram definidas chama a função calculo_senteca
  elif menu == 2:
    if vars == []:
      print("\nPara calcular uma sentença primeiro insira as variáveis! Aperte 'Enter' para continuar")
      confirmacaoUsuario = input('').split(" ")[0]
    else: 
      calculo_senteca(vars,descricaoTabela,tabelaIsoladaVars)
      print("\nAperte 'Enter para continuar'")
      confirmacaoUsuario = input('').split(" ")[0]

  elif menu == 3:                                                                                 #Menu Sobre
    os.system("cls")
    print("Ambiente necessário para execução:",
    "\nSistema Operacional: Windows x86 ou x64 (Preferencialmente) ou Distribuição Linux;",
    "\nBibliotecas Python instaladas no sistema escolhido (3.11 ou superior);"
    "\nCompiladores Python (Jupyter, Pycharm, Atom, Spyder, PyDev e outros);",
    "\n\nRequisitos de hardware:",
    "\nProcessador: 1 Núcleo ou superior, 2.6GHz ou superior;",
    "\nRam: 256Mb Livres;",
    "\nInternet: banda de 5Mbps (caso de execução online);",
    "\nArmazenamento: 100Mb de espaço em disco;")
    menu2 = -1
    while menu2 != 0:
      menu2 = int(input("\n0 - Voltar\n1 - informações do programa\n"))
      if menu2 == 1:
        os.system("cls")
        help(calculo_senteca)                                                                    #DocString, exibe sumário Tabela Verdade
        help(define_variaveis) 
        help(calculaOperador)
        help(calculaValorArvore) 
        help(criaArvore) 
        help(tratamentoParenteses)
  # Se o usuário digitar um número diferente das opções
  else:
    print("\nOps! Não entendi o que você quis dizer, por favor tente novamente. Aperte 'Enter' para continuar")
    confirmacaoUsuario = input('').split(" ")[0]
