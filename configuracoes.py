'''
_________________________________________________________________________________________________________________________________
|                                                                                                                               |
|********************************************************** DESCRIÇÃO **********************************************************|
|_______________________________________________________________________________________________________________________________|
| Neste arquivo se encontram todas as funções responsáveis pela configuração das imagens.                                       |
|                                                                                                                               |
|                                                               Autor: Yago José Araújo dos Santos. Contato: yago.santos@ufv.br |
|_______________________________________________________________________________________________________________________________|
'''

import numpy as np
import random
import platform
random.seed(0)

def getPlataforma():                                                                    # Retorna a identificação do Sistema Operacional
    return str(platform.system())

def getNumeroDeProcessos():                                                             # Retorna o número de processos em paralelo
    numeroDeProcessos = 4
    return numeroDeProcessos

def getExtensaoDaImagem():                                                              # Retorna a extensão da imagem
    extensao = '.jpg'
    return extensao

def getLimiteDeCaracteres():                                                            # Retorna o limite de caracteres do texto a ser inserido na imagem
    limiteDeCaracteres = 280
    return limiteDeCaracteres

def getElementosQueVariam():                                                            # Retorna a configuração manual dos elementos que variam, essa função serve como auxiliar da função 'configuracaoManual'
    # Elementos que variam
    angulo = setAngulo()                                                         # Seleção manual do ângulo de rotação do texto
    if type(angulo) == 'bool' and angulo == False:
        print('ERRO: Configuração inválida!')
        return False, False, False, False, False, False, False
    dimensao = setDimensao()                                                     # Seleção manual da dimensão da imagem
    if dimensao == False:
        print('ERRO: Configuração inválida!')
        return False, False, False, False, False, False, False
    estiloFonte = setFonte()                                                     # Seleção manual do estilo da fonte
    if estiloFonte == False:
        print('ERRO: Configuração inválida!')
        return False, False, False, False, False, False, False
    sombra = setSombra()                                                         # Seleção manual da inserção da sombra no texto
    corDaFonte, corDoPlanoDeFundo = setCorDaFonteEDoPlanoDeFundo()               # Cor da fonte e do plano de fundo definidos de forma manual
    if corDaFonte == False or corDoPlanoDeFundo == False:
        print('ERRO: Configuração inválida!')
        return False, False, False, False, False, False, False
    tamanhoDaFonte = setTamanhoDaFonte()                                         # Seleção manual do tamanho da fonte
    if tamanhoDaFonte == False:
        print('ERRO: Configuração inválida!')
        return False, False, False, False, False, False, False
    return angulo, dimensao, estiloFonte, sombra, corDaFonte, corDoPlanoDeFundo, tamanhoDaFonte

def getPaletaDeCores():                                                                 # Retorna uma lista de cores
    branco = (255, 255, 255)
    preto = (0, 0, 0)
    azul = (0, 0, 255)
    azulMedio = (50, 50, 205)
    azulArdosia = (0, 127, 255)
    azulEscuro = (0, 0, 156)
    paletaDeCores = [branco, preto, azul, azulMedio, azulArdosia, azulEscuro]
    return paletaDeCores

def getListaDeFontes():                                                                 # Retorna uma lista de fontes
    fonte1 = 'Fontes/ComicSansMS3/ComicSansMS3.ttf'                                     # Essa fonte pode aprsentar problemas, verificar
    fonte2 = 'Fontes/SanFranciscoBold(IOS)/Modern Serif.ttf'
    fonte3 = 'Fontes/KGPartofMe/KGPartofMe.ttf'
    fonte4 = 'Fontes/AppleGaramond/AppleGaramond.ttf'
    fonte5 = 'Fontes/Timeless/Timeless.ttf'
    fonte6 = 'Fontes/TypeMachine/Type Machine.ttf'
    fonte7 = 'Fontes/NixieOne/NixieOne.ttf'
    fonte8 = 'Fontes/KGLegoHouse/KGLegoHouse.ttf'
    fonte9 = 'Fontes/KGSorryNotSorry/KGSorryNotSorry.ttf'
    listaDeFontes = [fonte1, fonte2, fonte3, fonte4, fonte5, fonte6, fonte7, fonte8, fonte9]
    return listaDeFontes

def getFonteAleatoria():                                                                # Retorna um estilo de fonte aleatório.
    listaDeFontes = getListaDeFontes()
    x = random.randint(0, len(listaDeFontes) - 1)
    return listaDeFontes[x]

def getTamanhosDaFonte():                                                               # Retorna uma lista de tamnhos para a fonte
    pequeno = 40
    medio = 60
    grande = 80
    tamanhos = [pequeno, medio, grande]
    return tamanhos

def getTamanhoDaFonteAleatorio():                                                       # Retorna um tamanho de fonte aleatório
    tamanhos = getTamanhosDaFonte()
    tamanho = random.randint(0, len(tamanhos) - 1)
    return tamanhos[tamanho]

def getEspacamento():                                                                   # Retorna o espaçamento entre linhas
    espacamento = 4
    return espacamento

def getAlinhamento():                                                                   # Retorna o tipo de alinhamento do texto
    alinhamento = 'center'
    return alinhamento

def getMargem():                                                                        # Retorna o tamanho da margem
    margem = (5, 5, 5, 5)                                                               # margem = (esquerda, superior, direita, inferior)
    return margem

def getMargemDeRotacao():                                                               # Retorna uma margem maior para viabilizar a rotação
    margem = (150, 5, 150, 5)                                                           # margem = (esquerda, superior, direita, inferior)
    return margem

def getMaiuscula():                                                                     # Retorna uma lista com a configuração maiúscula para a fonte
    maiuscula = ['FONTE MAIÚSCULA']
    return maiuscula

def getSombra():                                                                        # Retorna uma lista booleana de possibilidades da sombra
    sombras = [True, False]
    return sombras

def getChecagemDeFatos():                                                                        # Retorna uma lista booleana de possibilidades da sombra
    checagemDeFatos = [True, False]
    return checagemDeFatos

def getSombraAleatorio():                                                               # Retorna uma configuração de sombra aleatória
    sombra = bool(random.getrandbits(1))
    return sombra

def getDimensoes():                                                                     # Retorna a lista de dimensões da imagem
    dimensoes1 = (1080, 566)                                                            # Imagem horizontal Feed proporção de  1.19:1
    dimensoes2 = (1080, 1080)                                                           # Imagem quadrada Feed proporção de 1:1
    dimensoes3 = (1080, 1350)                                                           # Imagem vertical Feed proporção de 4:5
    dimensoes4 = (1080, 1920)                                                           # Imagem vertical Stories proporção de 9:16
    dimensoes = [dimensoes1, dimensoes2, dimensoes3, dimensoes4]
    return dimensoes

def getDimensoesAleatorio():                                                            # Retorna uma dimensão aleatória
    dimensoes = getDimensoes()
    x = random.randint(0, len(dimensoes) - 1)
    return dimensoes[x]

def getAngulosDeRotacao():                                                               # Retorna uma lista com os ângulos de rotação
    anguloMaximo = 30
    anguloMinimo = anguloMaximo * (-1)
    passo = 5
    angulos = []
    for i in range(anguloMinimo, anguloMaximo + 1, passo):
        angulos.append(i)
    return angulos

def getAnguloDeRotacaoAleatorio():                                                      # No estado de geração aleatório, retorna o ângulo de rotação do texto que varia de -30 a 30 de 5 em 5
    angulos = getAngulosDeRotacao()
    #angulo = random.randint(0, len(angulos) - 1)
    #angulos = [-30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30]
    #pesos = [12, 12, 12, 4.5, 4.5, 4.5, 1, 4.5, 4.5, 4.5, 12, 12, 12]
    pesos = [8.16, 8.16, 8.16, 8.16, 8.16, 8.16, 2.08, 8.16, 8.16, 8.16, 8.16, 8.16, 8.16]
    angulo = random.choices(angulos, pesos, k=1)[0]                                    # Escolhe um ângulo de forma aleatória considerando os pesos
    return angulo

def getPossibilidadesDePlanoDeFundo():                                                  # Retorna uma lista com as possibilidades de planos de fundo (imagem ou cor)
    possibilidadesDePlanoDeFundo = ['imagem', 'cor']
    return possibilidadesDePlanoDeFundo

def getCorDaFonteEDoPlanoDeFundoAleatorio():                                            # Seleciona uma cor para a fonte para o plano de fundo de forma aleatória, para cores sólidas, a cor da fonte deve ser diferente da cor do plano de fundo
    paletaDeCores = getPaletaDeCores()
    x = random.randint(0, len(paletaDeCores) - 1)
    corDaFonte = paletaDeCores[x]
    y = random.randint(0, len(paletaDeCores) - 1)
    while (x == y):
        y = random.randint(0, len(paletaDeCores) - 1)
    corDoPlanoDeFundo = paletaDeCores[y]
    return corDaFonte, corDoPlanoDeFundo

def getListaDePlanosDeFundo():                                                          # Retorna uma lista com todas as opções de planos de fundo em formato de lista de strings
    listaDePlanosDeFundo = getPaletaDeCores()
    listaDePlanosDeFundo = [str(i) for i in listaDePlanosDeFundo]
    listaDePlanosDeFundo.append('im1')
    listaDePlanosDeFundo.append('im2')
    return listaDePlanosDeFundo

def getDadosDaRegex(regex):                                                             # Retorna os dados da regex
    regex = regex.split('-')
    indice = eval(regex[0])
    fonte = regex[1]
    tamanhoDaFonte = int(regex[2])
    corDaFonte = eval(regex[3])
    if regex[4] == 'True':
        sombra = True
    else:
        sombra = False
    if regex[5] != 'im1' and regex[5] != 'im2':                                         # O plano de fundo é uma cor sólida
        planoDeFundo = eval(regex[5])
    else:                                                                               # O plano de fundo é outra imagem
        planoDeFundo = regex[5]
    dimensoes = eval(regex[6])    
    if regex[7] == '':                                                                  # Ângulo negativo
        angulo = int(regex[8]) * -1
        if regex[9] == 'True':
            checagemDeFatos = True
        else:
            checagemDeFatos = False
    else:                                                                               # Ângulo positivo
        angulo = int(regex[7])
        if regex[8] == 'True':
            checagemDeFatos = True
        else:
            checagemDeFatos = False
    return indice, fonte, tamanhoDaFonte, corDaFonte, sombra, planoDeFundo, dimensoes, angulo, checagemDeFatos

def getPlanoDeFundo():                                                                  # Retorna uma lista de imagens de plano de fundo
    OS = getPlataforma()
    if OS == 'Windows':                                                                 # Caminho no Windows
        planoDeFundo1 = 'Planos de fundo\im1.jpg'
        planoDeFundo2 = 'Planos de fundo\im2.jpg'
    elif OS == 'Linux':                                                                 # Caminho no Linux
        planoDeFundo1 = 'Planos de fundo/im1.jpg'
        planoDeFundo2 = 'Planos de fundo/im2.jpg'
    listaDeImagens = [planoDeFundo1, planoDeFundo2]
    return listaDeImagens

def getMenu(listaDeOpcoes):                                                             # Cria uma menu para a lista informada e retorna a opção selecionada
    resposta = 0
    cont = 1
    limInferior = 1
    limSuperior = len(listaDeOpcoes) + 1
    print('[Cod] | [Opções]')
    for opcao in listaDeOpcoes:
        print(' (%d)  | '%(cont) + str(opcao))
        cont += 1
    print('\n (%d)  | '%(cont) + 'Sair\n')
    while resposta < limInferior or resposta > limSuperior:
        resposta = int(input('Informe o código da opção desejada. Intervalo [%d - %d]: ' %(limInferior, limSuperior)))
    if resposta == limSuperior:
        return False
    else:
        return listaDeOpcoes[resposta - 1]

def getConfiguracaoPadrao():                                                               # Configuração padrão de imagem
    angulo, dimensoes, fonte, sombra, corDaFonte, corDoPlanoDeFundo, tamanhoDaFonte = 0, (1080, 1920), 'Fontes/Timeless/Timeless.ttf', False, (0, 0, 0), (255, 255, 255), 40
    return angulo, dimensoes, fonte, sombra, corDaFonte, corDoPlanoDeFundo, tamanhoDaFonte

def setAngulo():                                                                        # Define o angulo de forma manual
    print('\n' + 10 * '_' + ' Seleção do ângulo ' + 10 * '_' + '\n')
    return getMenu(getAngulosDeRotacao())

def setDimensao():                                                                      # Define a dimensão de forma manual
    print('\n' + 10 * '_' + ' Seleção da dimensão ' + 10 * '_' + '\n')
    return getMenu(getDimensoes())

def setFonte():                                                                         # Define a fonte de forma manual
    print('\n' + 10 * '_' + ' Seleção da fonte ' + 10 * '_' + '\n')
    return getMenu(getListaDeFontes())

def setSombra():                                                                        # Define a sombra de forma manual
    print('\n' + 10 * '_' + ' Seleção da sombra ' + 10 * '_' + '\n')
    return getMenu(getSombra())

def setCorDaFonteEDoPlanoDeFundo():                                                     # Define a cor da fonte e do plano de fundo de forma manual
    print('\n' + 3 * '_' + ' Seleção da cor da fonte e do plano de fundo ' + 3 * '_' + '\n')
    corDaFonte = corDoPlanoDeFundo = (0, 0, 0)
    while corDaFonte == corDoPlanoDeFundo:
        corDaFonte = getMenu(getPaletaDeCores())
        if corDaFonte == False:
            return False, False
        escolha = getMenu(getPossibilidadesDePlanoDeFundo())
        if escolha == False:
            return False, False
        elif escolha == 'cor':
            corDoPlanoDeFundo = getMenu(getPaletaDeCores())
            if corDoPlanoDeFundo == False:
                return False, False
        elif escolha == 'imagem':
            corDoPlanoDeFundo = getMenu(getPlanoDeFundo())
    return corDaFonte, corDoPlanoDeFundo

def setTamanhoDaFonte():                                                                # Define o tamanho da fonte de forma manual
    print('\n' + 10 * '_' + ' Seleção do tamanho da fonte ' + 10 * '_' + '\n')
    return getMenu(getTamanhosDaFonte())