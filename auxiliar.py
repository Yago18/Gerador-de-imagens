'''
_________________________________________________________________________________________________________________________________
|                                                                                                                               |
|********************************************************** DESCRIÇÃO **********************************************************|
|_______________________________________________________________________________________________________________________________|
| Neste arquivo se encontram todas as funções auxiliares do gerador de imagens.                                                 |
|                                                                                                                               |
|                                                               Autor: Yago José Araújo dos Santos. Contato: yago.santos@ufv.br |
|_______________________________________________________________________________________________________________________________|
'''

import os
import pandas as pd
import math
import shutil
import PIL
from PIL import Image
from PIL import ImageFilter
from PIL import ImageFont
from PIL import ImageDraw
import configuracoes as config

def carregaDataset():                                                                   # Carrega o dataset
    file_name = 'Dataset/FACTCKBR'
    dataset = pd.read_csv(file_name + ".tsv", sep='\t', index_col=0)
    #print(dataset.head(11))
    #print('Rótulos do dataset:', dataset.dtypes)
    return dataset

def cria_diretorio(nome):                                                               # Cria um diretório
    diretorio = nome
    if os.path.isdir(diretorio) != True:                                                # Verifica se o diretório já existe
        os.mkdir(diretorio)

def determinaOMenorEOMaiorTexto(listaDeTextos, limiteDeCaracteres):                     # Determina o maior e o menor elemnto do conjunto de dados
    menor = 9999999
    maior = 0
    indice = 0
    for item in listaDeTextos:
        if str(item).upper() != 'NAN' and len(str(item)) <= limiteDeCaracteres:
            if len(str(item)) > maior:
                maior = len(str(item))
                maiorTexto = item
                indiceMaior = indice
            if len(str(item)) < menor:
                menor = len(str(item))
                menorTexto = item
                indiceMenor = indice
        indice += 1
    return indiceMenor, indiceMaior

def deletaDiretorio(caminho):                                                           # Deleta diretório
    if os.path.exists(caminho) == True:
        shutil.rmtree(caminho)
    else:
        return

def deletaArquivo(caminho, nomeDoArquivo):
    dir = os.listdir(caminho)
    for file in dir:
        if file == nomeDoArquivo:
            os.remove(file)

def listaArquivos(caminho):                                                             # Retorna uma lista de arquivos da extensão informada
    pasta = caminho
    caminhos = [os.path.join(pasta, nome) for nome in os.listdir(pasta)]
    arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
    jpgs = [arq for arq in arquivos if arq.lower().endswith(".jpg")]
    return jpgs

def contaArquivos(OS, caminho, indiceVerificado):                                       # Retorna a quantidade de arquivos produzidos com o índice verificado
    listaDeArquivos = listaArquivos(caminho)
    cont = 0
    for arquivo in listaDeArquivos:
        #Este trecho extrai a regex sem a extensão do arquivo e o caminho
        aux = arquivo
        if OS == 'Windows':
            aux = aux.split('\\')              # Windows
        elif OS == 'Linux':
            aux = aux.split('/')               # Linux
        aux = os.path.splitext(aux[1])
        regex = aux[0]
        indice, fonte, tamanhoDaFonte, corDaFonte, sombra, planoDeFundo, dimensoes, angulo, checagemDeFatos = config.getDadosDaRegex(regex)
        if indice == indiceVerificado:
            cont += 1        
    return cont                             # Quantidade de arquivos com o mesmo texto

def divideDataset(lista, numProcessos):                                            # Divide o dataset para o processamento paralelo
    if len(lista) >= 4:
        tamanho = math.ceil(len(lista) / numProcessos)
        listaDeTrabalhos = []
        aux = []
        cont = 0
        while len(lista) != 0:
            if cont < tamanho:
                aux.append(lista[0])
                del lista[0]
            elif cont == tamanho and len(lista) != 0:
                listaDeTrabalhos.append(aux)
                aux = []
                cont = 0
                aux.append(lista[0])
                del lista[0]
            if len(lista) == 0:
                listaDeTrabalhos.append(aux)
                aux = []
            cont += 1
        return listaDeTrabalhos
    else:
        listaDeTrabalhos = []
        listaDeTrabalhos.append(lista)
        return listaDeTrabalhos