'''
_________________________________________________________________________________________________________________________________
|                                                                                                                               |
|********************************************************** DESCRIÇÃO **********************************************************|
|_______________________________________________________________________________________________________________________________|
| Neste arquivo se encontram todas as funções responsáveis pelo levantamento estatístico do dataset.                            |
|                                                                                                                               |
|                                                               Autor: Yago José Araújo dos Santos. Contato: yago.santos@ufv.br |
|_______________________________________________________________________________________________________________________________|
'''

import auxiliar
import configuracoes as config
from collections import Counter
import os
import configuracoes as config

def salvaDados(caminho, nomeArquivo, lista, listaDeReferencia, tamanhoDoDataset):
    d = Counter(lista)
    arquivo = caminho + nomeArquivo + '.txt'
    saida = open(arquivo, 'w')
    for item in listaDeReferencia:
        porcentagem = (d[item] / tamanhoDoDataset) * 100
        resultado = 'O item: (' + str(item) + ') ocorreu ' + str(d[item]) + ' vezes. O equivalente a: ' + str(porcentagem) + '%\n'
        saida.write(resultado)
    saida.close()

def listaArquivos(pasta):
    extensao = config.getExtensaoDaImagem()
    caminhos = [os.path.join(pasta, nome) for nome in os.listdir(pasta)]
    arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
    jpgs = [arq for arq in arquivos if arq.lower().endswith(extensao)]
    return jpgs

def levantaDados(OS, caminho, pasta):
    listaDeArquivos = listaArquivos(pasta)
    tamanhoDoDataset = len(listaDeArquivos)
    indices = []
    fontes = []
    tamanhosDeFonte = []
    coresDeFonte = []
    sombras = []
    planosDeFundo = []
    dimensoesDasImagens = []
    angulos = []
    checagensDeFatos = []
    cont = 0
    for arquivo in listaDeArquivos:
        print('Processando arquivo (%d) de (%d) ...' %(cont, len(listaDeArquivos)))
        cont += 1
        #Este trecho extrai a regex sem a extensão do arquivo e o caminho
        aux = arquivo
        if OS == 'Windows':
            aux = aux.split('\\')              # Windows
        elif OS == 'Linux':
            aux = aux.split('/')               # Linux
        aux = os.path.splitext(aux[1])
        regex = aux[0]
        indice, fonte, tamanhoDaFonte, corDaFonte, sombra, planoDeFundo, dimensoes, angulo, checagemDeFatos = config.getDadosDaRegex(regex)
        indices.append(indice)
        fontes.append(fonte)
        tamanhosDeFonte.append(tamanhoDaFonte)
        coresDeFonte.append(corDaFonte)
        sombras.append(sombra)
        planosDeFundo.append(planoDeFundo)
        dimensoesDasImagens.append(dimensoes)
        angulos.append(angulo)
        checagensDeFatos.append(checagemDeFatos)
    # Dados dos nomes das fontes
    listaDeReferencia = []
    listaDeFontes = config.getListaDeFontes()
    for fonte in listaDeFontes:
        nomeDaFonte = os.path.splitext(fonte)[0]
        nomeDaFonte = nomeDaFonte.split('/')
        nomeDaFonte = nomeDaFonte[2]
        listaDeReferencia.append(nomeDaFonte)
    salvaDados(caminho, 'Fonte', fontes, listaDeReferencia, tamanhoDoDataset)
    # Dados dos tamanhos de fonte
    listaDeReferencia = config.getTamanhosDaFonte()
    salvaDados(caminho, 'Tamanho da fonte', tamanhosDeFonte, listaDeReferencia, tamanhoDoDataset)
    # Dados das cores de fonte
    listaDeReferencia = config.getPaletaDeCores()
    salvaDados(caminho, 'Cor da fonte', coresDeFonte, listaDeReferencia, tamanhoDoDataset)
    # Dados das sombras
    listaDeReferencia = config.getSombra()
    salvaDados(caminho, 'Sombras', sombras, listaDeReferencia, tamanhoDoDataset)
    # Dados da checagem de fatos
    listaDeReferencia = config.getChecagemDeFatos()
    salvaDados(caminho, 'Checagem de fatos', checagensDeFatos, listaDeReferencia, tamanhoDoDataset)
    # Dados dos planos de fundo
    nomeDosPlanosDeFundo = ['im1', 'im2']
    listaDeReferencia = config.getPaletaDeCores()
    listaDeReferencia.append(nomeDosPlanosDeFundo[0])
    listaDeReferencia.append(nomeDosPlanosDeFundo[1])
    salvaDados(caminho, 'Planos de fundo', planosDeFundo, listaDeReferencia, tamanhoDoDataset)
    # Dados das dimensões de imagem
    listaDeReferencia = config.getDimensoes()
    salvaDados(caminho, 'Dimensões', dimensoesDasImagens, listaDeReferencia, tamanhoDoDataset)
    # Dados dos ângulos de rotação
    listaDeReferencia = config.getAngulosDeRotacao()
    salvaDados(caminho, 'Angulos', angulos, listaDeReferencia, tamanhoDoDataset)

def getPasta():
    escolha = 0
    limInferior = 1
    limSuperior = 6
    listaDeDiretorios = os.listdir('./')
    print(28 * '_' + ' MENU ' + 28 * '_')
    print('\n (1) DATASET - RANDOM')
    print(' (2) DATASET - COMB MIN and MAX')
    print(' (3) DATASET - COMB ALL')
    print(' (4) DATASET - MANUAL')
    print(' (5) Informar o nome do dataset')
    print(' (6) Sair')
    print(62 * ('_'))
    while escolha < limInferior or escolha > limSuperior:
        escolha = int(input(' Informe o código do dataset que deseja levantar os dados: '))
    print(62 * ('-'))
    if escolha == 1:
        pasta = 'DATASET - RANDOM'
        return pasta
    elif escolha == 2:
        pasta = 'DATASET - COMB MIN and MAX'
        return pasta
    elif escolha == 3:
        pasta = 'DATASET - COMB ALL'
        return pasta
    elif escolha == 4:
        pasta = 'DATASET - MANUAL'
        return pasta
    elif escolha == 5:
        pasta = input('Digite o nome do diretório que deseja usar: ')
        if pasta in listaDeDiretorios:
            return pasta
    elif escolha == 6:
        return False

def getCaminho(pasta):
    OS = config.getPlataforma()
    if OS != 'Windows' and OS != 'Linux':
        print('\n' + 67 * '_' + '\n' + '\n| ERRO - O gerador não oferece suporte ao seu Sistema Operacional |\n' + 67 * '_' + '\n')
        return False
    elif OS == 'Windows':
        caminho = 'Estatisticas do dataset (' + pasta + ')\\'                  # Windows
        return caminho
    elif OS == 'Linux':
        caminho = 'Estatisticas do dataset (' + pasta + ')/'                   # Linux
        return caminho

def main():
    pasta = getPasta()
    if pasta == False: return
    caminho = getCaminho(pasta)
    if caminho == False: return
    OS = config.getPlataforma()
    auxiliar.deletaDiretorio('Estatisticas do dataset (' + pasta + ')')
    auxiliar.cria_diretorio('Estatisticas do dataset (' + pasta + ')')
    print('======== INICIANDO ========')
    print('        Analisando...      ')
    levantaDados(OS, caminho, pasta)
    print('____ Análise concluída! ____')

main()