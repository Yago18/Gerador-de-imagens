'''
_________________________________________________________________________________________________________________________________
|                                                                                                                               |
|********************************************************** DESCRIÇÃO **********************************************************|
|_______________________________________________________________________________________________________________________________|
| Neste arquivo se encontram todas as funções responsáveis pela criação do dataset.                                             |
|                                                                                                                               |
|                                                               Autor: Yago José Araújo dos Santos. Contato: yago.santos@ufv.br |
|_______________________________________________________________________________________________________________________________|
'''

import os
import time
import random
import csv
import numpy as np
import math
from multiprocessing.pool import ThreadPool
import PIL
from PIL import Image
from PIL import ImageFilter
from PIL import ImageFont
from PIL import ImageDraw
import configuracoes as config
import auxiliar
random.seed(0)

def configuracaoManual(OS, indice, tamanhoTexto, texto, angulo, dimensao, estiloFonte, sombra, corDaFonte, corDoPlanoDeFundo, tamanhoDaFonte, configuracaoDeGeracao):                                        # Recebe a quantidade de caracteres do texto e configura o tipo de imagem a ser gerada
    # Elementos fixos
    alinhamento = config.getAlinhamento()                                               # Alinhamento do texto
    espacamento = config.getEspacamento()                                               # Espaçamento entre linhas
    margem = config.getMargem()                                                         # Tamanho da margem
    # Primeiro essa função tenta inserir o texto na imagem com a configuração indicada
    if angulo == 0:
        anguloOriginal = True
    else:
        anguloOriginal = False
    textoAjustado = ajustaTexto(estiloFonte, tamanhoDaFonte, dimensao, margem, texto)
    if textoAjustado != False:
        if angulo != 0:
            margem = config.getMargemDeRotacao() 
        return margem, alinhamento, espacamento, angulo, anguloOriginal, textoAjustado
    # Caso ainda não seja possível produzir uma imagem, a informação textual é ignorada e o programa pega o próximo texto
    else:
        return False, False, False, 'ERRO', False, False

def configuracaoAleatoria(OS, indice, tamanhoTexto, texto, configuracaoDeGeracao):      # Recebe a quantidade de caracteres do texto e configura o tipo de imagem a ser gerada
    # Elementos que variam
    angulo = config.getAnguloDeRotacaoAleatorio()                                       # Seleção aleatória do ângulo de rotação do texto
    dimensaoAtual = dimensao = config.getDimensoesAleatorio()                           # Seleção aleatória da dimensão da imagem
    estiloFonte = config.getFonteAleatoria()                                            # Seleção aleatória do estilo da fonte
    sombra = config.getSombraAleatorio()                                                # Seleção aleatória da inserção da sombra no texto
    corDaFonte, corDoPlanoDeFundo = config.getCorDaFonteEDoPlanoDeFundoAleatorio()      # Cor da fonte e do plano de fundo definidos de forma aleatória
    tamanhoDaFonteAtual = tamanhoDaFonte = config.getTamanhoDaFonteAleatorio()          # Seleção aleatória do tamanho da fonte
    # Elementos fixos
    dimensoes = config.getDimensoes()                                                   # Lista de dimensões
    alinhamento = config.getAlinhamento()                                               # Alinhamento do texto
    espacamento = config.getEspacamento()                                               # Espaçamento entre linhas
    margem = config.getMargem()                                                         # Tamanho da margem
    tamanhosDaFonte = config.getTamanhosDaFonte()                                       # Lista de tamanhos de fonte
    # Primeiro essa função tenta inserir o texto na imagem com o tamanho de fonte aleatório, caso não consiga ela testará todos os tamanhos de fonte possíveis
    if angulo == 0:
        anguloOriginal = True
    else:
        anguloOriginal = False
    if angulo != 0:
        margem = config.getMargemDeRotacao()
        textoAjustado = ajustaTexto(estiloFonte, tamanhoDaFonte, dimensao, margem, texto)
    else:
        textoAjustado = ajustaTexto(estiloFonte, tamanhoDaFonte, dimensao, margem, texto)
    if textoAjustado != False:
        return dimensao, corDaFonte, corDoPlanoDeFundo, margem, alinhamento, estiloFonte, sombra, tamanhoDaFonte, espacamento, angulo, anguloOriginal, textoAjustado
    # Caso não consiga inserir o texto de nenhuma forma, a função aplicará a seguinte contramedida que aumenta a dimensão da imagem e reduz o tamanho da fonte de forma gradual até que seja possível produzir uma imagem. Caso ainda não seja possível produzir uma imagem, a informação textual é ignorada e o programa pega o próximo texto
    else:
        print('Aplicando contramedida...')
        for tamanhoDaFonte in tamanhosDaFonte:
            if tamanhoDaFonte < tamanhoDaFonteAtual:
                print('Reduzindo o tamanho da fonte...')
                for dimensao in dimensoes:
                    if dimensao[0] >= dimensaoAtual[0] and dimensao[1] > dimensaoAtual[1]:
                        print('Aumentando a dimensão da imagem...')
                        textoAjustado = ajustaTexto(estiloFonte, tamanhoDaFonte, dimensao, margem, texto)
                        if textoAjustado != False:
                            return dimensao, corDaFonte, corDoPlanoDeFundo, margem, alinhamento, estiloFonte, sombra, tamanhoDaFonte, espacamento, angulo, anguloOriginal, textoAjustado
                        else:
                            print('ERRO: Não foi possível produzir a imagem com a configuração indicada, tentando com outra configuração...')
                            print('\n<<<<<<<<<< REGISTRANDO LOG >>>>>>>>>>\n')
                            nomeDoArquivo = str('DATASET - RANDOM' + '/' + '(' + str(indice) +') ' + '-' + str(estiloFonte) + '-' + str(tamanhoDaFonte) + '-' + str(corDaFonte) + '-' + str(corDoPlanoDeFundo) + '-' + str(sombra) + '-' + str(dimensao) + '-' + str(angulo) + config.getExtensaoDaImagem())
                            logs = open('Logs - configurações impossíveis.txt', 'a')
                            logs.write(nomeDoArquivo + '\n')
                            logs.close()
        if textoAjustado == False:
            print('ERRO: Não foi possível produzir a imagem com a configuração indicada!')
            return False, False, False, False, False, False, False, False, False, 'ERRO', False, False

def configuracaoTodasCombinacoes(OS, caminho, tamanhoTexto, texto, indice, configuracaoDeGeracao):                              # Recebe a quantidade de caracteres do texto e configura o tipo de imagem a ser gerada
    extensaoDaImagem = config.getExtensaoDaImagem()
    dimensoes = config.getDimensoes()
    angulos = config.getAngulosDeRotacao()
    listaDeFontes = config.getListaDeFontes()
    sombras = config.getSombra()
    paletaDeCores = config.getPaletaDeCores()
    tamanhosDaFonte = config.getTamanhosDaFonte()
    possibilidadesDePlanoDeFundo = config.getPossibilidadesDePlanoDeFundo()
    espacamento = config.getEspacamento()
    margem = config.getMargem()
    alinhamento = config.getAlinhamento()
    AS = 0
    for dimensao in dimensoes:
        for angulo in angulos:
            if angulo == 0:
                anguloOriginal = True
            else:
                anguloOriginal = False
            for fonte in listaDeFontes:
                for tamanhoDaFonte in tamanhosDaFonte:
                    if angulo != 0:
                        margemDeRotacao = config.getMargemDeRotacao()
                        textoAjustado = ajustaTexto(fonte, tamanhoDaFonte, dimensao, margemDeRotacao, texto)
                    elif angulo == 0 or textoAjustado == False:
                        textoAjustado = ajustaTexto(fonte, tamanhoDaFonte, dimensao, margem, texto)
                    if textoAjustado != False:
                        for sombra in sombras:
                            for corDaFonte in paletaDeCores:
                                for possibilidadeDePlanoDeFundo in possibilidadesDePlanoDeFundo:
                                    if possibilidadeDePlanoDeFundo == 'imagem':                      # Testa todas as possibilidades considerando que o plano de fundo é composto por outra imagem
                                        planosDeFundo, nomesDosPlanosDefundo = criaImagemAPartirDeOutraImagem(OS, dimensao)
                                        i = 0
                                        for img in planosDeFundo:
                                            img, angulo = insereTextoNaImagem(indice, img, margem, dimensao, textoAjustado, fonte, sombra, alinhamento, tamanhoDaFonte, corDaFonte, espacamento, angulo, anguloOriginal, configuracaoDeGeracao)
                                            if img == False:
                                                print('\nERRO: (A caixa de texto está sendo posicionada em uma coordenada negativa, isso pode estar acontecendo por excesso do número de linhas, dessa forma a imagem não será salva)')
                                            else:
                                                auxiliar.cria_diretorio(caminho)
                                                caminhoDaFonte = os.path.basename(fonte)
                                                nomeDaFonte = os.path.splitext(caminhoDaFonte)[0]
                                                #Regex da imagem: (Número da linha da planilha que contém a notícia) - nome da fonte - tamanho da fonte - cor da fonte - sombra - cor do plano de fundo - dimensões da imagem - angulo de rotação do texto
                                                nomeDoArquivo = str(caminho + '/' + '(' + str(indice) +') ' + '-' + str(nomeDaFonte) + '-' + str(tamanhoDaFonte) + '-' + str(corDaFonte) + '-' + str(sombra) + '-' + str(nomesDosPlanosDefundo[i]) + '-' + str(img.size) + '-' + str(angulo) + extensaoDaImagem)
                                                img.save(nomeDoArquivo)
                                            i = i + 1
                                    else:
                                        for corDoPlanoDeFundo in paletaDeCores:                      # Testa todas as possibilidades considerando que o plano de fundo é somente cor
                                            if corDaFonte != corDoPlanoDeFundo:
                                                img = criaImagem(dimensao, corDoPlanoDeFundo)
                                                img, angulo = insereTextoNaImagem(indice, img, margem, dimensao, textoAjustado, fonte, sombra, alinhamento, tamanhoDaFonte, corDaFonte, espacamento, angulo, anguloOriginal, configuracaoDeGeracao)
                                                if img == False:
                                                    print('\nERRO: (A caixa de texto está sendo posicionada em uma coordenada negativa, isso pode estar acontecendo por excesso do número de linhas, dessa forma a imagem não será salva)')
                                                else:
                                                    auxiliar.cria_diretorio(caminho)
                                                    caminhoDaFonte = os.path.basename(fonte)
                                                    nomeDaFonte = os.path.splitext(caminhoDaFonte)[0]
                                                    #Regex da imagem: (Número da linha da planilha que contém a notícia) - nome da fonte - tamanho da fonte - cor da fonte - sombra - cor do plano de fundo - dimensões da imagem - angulo de rotação do texto
                                                    nomeDoArquivo = str(caminho + '/' + '(' + str(indice) +') ' + '-' + str(nomeDaFonte) + '-' + str(tamanhoDaFonte) + '-' + str(corDaFonte) + '-' + str(sombra) + '-' + str(corDoPlanoDeFundo) + '-' + str(img.size) + '-' + str(angulo) + extensaoDaImagem)
                                                    img.save(nomeDoArquivo)

                                        #A medida em points multiplica os pixels por 1.33, para compensar eu multipliquei o limite por 1.67
                    else:
                        print('ERRO: Não foi possível produzir a imagem com a configuração indicada!')

def criaImagem(tamanho, cor):                                                           #Cria uma imagem
    img = PIL.Image.new(mode = "RGB", size = tamanho, color = cor)
    return img

def criaImagemTransparente(tamanho):                                                    #Cria uma imagem
    img = PIL.Image.new(mode = "RGBA", size = tamanho, color = (255, 255, 255, 0))
    return img

def criaImagemAPartirDeOutraImagemManual(OS, tamanho, planoDeFundo):                    #Usa uma imagem como plano de fundo
    planoDeFundo1 = Image.open(planoDeFundo)
    if planoDeFundo == 'Planos de fundo\im1.jpg' or planoDeFundo == 'Planos de fundo/im1.jpg':
        nomeDaImagem = 'im1'
    elif planoDeFundo == 'Planos de fundo\im2.jpg' or planoDeFundo == 'Planos de fundo/im2.jpg':
        nomeDaImagem = 'im2'
    img = planoDeFundo1.resize(tamanho)
    return img, nomeDaImagem

def criaImagemAPartirDeOutraImagem(OS, tamanho):                                        # Usa uma imagem como plano de fundo
    if OS == 'Windows':
        # Caminho no Windows
        planoDeFundo1 = Image.open('Planos de fundo\im1.jpg')
        planoDeFundo2 = Image.open('Planos de fundo\im2.jpg')
    elif OS == 'Linux':
        # Caminho no Linux
        planoDeFundo1 = Image.open('Planos de fundo/im1.jpg')
        planoDeFundo2 = Image.open('Planos de fundo/im2.jpg')
    nomeDosPlanosDeFundo = ['im1', 'im2']
    listaDeImagens = [planoDeFundo1, planoDeFundo2]
    listaDeRetorno = []
    for imagem in listaDeImagens:
        img = imagem.resize(tamanho)
        listaDeRetorno.append(img)
    return listaDeRetorno, nomeDosPlanosDeFundo

def criaImagemAPartirDeOutraImagemAleatorio(OS, tamanho):                               # Usa uma imagem como plano de fundo
    if OS == 'Windows':
        # Caminho no Windows
        planoDeFundo1 = Image.open('Planos de fundo\im1.jpg')
        planoDeFundo2 = Image.open('Planos de fundo\im2.jpg')
    elif OS == 'Linux':
        # Caminho no Linux
        planoDeFundo1 = Image.open('Planos de fundo/im1.jpg')
        planoDeFundo2 = Image.open('Planos de fundo/im2.jpg')
    nomeDosPlanosDeFundo = ['im1', 'im2']
    listaDeImagens = [planoDeFundo1, planoDeFundo2]
    x = random.randint(0, len(listaDeImagens) - 1)
    planoDeFundo = listaDeImagens[x].resize(tamanho)
    return planoDeFundo, nomeDosPlanosDeFundo[x]

def insereSombra(imagem, posicao, texto, corDaFonte, font, espacamento, alinhamento, tamanhoDaFonte):   # Insere sombra no texto
    tmp = imagem
    tmp2 = criaImagemTransparente(imagem.size)                                          # Imagem vazia
    if tamanhoDaFonte > 40:
        intensidade = 2                                                                 # Intensidade da sombra
    else:
        intensidade = 1
    posX = int(0.05 * tamanhoDaFonte)                                                   # Posição da sombra
    posY = int(0.05 * tamanhoDaFonte)
    tmp = tmp.filter(ImageFilter.BoxBlur(intensidade))                                  # Inserindo sombra no texto
    tmp2.paste(tmp, (posX, posY), tmp)
    tmp2.paste(imagem, (0, 0), imagem)                                                  # Sobrepondo as imagens
    return tmp2

def ajustaTexto(fonte, tamanhoDaFonte, dimensoes, margem, texto):                       # Formata o texto para caber na imagem
    # margem = (esquerda, superior, direita, inferior)
    tamanhoDaImagem = dimensoes                                                         # Dimensões da imagem auxiliar
    branco = (255, 255, 255)                                                            # Cor do plano de fundo
    preto = (0, 0, 0)                                                                   # Cor do texto
    posicao = (margem[0], margem[1])                                                    # Posição da caixa de texto
    largura = 0
    altura = 0
    texto = texto.replace('\n', ' ')                                                    # Remove as quebras de linha do texto original
    texto = texto.replace('  ', ' ')                                                    # Remove os espaçamentos duplos do texto original
    texto = texto.split(' ')                                                            # Transforma o texto em uma lista de palavras
    lista = []
    text = ''
    frase = ''                                                                          # Acumula os caracteres de uma linha da caixa de texto
    qtdPalavras = 0                                                                     # Inicializando o contador de palavras
    limiteDeCaracteres = 0                                                              # Inicializando o contador de limite de caracteres
    #print('TEXTO: ', texto)
    for palavra in texto:
        qtdPalavras += 1
        aux = text
        if len(text) == 0:                                                              # Se a string 'text' for vazia, faça 'text' = palavra
            text = palavra
            frase = palavra
            aux2 = frase
        else:                                                                           # Senão, concatene a palavra a string 'text' e a string 'frase'
            text = text + ' ' + palavra
            aux2 = frase
            frase = frase + ' ' + palavra
        if len(frase) > limiteDeCaracteres or qtdPalavras == len(texto):                # Se o tamanho da string 'frase' exceder oo limite de caracteres ou a quantidade de palavras for igual ao tamanho do texto, verifique a largura da frase, se couber na imagem, insira-a, senão, adicione uma quebra de texto e recalcule
            imagem = criaImagem(tamanhoDaImagem, branco)
            draw = ImageDraw.Draw(imagem)
            font = ImageFont.truetype(fonte, tamanhoDaFonte)
            draw.multiline_text(posicao, text, preto, font)
            #imagem.show()
            dim = draw.textbbox(posicao, text, font)
            largura = dim[2] - dim[0]
            altura = dim[3] - dim[1]
            if largura > (dimensoes[0] - (margem[0] + margem[2])):
                text = aux
                text = text + '\n' + palavra
                limiteDeCaracteres = len(aux2)
                frase = palavra
                aux = text
                imagem = criaImagem(tamanhoDaImagem, branco)
                draw = ImageDraw.Draw(imagem)
                font = ImageFont.truetype(fonte, tamanhoDaFonte)
                draw.multiline_text(posicao, text, preto, font)
                dim = draw.textbbox(posicao, text, font)
                largura = dim[2] - dim[0]
                altura = dim[3] - dim[1]
                if largura > (dimensoes[0] - (margem[0] + margem[2])):
                    print('ERRO: O texto contém uma palavra que excede os limites da linha')
                    return False
            if altura > (dimensoes[1] - margem[3]):
                    print('ERRO: O texto excede os limites da imagem')
                    return False
    return text

def verificaPontos(pontos, imagem, margem):
    distancia = []
    origem = (0, 0)
    for ponto in pontos:
        distancia.append(math.sqrt(((ponto[0] - origem[0]) ** 2) + ((ponto[1] - origem[1]) ** 2)))      # Calcula a distância entre dois pontos
    # Analogia: Pense na rotação como sendo o ponteiro de um relógio, o ponteiro é fixo na origem, grau pequeno diminui pouco o Y, grau grande decrementa muito o Y.
    a = pontos[0]
    b = pontos[1]
    c = pontos[2]
    d = pontos[3]
    if (abs(d[0]) + abs(a[0]) > imagem.size[0] - (margem[0] * 2))\
         or (abs(b[0]) + abs(c[0]) > imagem.size[0] - (margem[2] * 2)\
             or (abs(b[1]) + abs(c[1]) > imagem.size[1] - margem[1] * 2)\
                or (abs(a[1]) + abs(d[1]) > imagem.size[1] - margem[3] * 2)):
        return False
    else:
        return True

def insereTextoNaImagem(indice, imagem, margem, dimensoes, texto, fonte, sombra, alinhamento, tamanhoDaFonte, corDaFonte, espacamento, angulo, anguloOriginal, configuracaoDeGeracao):     # Insere texto na imagem
    # margem = (esquerda, superior, direita, inferior)
    branco = (255, 255, 255)
    preto = (0, 0, 0)
    if angulo == 0:
        margem = config.getMargem()
        if anguloOriginal == False:
            texto = ajustaTexto(fonte, tamanhoDaFonte, (imagem.size[0], imagem.size[1]), margem, texto)
        if texto != False:
            tmp = criaImagemTransparente(imagem.size)
            draw = ImageDraw.Draw(tmp)
            font = ImageFont.truetype(fonte, tamanhoDaFonte)
            margem = config.getMargem()
            dimensoes = (imagem.size[0], imagem.size[1])
            posicao = (margem[0], margem[1])
            dimensoes = draw.multiline_textbbox(posicao, texto, font)                       # Pega as dimensões da caixa de texto
            posX = (imagem.size[0] - (dimensoes[2] - dimensoes[0])) / 2                     # Centraliza a caixa de texto na imagem
            posY = ((imagem.size[1] - (dimensoes[3] - dimensoes[1])) / 2) - (margem[1] + margem[3])
            posicao = (posX, posY)                                                          # Coloca o texto no meio da imagem
            draw.multiline_text(posicao, texto, corDaFonte, font, None, espacamento, alinhamento)
            if sombra == True:
                tmp = insereSombra(tmp, posicao, texto, corDaFonte, font, espacamento, alinhamento, tamanhoDaFonte)
                imagem.paste(tmp, (0, 0), tmp)
            imagem.paste(tmp, (0, 0), tmp)
            return imagem, angulo
        else:
            return False, 'ERRO'
    else:
        draw = ImageDraw.Draw(imagem)
        font = ImageFont.truetype(fonte, tamanhoDaFonte)
        posicao = (margem[0], margem[1])
        dimensoes = draw.multiline_textbbox(posicao, texto, font)                       # Pega as dimensões da caixa de texto
        x1 = dimensoes[0]
        x2 = dimensoes[2]
        y1 = dimensoes[1]
        y2 = dimensoes[3]
        A = (x1, y1)
        B = (x1, y2)
        C = (x2, y1)
        D = (x2, y2)
        #print('\nPontos da caixa de texto originais: ', A, B, C, D)
        # Movendo pontos para origem
        x1t = x1 - x1
        x2t = x2 - x1
        y1t = y1 - y1
        y2t = y2 - y1
        A = (x1t, y1t)
        B = (x1t, y2t)
        C = (x2t, y1t)
        D = (x2t, y2t)
        ang = angulo
        angulo = math.radians(angulo) # Converte o ângulo para radianos
        seno = math.sin(angulo)
        coseno = math.cos(angulo)
        angulo = ang
        a = ((x1t * coseno - y1t * seno), (x1t * seno + y1t * coseno))
        b = ((x1t * coseno - y2t * seno), (x1t * seno + y2t * coseno))
        c = ((x2t * coseno - y1t * seno), (x2t * seno + y1t * coseno))
        d = ((x2t * coseno - y2t * seno), (x2t * seno + y2t * coseno))
        pontos = [a, b, c, d]
        check = False
        if verificaPontos(pontos, imagem, margem) == False:
            check = False
        else:
            check = True
        verificador = check
        posX = (imagem.size[0] - (dimensoes[2] - dimensoes[0])) / 2                     # Centraliza a caixa de texto na imagem
        posY = ((imagem.size[1] - (dimensoes[3] - dimensoes[1])) / 2) - (margem[1] + margem[3])
        posicao = (posX, posY)                                                          # Coloca o texto no meio da imagem
        tmp = imagem
        tmp2 = criaImagemTransparente(imagem.size)
        draw2 = ImageDraw.Draw(tmp2)
        draw2.multiline_text(posicao, texto, corDaFonte, font, None, espacamento, alinhamento)
        if verificador == True:
            tmp2 = tmp2.rotate(angulo)
            imagem = tmp2
            if sombra == True:  # Aplica a sombra no texto
                imagem = insereSombra(imagem, posicao, texto, corDaFonte, font, espacamento, alinhamento, tamanhoDaFonte)
                tmp.paste(imagem, (0, 0), imagem)
                imagem = tmp
            else:
                tmp.paste(tmp2, (0, 0), tmp2)
                imagem = tmp
            return imagem, angulo
        else: # Se a configuração 'MANUAL', 'COMB ALL', ou 'MIN and MAX' estiver acionada, nenhuma contramedida deve ser adotada
            if configuracaoDeGeracao == 'MANUAL' or configuracaoDeGeracao == 'COMB ALL' or configuracaoDeGeracao == 'MIN and MAX':
                return False, 'ERRO'
            else:
                print('ERRO: (Não foi possível rotacionar a imagem, o texto é muito extenso, reduzindo o ângulo)')
                if angulo < 0:
                    angulo = angulo + 5
                    if angulo == 0:
                        anguloOriginal = False
                elif angulo > 0:
                    angulo = angulo - 5
                    if angulo == 0:
                        anguloOriginal = False
                imagem, angulo = insereTextoNaImagem(indice, imagem, margem, dimensoes, texto, fonte, sombra, alinhamento, tamanhoDaFonte, corDaFonte, espacamento, angulo, anguloOriginal, configuracaoDeGeracao)
                return imagem, angulo

def criaConjuntoDeDadosAleatorio(OS, caminho, dimensoes, corDoPlanoDeFundo, fonte, corDaFonte, sombra, tamanhoDaFonte, espacamento, textoAjustado, margem, alinhamento, angulo, anguloOriginal, indice, configuracaoDeGeracao, listaDeFatosVerificados):   #Cria o conjunto de dados diretório a diretório
    if listaDeFatosVerificados[indice] == 'FALSO':
        checagemDeFatos = True
    else:
        checagemDeFatos = False
    extensaoDaImagem = config.getExtensaoDaImagem()
    population = [1, 2]
    weights = [80, 20]                                                                    # 20% de chances de gerar uma imagem com plano de fundo baseado em outra imagem e 80% de chances de gerar uma imagem com plano de fundo colorido
    verificador = False                                                                   # Verifica se o plano de fundo é uma corsólida ou outra imagem
    valor = random.choices(population, weights, k = 1)                                    # Sorteia o tipo de imagem a ser gerada com base nos pesos de cada conjunto
    if valor[0] == 1:
        img = criaImagem(dimensoes, corDoPlanoDeFundo)
    else:
        img, nomeDoPlanoDeFundo = criaImagemAPartirDeOutraImagemAleatorio(OS, dimensoes)
        verificador = True
    img, angulo = insereTextoNaImagem(indice, img, margem, dimensoes, textoAjustado, fonte, sombra, alinhamento, tamanhoDaFonte, corDaFonte, espacamento, angulo, anguloOriginal, configuracaoDeGeracao)
    if angulo != 'ERRO':
        angulo = int(angulo)
    if type(img) != bool and img != False:
        auxiliar.cria_diretorio(caminho)
        caminhoDaFonte = os.path.basename(fonte)
        nomeDaFonte = os.path.splitext(caminhoDaFonte)[0]
        if verificador == False:
            # Regex da imagem: (Número da linha da planilha que contém a notícia) - nome da fonte - tamanho da fonte - cor da fonte - sombra - cor do plano de fundo - dimensões da imagem - angulo de rotação do texto
            nomeDoArquivo = str(caminho + '/' + '(' + str(indice) +') ' + '-' + str(nomeDaFonte) + '-' + str(tamanhoDaFonte) + '-' + str(corDaFonte) + '-' + str(sombra) + '-' + str(corDoPlanoDeFundo) + '-' + str(img.size) + '-' + str(angulo) + '-' + str(checagemDeFatos) + extensaoDaImagem)
            img.save(nomeDoArquivo, quality = 100, dpi = (300, 300))
        else:
            # Regex da imagem: (Número da linha da planilha que contém a notícia) - nome da fonte - tamanho da fonte - cor da fonte - sombra - cor do plano de fundo - dimensões da imagem - angulo de rotação do texto
            nomeDoArquivo = str(caminho + '/' + '(' + str(indice) +') ' + '-' + str(nomeDaFonte) + '-' + str(tamanhoDaFonte) + '-' + str(corDaFonte) + '-' + str(sombra) + '-' + str(nomeDoPlanoDeFundo) + '-' + str(img.size) + '-' + str(angulo) + '-' + str(checagemDeFatos) + extensaoDaImagem)
            img.save(nomeDoArquivo, quality = 100, dpi = (300, 300))

def criaConjuntoDeDadosManual(OS, caminho, dimensoes, corDoPlanoDeFundo, fonte, corDaFonte, sombra, tamanhoDaFonte, espacamento, textoAjustado, margem, alinhamento, angulo, anguloOriginal, indice, configuracaoDeGeracao, listaDeFatosVerificados):   #Cria o conjunto de dados diretório a diretório
    if listaDeFatosVerificados[indice] == 'FALSO':
        checagemDeFatos = True
    else:
        checagemDeFatos = False
    extensaoDaImagem = config.getExtensaoDaImagem()
    verificador = False                                                                     # Verifica se o plano de fundo é uma cor sólida ou outra imagem
    if type(corDoPlanoDeFundo) != str:
        img = criaImagem(dimensoes, corDoPlanoDeFundo)
    else:
        img, nomeDoPlanoDeFundo = criaImagemAPartirDeOutraImagemManual(OS, dimensoes, corDoPlanoDeFundo)
        verificador = True
    img, angulo = insereTextoNaImagem(indice, img, margem, dimensoes, textoAjustado, fonte, sombra, alinhamento, tamanhoDaFonte, corDaFonte, espacamento, angulo, anguloOriginal, configuracaoDeGeracao)
    if angulo != 'ERRO':
        angulo = int(angulo)
    if type(img) != bool and img != False:
        auxiliar.cria_diretorio(caminho)
        caminhoDaFonte = os.path.basename(fonte)
        nomeDaFonte = os.path.splitext(caminhoDaFonte)[0]
        if verificador == False:
            # Regex da imagem: (Número da linha da planilha que contém a notícia) - nome da fonte - tamanho da fonte - cor da fonte - sombra - cor do plano de fundo - dimensões da imagem - angulo de rotação do texto
            nomeDoArquivo = str(caminho + '/' + '(' + str(indice) +') ' + '-' + str(nomeDaFonte) + '-' + str(tamanhoDaFonte) + '-' + str(corDaFonte) + '-' + str(sombra) + '-' + str(corDoPlanoDeFundo) + '-' + str(img.size) + '-' + str(angulo) + '-' + str(checagemDeFatos) + extensaoDaImagem)
            img.save(nomeDoArquivo, quality = 100, dpi = (300, 300))
        else:
            # Regex da imagem: (Número da linha da planilha que contém a notícia) - nome da fonte - tamanho da fonte - cor da fonte - sombra - cor do plano de fundo - dimensões da imagem - angulo de rotação do texto
            nomeDoArquivo = str(caminho + '/' + '(' + str(indice) +') ' + '-' + str(nomeDaFonte) + '-' + str(tamanhoDaFonte) + '-' + str(corDaFonte) + '-' + str(sombra) + '-' + str(nomeDoPlanoDeFundo) + '-' + str(img.size) + '-' + str(angulo) + extensaoDaImagem)
            img.save(nomeDoArquivo, quality = 100, dpi = (300, 300))
    if type(img) == bool and img == False and type(angulo) == str and angulo == 'ERRO':
        print('\n<<<<<<<<<< REGISTRANDO LOG >>>>>>>>>>\n')
        nomeDoArquivo = str(configuracaoDeGeracao + '-' + '(' + str(indice) +') ' + '-' + str(fonte) + '-' + str(tamanhoDaFonte) + '-' + str(corDaFonte) + '-' + str(sombra) + '-' + str(corDoPlanoDeFundo) + '-' + str(dimensoes) + '-' + str(angulo) + '-' + str(checagemDeFatos) + extensaoDaImagem)
        logs = open('Logs - textos descartados.txt', 'a')
        logs.write(nomeDoArquivo + '\n')
        logs.close()
#________________________________________________________________________________________________________________________________________________________________________________________________________________________
def processaMenorEMaiorTexto(OS, diretorio, listaDeTextos):                                                # Gera todas as combinações para o menor e o maior textos
    print('\n' + '_' * 20 + ' GERANDO IMAGENS ' + '_' * 20 + '\n')
    limiteDeCaracteres = config.getLimiteDeCaracteres()
    indiceMenor, indiceMaior = auxiliar.determinaOMenorEOMaiorTexto(listaDeTextos, limiteDeCaracteres)
    caminho = diretorio
    auxiliar.deletaDiretorio(caminho)
    configuracaoDeGeracao = 'MIN and MAX'
    # Gera todas as combinações para o menor texto
    item = listaDeTextos[indiceMenor] 
    configuracaoTodasCombinacoes(OS, caminho, len(item), item, indiceMenor, configuracaoDeGeracao)
    # Gera todas as combinações para o maior texto
    item = listaDeTextos[indiceMaior]
    configuracaoTodasCombinacoes(OS, caminho, len(item), item, indiceMaior, configuracaoDeGeracao)
    print('\n' + '_' * 20 + ' FIM DA EXECUÇÃO DA THREAD ' + '_' * 20 + '\n')

def processaTodasCombinacoes(OS, diretorio, listaDeTextos, dataset):                                        # Gera todas as combinações para cada amostra de texto
    print('\n' + '_' * 20 + ' GERANDO IMAGENS ' + '_' * 20 + '\n')
    limiteDeCaracteres = config.getLimiteDeCaracteres()
    caminho = diretorio
    auxiliar.deletaDiretorio(caminho)
    configuracaoDeGeracao = 'COMB ALL'
    # Gera todas as combinações possíveis para cada amostra de texto
    for texto in listaDeTextos:
        indice = dataset.index(texto)
        configuracaoTodasCombinacoes(OS, caminho, len(texto), texto, indice, configuracaoDeGeracao)
    print('\n' + '_' * 20 + ' FIM DA EXECUÇÃO DA THREAD ' + '_' * 20 + '\n')

def processaAleatorio(OS, listaDeTextos, numImagensComOMesmoTexto, dataset, listaDeFatosVerificados):                     # Produz imagens com configuração aleatória
    print('\n' + '_' * 20 + ' GERANDO IMAGENS ' + '_' * 20 + '\n')
    limiteDeCaracteres = config.getLimiteDeCaracteres()
    caminho = 'DATASET - RANDOM'
    configuracaoDeGeracao = 'RANDOM'
    for item in listaDeTextos:
        indice = dataset.index(item)
        if len(item) <= limiteDeCaracteres:                                                      # Limitando o tamanho do texto (Limite do Instagram -> 2200; Limite do Twiter -> 280)
            if item.upper() != 'NAN':
                contador = 0
                configuracoes = []
                while contador < numImagensComOMesmoTexto:
                    dimensoes, corDaFonte, corDoPlanoDeFundo, margem, alinhamento, fonte, sombra, tamanhoDaFonte, espacamento, angulo, anguloOriginal, textoAjustado = configuracaoAleatoria(OS, indice, len(item), item, configuracaoDeGeracao)
                    configuracao = [dimensoes, corDaFonte, corDoPlanoDeFundo, margem, alinhamento, fonte, sombra, tamanhoDaFonte, espacamento, angulo]
                    if configuracao not in configuracoes:
                        configuracoes.append(configuracao)
                        if textoAjustado != False:
                            criaConjuntoDeDadosAleatorio(OS, caminho, dimensoes, corDoPlanoDeFundo, fonte, corDaFonte, sombra, tamanhoDaFonte, espacamento, textoAjustado, margem, alinhamento, angulo, anguloOriginal, indice, configuracaoDeGeracao, listaDeFatosVerificados)
                            contador = auxiliar.contaArquivos(OS, caminho, indice)
    print('\n' + '_' * 20 + ' FIM DA EXECUÇÃO DA THREAD ' + '_' * 20 + '\n')

def processaManual(OS, diretorio, listaDeTextos, dataset, angulo, dimensoes, fonte, sombra, corDaFonte, corDoPlanoDeFundo, tamanhoDaFonte, listaDeFatosVerificados):                                                       # Produz imagens com configuração aleatória
    print('\n' + '_' * 20 + ' GERANDO IMAGENS ' + '_' * 20 + '\n')
    limiteDeCaracteres = config.getLimiteDeCaracteres()
    caminho = diretorio
    configuracaoDeGeracao = 'MANUAL'
    for item in listaDeTextos:
        indice = dataset.index(item)
        if len(item) <= limiteDeCaracteres:                                               #Limitando o tamanho do texto (Limite do Instagram -> 2200; Limite do Twiter -> 280)
            if item.upper() != 'NAN':
                margemAux, alinhamentoAux, espacamentoAux, anguloAux, anguloOriginalAux, textoAjustadoAux = configuracaoManual(OS, indice, len(item), item, angulo, dimensoes, fonte, sombra, corDaFonte, corDoPlanoDeFundo, tamanhoDaFonte, configuracaoDeGeracao)
                if textoAjustadoAux != False and anguloAux != 'ERRO':
                    criaConjuntoDeDadosManual(OS, caminho, dimensoes, corDoPlanoDeFundo, fonte, corDaFonte, sombra, tamanhoDaFonte, espacamentoAux, textoAjustadoAux, margemAux, alinhamentoAux, anguloAux, anguloOriginalAux, indice, configuracaoDeGeracao, listaDeFatosVerificados)
                else:
                    print('ERRO: Não foi possível produzir a imagem com a configuração informada!\nDescartando texto!')
                    print('\n<<<<<<<<<< REGISTRANDO LOG >>>>>>>>>>\n')
                    nomeDoArquivo = str('DATASET - RANDOM' + '/' + '(' + str(indice) +') ' + '-' + str(fonte) + '-' + str(tamanhoDaFonte) + '-' + str(corDaFonte) + '-' + str(sombra) + '-' + str(dimensoes) + '-' + str(anguloAux) + config.getExtensaoDaImagem())
                    logs = open('Logs - textos descartados.txt', 'a')
                    logs.write(nomeDoArquivo + '\n')
                    logs.close()
    print('\n' + '_' * 20 + ' FIM DA EXECUÇÃO DA THREAD ' + '_' * 20 + '\n')

#____________________________________________________________________________ Estado de Geração _________________________________________________________________________________________________________________________

def aleatorio(OS, diretorio, numImagensComOMesmoTexto):
    numProcessos = config.getNumeroDeProcessos()                      # Número de threads
    auxiliar.deletaDiretorio(diretorio)
    dataset = auxiliar.carregaDataset()
    label = 'claimReviewed'
    labelVerificacaoDeFatos = 'alternativeName'
    listaDeFatosVerificados = []
    listaDeTextos = []
    for item in dataset[label]:
        listaDeTextos.append(str(item))
    for item in dataset[labelVerificacaoDeFatos]:
        fato = str(item)
        fato = fato.upper()
        listaDeFatosVerificados.append(fato)
    dataset = listaDeTextos.copy()
    listaDeTrabalhos = auxiliar.divideDataset(listaDeTextos, numProcessos)
    pool = ThreadPool(processes = numProcessos)
    threads = []
    for job in listaDeTrabalhos:
        async_result = pool.apply_async(processaAleatorio, (OS, job, numImagensComOMesmoTexto, dataset, listaDeFatosVerificados, )) # Semente random não funciona, processa mais rápido
        #async_result = pool.apply(processaAleatorio, (OS, job, numImagensComOMesmoTexto, dataset, listaDeFatosVerificados, )) # Semente random funciona
        threads.append(async_result)
    letters_list = [result.get() for result in threads]

def todasCombinacoesMenorEMaiorTextos(OS, diretorio):                            # Produz todas as combinações de imagens para o menor e o maior textos 
    dataset = auxiliar.carregaDataset()
    label = 'claimReviewed'
    labelVerificacaoDeFatos = 'alternativeName'
    listaDeFatosVerificados = []
    listaDeTextos = []
    for item in dataset[label]:
        listaDeTextos.append(str(item))
    processaMenorEMaiorTexto(OS, diretorio, listaDeTextos)

def todasCombinacoes(OS, diretorio):                                             # Produz todas as combinações de imagens
    dataset = auxiliar.carregaDataset()
    label = 'claimReviewed'
    labelVerificacaoDeFatos = 'alternativeName'
    listaDeFatosVerificados = []
    limite = int(len(dataset) * 0.1)                                  # Usa apenas 10% do dataset
    listaDeTextos = []
    cont = 0
    for item in dataset[label]:
        listaDeTextos.append(str(item))
        cont += 1
        if cont == limite:
            break
    cont = 0
    for item in dataset[labelVerificacaoDeFatos]:
        fato = str(item)
        fato = fato.upper()
        listaDeFatosVerificados.append(fato)
        cont += 1
        if cont == limite:
            break
    dataset = listaDeTextos.copy()
    processaTodasCombinacoes(OS, diretorio, listaDeTextos, dataset)

def manual(OS, diretorio):
    numProcessos = config.getNumeroDeProcessos()                      # Número de threads
    auxiliar.deletaDiretorio(diretorio)
    dataset = auxiliar.carregaDataset()
    label = 'claimReviewed'
    labelVerificacaoDeFatos = 'alternativeName'
    listaDeFatosVerificados = []
    listaDeTextos = []
    for item in dataset[label]:
        listaDeTextos.append(str(item))
    for item in dataset[labelVerificacaoDeFatos]:
        fato = str(item)
        fato = fato.upper()
        listaDeFatosVerificados.append(fato)
    dataset = listaDeTextos.copy()
    listaDeTrabalhos = auxiliar.divideDataset(listaDeTextos, numProcessos)
    angulo, dimensoes, fonte, sombra, corDaFonte, corDoPlanoDeFundo, tamanhoDaFonte = config.getElementosQueVariam()
    # OBS.: A sombra é uma variável booleana, portanto não poderá fazer parte da verificação abaixo, a variável angulo também deve ser observada, pois se o ângulo escolhido for 0 e a variável não for tratada, ela poderá ser reconhecida como booleana e executar operações indevidas.
    if (type(angulo) == int and type(dimensoes) == tuple and type(fonte) == str and type(sombra) == bool and type(corDaFonte) == tuple and (type(corDoPlanoDeFundo) == tuple or type(corDoPlanoDeFundo) == str) and type(tamanhoDaFonte) == int):
        pool = ThreadPool(processes = numProcessos)
        threads = []
        for job in listaDeTrabalhos:
            async_result = pool.apply_async(processaManual, (OS, diretorio, job, dataset, angulo, dimensoes, fonte, sombra, corDaFonte, corDoPlanoDeFundo, tamanhoDaFonte, listaDeFatosVerificados, ))
            threads.append(async_result)
        letters_list = [result.get() for result in threads]
    else:
        print('ERRO: Configuração inválida!')

def configuracaoPadraoVariavel(OS, diretorio, angulo, dimensoes, fonte, sombra, corDaFonte, corDoPlanoDeFundo, tamanhoDaFonte):
    numProcessos = config.getNumeroDeProcessos()                      # Número de threads
    dataset = auxiliar.carregaDataset()
    label = 'claimReviewed'
    labelVerificacaoDeFatos = 'alternativeName'
    listaDeFatosVerificados = []
    listaDeTextos = []
    for item in dataset[label]:
        listaDeTextos.append(str(item))
    for item in dataset[labelVerificacaoDeFatos]:
        fato = str(item)
        fato = fato.upper()
        listaDeFatosVerificados.append(fato)
    if diretorio == 'PADRÃO MAIÚSCULA':
        listaDeTextos = [texto.upper() for texto in listaDeTextos]
    dataset = listaDeTextos.copy()
    listaDeTrabalhos = auxiliar.divideDataset(listaDeTextos, numProcessos)
    # OBS.: A sombra é uma variável booleana, portanto não poderá fazer parte da verificação abaixo, a variável angulo também deve ser observada, pois se o ângulo escolhido for 0 e a variável não for tratada, ela poderá ser reconhecida como booleana e executar operações indevidas.
    if (type(angulo) == int and type(dimensoes) == tuple and type(fonte) == str and type(sombra) == bool and type(corDaFonte) == tuple and (type(corDoPlanoDeFundo) == tuple or type(corDoPlanoDeFundo) == str) and type(tamanhoDaFonte) == int):
        pool = ThreadPool(processes = numProcessos)
        threads = []
        for job in listaDeTrabalhos:
            async_result = pool.apply_async(processaManual, (OS, diretorio, job, dataset, angulo, dimensoes, fonte, sombra, corDaFonte, corDoPlanoDeFundo, tamanhoDaFonte, listaDeFatosVerificados, ))
            threads.append(async_result)
        letters_list = [result.get() for result in threads]
    else:
        print('ERRO: Configuração inválida!')

def padraoVariavel(OS, diretorio):
    dir1 = 'PADRÃO VARIANDO SOMBRA'
    dir2 = 'PADRÃO VARIANDO TAMANHO DA FONTE'
    dir3 = 'PADRÃO VARIANDO ESTILO DA FONTE'
    dir4 = 'PADRÃO VARIANDO PLANO DE FUNDO'
    dir5 = 'PADRÃO VARIANDO COR DA FONTE'
    dir6 = 'PADRÃO VARIANDO DIMENSÕES'
    dir7 = 'PADRÃO VARIANDO ÂNGULO'
    dir8 = 'PADRÃO MAIÚSCULA'
    listaDeDiretorios = [dir1, dir2, dir3, dir4, dir5, dir6, dir7]
    for diretorio in listaDeDiretorios:
        auxiliar.deletaDiretorio(diretorio)
        angulo, dimensoes, fonte, sombra, corDaFonte, corDoPlanoDeFundo, tamanhoDaFonte = config.getConfiguracaoPadrao()
        estadoDeGeracao = diretorio
        if diretorio == dir1:
            for sombra in config.getSombra():
                configuracaoPadraoVariavel(OS, diretorio, angulo, dimensoes, fonte, sombra, corDaFonte, corDoPlanoDeFundo, tamanhoDaFonte)
        elif diretorio == dir2:
            for tamanhoDaFonte in config.getTamanhosDaFonte():
                configuracaoPadraoVariavel(OS, diretorio, angulo, dimensoes, fonte, sombra, corDaFonte, corDoPlanoDeFundo, tamanhoDaFonte)
        elif diretorio == dir3:
            for fonte in config.getListaDeFontes():
                configuracaoPadraoVariavel(OS, diretorio, angulo, dimensoes, fonte, sombra, corDaFonte, corDoPlanoDeFundo, tamanhoDaFonte)
        elif diretorio == dir4:
            for corDoPlanoDeFundo in config.getPaletaDeCores():
                configuracaoPadraoVariavel(OS, diretorio, angulo, dimensoes, fonte, sombra, corDaFonte, corDoPlanoDeFundo, tamanhoDaFonte)
            for corDoPlanoDeFundo in config.getPlanoDeFundo():
                configuracaoPadraoVariavel(OS, diretorio, angulo, dimensoes, fonte, sombra, corDaFonte, corDoPlanoDeFundo, tamanhoDaFonte)
        elif diretorio == dir5:
            for corDaFonte in config.getPaletaDeCores():
                if corDaFonte == corDoPlanoDeFundo:
                    print('ERRO: Cor da fonte igual à cor do plano de fundo, ignorando configuração!')
                else:
                    configuracaoPadraoVariavel(OS, diretorio, angulo, dimensoes, fonte, sombra, corDaFonte, corDoPlanoDeFundo, tamanhoDaFonte)
        elif diretorio == dir6:
            for dimensoes in config.getDimensoes():
                configuracaoPadraoVariavel(OS, diretorio, angulo, dimensoes, fonte, sombra, corDaFonte, corDoPlanoDeFundo, tamanhoDaFonte)
        elif diretorio == dir7:
            for angulo in config.getAngulosDeRotacao():
                configuracaoPadraoVariavel(OS, diretorio, angulo, dimensoes, fonte, sombra, corDaFonte, corDoPlanoDeFundo, tamanhoDaFonte)
        elif diretorio == dir8:
            configuracaoPadraoVariavel(OS, diretorio, angulo, dimensoes, fonte, sombra, corDaFonte, corDoPlanoDeFundo, tamanhoDaFonte)
#________________________________________________________________________________________________________________________________________________________________________________________________________________________
def menu():                                                            # Exibe as opções de geração do dataset
    escolha = 0
    numImagensComOMesmoTexto = 0
    print('\n' + 62 * '_' + ' MENU ' + 62 * '_')
    print('\n (1) DATASET - RANDOM -> Gera um dataset com configuração aleatória para as imagens\n (2) DATASET - COMB MIN and MAX -> Gera um dataset com todas as combinações possíveis de configuração para o menor e o maior textos\n (3) DATASET - COMB ALL -> Gera um dataset com todas as combinações possíveis de configuração de imagem para cada amostra de texto\n (4) DATASET - MANUAL -> Gera um dataset com configuração manual\n (5) DATASET - PADRÃO VARIÁVEL\n (6) Sair')
    print(130 * ('_'))
    while escolha < 1 or escolha > 6:
        escolha = int(input(' Informe o código da opção desejada: '))
    print(130 * ('-'))
    if escolha == 1:
        diretorio = 'DATASET - RANDOM'
        limInferior = 1     # Número mínimo de imagens com o mesmo texto
        limSuperior = 8232  # Número máximo de imagens com o mesmo texto = Todas as possibilidades de geração com o maior texto = 8232 imagens
        while numImagensComOMesmoTexto < limInferior or numImagensComOMesmoTexto > limSuperior:
            numImagensComOMesmoTexto = int(input(' Informe a quantidade de imagens que deseja gerar por amostra de texto. Intervalo [%d - %d]: '%(limInferior, limSuperior)))
        return diretorio, numImagensComOMesmoTexto
    elif escolha == 2:
        diretorio = 'DATASET - COMB MIN and MAX'
        return diretorio, numImagensComOMesmoTexto
    elif escolha == 3:
        diretorio = 'DATASET - COMB ALL'
        return diretorio, numImagensComOMesmoTexto
    elif escolha == 4:
        diretorio = 'DATASET - MANUAL'
        return diretorio, numImagensComOMesmoTexto
    elif escolha == 5:
        diretorio = 'DATASET - PADRÃO VARIÁVEL'
        return diretorio, numImagensComOMesmoTexto
    elif escolha == 6:
        return False, numImagensComOMesmoTexto

def gerador(diretorio, numImagensComOMesmoTexto):                 # Produz o dataset
    OS = config.getPlataforma()
    if OS != 'Windows' and OS != 'Linux':
        print('\n' + 67 * '_' + '\n' + '\n| ERRO - O gerador não oferece suporte ao seu Sistema Operacional |\n' + 67 * '_' + '\n')
        return False
    elif diretorio == 'DATASET - RANDOM':
        aleatorio(OS, diretorio, numImagensComOMesmoTexto)
    elif diretorio == 'DATASET - COMB MIN and MAX':
        todasCombinacoesMenorEMaiorTextos(OS, diretorio)    # Produz todas as combinações de imagens para o menor e o maior textos
    elif diretorio == 'DATASET - COMB ALL':
        todasCombinacoes(OS, diretorio)
    elif diretorio == 'DATASET - MANUAL':
        manual(OS, diretorio)
    elif diretorio == 'DATASET - PADRÃO VARIÁVEL':
        padraoVariavel(OS, diretorio)
    else:
        return False
#________________________________________________________________________________________________________________________________________________________________________________________________________________________
def main():                                                             # Chamada principal
    estadoDeGeracao, numImagensComOMesmoTexto = menu()
    auxiliar.deletaArquivo('./', 'Logs - textos descartados.txt')       # Deleta o arquivo de logs
    auxiliar.deletaArquivo('./', 'Logs - configurações impossíveis.txt')
    if estadoDeGeracao == False:
        return
    else:
        start = time.time()
        inicio = time.process_time()    # Mede o tempo de processo na CPU
        gerador(estadoDeGeracao, numImagensComOMesmoTexto)
        fim = time.process_time()
        end = time.time()
        tempoDeExecucaoNaCPU = fim - inicio
        tempoSimples = end - start
        print('Tempo de execução na CPU: ', tempoDeExecucaoNaCPU, ' segundos')
        print('Tempo de execução com cronômetro simples: ', tempoSimples, ' segundos')
        resultados = open('Relatório de execução do Gerador de Imagens.txt', 'w')
        relatorio = 'Tempo de execução na CPU: ' + str(tempoDeExecucaoNaCPU) + ' segundos' + '\nTempo de execução com cronômetro simples: ' + str(tempoSimples) + ' segundos'
        resultados.write(relatorio)
        resultados.close()

main()