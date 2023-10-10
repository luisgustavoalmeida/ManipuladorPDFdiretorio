#import io
#from tkinter import *
import re                           # expreçoes regulares
#from dateutil import parser


# manipular pdf
import datetime
import locale

import PyPDF2
from PyPDF2 import PdfReader, PdfWriter
import os
from pathlib import Path
#import shutil
import locale
locale.setlocale(locale.LC_TIME, 'portuguese')
#locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
# linguagem = locale.getlocale()
# print(linguagem)
# locale.setlocale(locale.LC_ALL, linguagem[0])


def extrair_data(data_texto):
    # Converte o texto para minúsculo
    data_texto = data_texto.lower()

    # Verifica se o texto contém a palavra "de"
    if re.search("de", data_texto) != None:
        # Remove espaços em branco desnecessários
        data_texto = data_texto.replace(" ", "")
        # Adiciona um espaço após a palavra "de"
        data_texto = data_texto.replace(",", ", ")
        data_texto = data_texto.replace("de", " de ")
        # Corrige um problema com a data "dezembro"
        data_texto = data_texto.replace("de ze", "deze")

    # Remove espaços em branco duplicados
    data_texto = re.sub(r"\s{2,}", " ", data_texto)
    print("data texto na fonção", data_texto)

    # Lista de padrões de datas
    padroes_data = [
        r"(\d{1,2}) de (\w+) de (\d{2,4})",     # Ex: 1 de Janeiro de 2022
        r"(\d{1,2})/(\d{1,2})/(\d{2,4})",       # Ex: 01/01/22
        r"(\d{2,4})-(\d{1,2})-(\d{1,2})",       # Ex: 2022-01-01
        r"(\w{3}) (\d{2}), (\d{4})",            # Ex: Jan 01, 2022
        r"(\d{2}) (\w{3}) (\d{4})",             # Ex: 01 Jan 2022
        r"(\d{2}) (\w{3}) (\d{2})",             # Ex: 01 Jan 22
        r"(\d{4}) (\w{3}) (\d{2})",             # Ex: 2022 Jan 01
        r'(\d{1,2}) (\w{3})/(\d{4})',           # Ex: 01 Jan/2022
        r'(\d{2}\w{3}/\d{4})'                   # Ex: 01Jan/2022
    ]

    for padrao_data in padroes_data:
        # Procura por uma data no texto com base no padrão atual
        for match in re.finditer(padrao_data, data_texto):
            encontrado_data = match.group()
            grupos = match.groups()
            qtde_grupos = len(grupos)

            print(grupos)
            print(qtde_grupos)
            #print(len(grupos[0]))
            #print(len(grupos[1]))
            #print(len(grupos[2]))

            print("DATA ENCONTRADA", encontrado_data)

            if qtde_grupos == 1:
                if len(grupos[0]) == 10:
                    # '%d/%m/%Y'
                    formato = '%d%b/%Y'
                    print('formato 6')
                data = datetime.datetime.strptime(encontrado_data, formato).date()
                return data

            else:

                if len(grupos[1]) >= 4 and len(grupos[2]) == 4 and grupos[1].isdigit() == False:
                    # '%d de %B de %Y'
                    formato = '%d de %B de %Y'
                    print('formato 1')
                elif len(grupos[1]) >= 4 and len(grupos[2]) == 2 and grupos[1].isdigit() == False:
                    # '%d de %B de %y'
                    formato = '%d de %B de %y'
                    print('formato 2')
                elif len(grupos[1]) == 2 and len(grupos[2]) == 4 and grupos[1].isdigit() == True:
                    # '%d/%m/%Y'
                    formato = '%d/%m/%Y'
                    print('formato 3')
                elif len(grupos[1]) == 2 and len(grupos[2]) == 2 and grupos[1].isdigit() == True:
                    # '%d/%m/%Y'
                    formato = '%d/%m/%y'
                    print('formato 4')
                elif len(grupos[1]) == 3 and len(grupos[2]) == 4 and grupos[1].isdigit() == False:
                    # '%d/%m/%Y'
                    formato = '%d %b/%Y'
                    print('formato 5')
                else:
                    # '%d %B %Y'
                    formato = '%d%m%Y'
                    print('formato 7')
                data = datetime.datetime.strptime(encontrado_data, formato).date()
                return data

    return None


def selecao_caminho(): #
    # identifica a pasta Download dentro no ususrio e ler todos os arquivos e identificar oque sao do tipo .pdf
    caminho = os.path.expanduser("~")  #busca o usuario do computador
    pasta = Path( caminho + "/Downloads") #cria o diretorio pasta
    #print(pasta)
    caminho_do_arquivo = []
    arquivo_a_mover = []

    for diretorio, subpastas, arquivos in os.walk(pasta):
        #print(diretorio)
        #print(subpastas)
        #print(arquivos)

        for arquivo in arquivos:
            #print(arquivo)
            #print(os.path.join(diretorio, arquivo))
            #caminho_do_arquivo.append(os.path.join(diretorio, arquivo))
            #print(caminho_do_arquivo)
            separa_tupla = os.path.splitext(arquivo) # sepra em um tupla o nome do arquivo e a exteção para poder identificar o tipo PDF
            #print("Tupla: ",separa_tupla)
            #arquivo_nome = separa_tupla[0]
            arquivo_extensao = separa_tupla[1]
            if arquivo_extensao == '.pdf': # testa se é do tipo .pdf
                #print(os.path.join(diretorio, arquivo))
                #print("Nome do arquivo: ", arquivo_nome)
                #print("Extesão do arquivo: ", arquivo_extensao)
                arquivo_a_mover.append(arquivo)
                caminho_do_arquivo.append(os.path.join(diretorio, arquivo)) # junta o diretorio com o nome do arquivo e guarda em uma lista para alimenta a saida da função
                #so_caminho_do_arquivo.append(diretorio)

    #print(caminho_do_arquivo)
    lista_arquivos_pdf = str("Existem " + str(len(caminho_do_arquivo)) + " arquivos do tipo '.pdf'")
    #print(lista_arquivos_pdf)
    return (caminho_do_arquivo)

def identificar_caderno(caminho_do_arquivo):

    # para criara as listas de estados e siglas
    nome_estado = ['Acre','Alagoas','Amapá','Amazonas','Bahia','Ceará','Espirito Santo','Goiás','Maranhão','Mato Grosso',
                   'Mato Grosso do Sul','Minas Gerais','Pará','Paraiba','Paraná','Pernambuco','Piauí','Rio de Janeiro',
                   'Rio Grande do Norte','Rio Grande do Sul','Rondonia','Roraima','Santa Catarina','São Paulo','Sergipe',
                   'Tocantis','Distrito Federal']
    sigla_estado =['AC','AL','AP','AM','BA','CE','ES','GO','MA','MT',
                   'MS','MG','PA','PB','PR','PE','PI','RJ','RN',
                   'RS','RO','RR','SC','SP','SE',
                   'TO','DF']
    estado_sigla = dict(zip(nome_estado, sigla_estado)) # cria um dicionario com nome do estado e sigla

    #estado_sigla = {'Acre': 'AC', 'Alagoas': 'AL', 'Amapá': 'AP', 'Amazonas': 'AM', 'Bahia': 'BA', 'Ceará': 'CE',\
    # 'Espirito Santo': 'ES', 'Goiás': 'GO', 'Maranhão': 'MA', 'Mato Grosso': 'MT', 'MatoGrosso do Sul': 'MS', \
    # 'Minas Gerais': 'MG', 'Pará': 'PA', 'Paraiba': 'PB', 'Paraná': 'PR', 'Pernambuco': 'PE', 'Piauí': 'PI', \
    # 'Rio de Janeiro': 'RJ', 'Rio Grande do Norte': 'RN', 'Rio Grande do Sul': 'RS', 'Rondonia': 'RO', 'Roraima': 'RR',\
    # 'Santa Catarina': 'SC', 'São Paulo': 'SP', 'Sergipe': 'SE', 'Tocantis': 'TO', 'Distrito Federal': 'DF'}
    #print(estado_sigla)

    # listas de tribunais
    lista_tribunais = ['Diário da Justiça Eletrônico do Tribunal Regional Eleitoral d',
                       'DIÁRIO DA JUSTIÇA ELETRÔNICO DO ESTADO DO RIO GRANDE DO SUL',
                       'Diário da Justiça Eletrônico - RS','www.tce.rn.gov.br',
                       'COMPOSIÇÃO DO TRIBUNAL DE JUSTIÇA DO MARANHÃO',
                       'Tribunal de Justiça do Estado de Mato Grosso',
                       'Tribunal de Justiça do Estado do Piauí',
                       'https://diofe.portal.ap.gov.br',
                       'www.imprensaoficial.am.gov.br',
                       ' DA PARAÍBADIÁRIO OFICIAL',
                       'www.diariooficial.rs.gov.br',
                       'Diário Oficial Eletrônico do Tribunal de Contas do Estado da Bahia',
                       'Diário OficialEstado de Goiás',
                       'Diário Oficial Eletrônico Instituido Conforme Lei 7.300',
                       'MARANHÃOTRIBUNAL DE CONTAS DO ESTADODIÁRIO OFICIAL ELETRÔNICO',
                       'doc_tce@tce.mt.gov.br',
                       'Tribunal de Contas do EstadoPernambucoDiário Eletrônico',
                       'DIÁRIO ELETRÔNICO DO TRIBUNAL DE CONTAS DO ESTADO DO PARANÁ',
                       'www.tce.ro.gov.br','https://app.tce.to.gov .br/boletim']

    sigla_tibunais = ['DOTRE','djrs','djrs','TCERN','djma','djmt','dodjpi','DOEAP','DOEAM','DOEPB','doers','TCEBA',
                      'doego','TCEAL','TCEMA','TCEMT','TCEPE','TCEPR','TCERO','TCETO']
    dicionaria_tibunais_siglas = dict(zip(lista_tribunais, sigla_tibunais))
    # cria m dicionario com os nomes dos tribunias e suas siglas

    for iten in caminho_do_arquivo:

        abrindo_pdf = open(iten, 'rb')
        ler_pdf = PyPDF2.PdfReader(abrindo_pdf)
        numero_paginas_pdf = len(ler_pdf.pages)
        print("O pdf tem: ", numero_paginas_pdf , "paginas")

        objeto_pagina0 = ""
        objeto_pagina1 = ""

        objeto_pagina = ler_pdf.pages[0]
        # # print(objeto_pagina.extractText())
        #texto_pdf = objeto_pagina.extract_text()
        #print(texto_pdf)


        if numero_paginas_pdf > 1:
            objeto_pagina0 = ler_pdf.pages[0]
            objeto_pagina1 = ler_pdf.pages[1]
            texto_pdf0 = objeto_pagina0.extract_text() + objeto_pagina1.extract_text()
        else:
            objeto_pagina0 = ler_pdf.pages[0]
            texto_pdf0 = objeto_pagina0.extract_text()

        #print(objeto_pagina0.extractText())


        print('texto')
        #print(texto_pdf0)

        cont_linha = 0
        texto_pdf = ""
        for linha in texto_pdf0.splitlines():
            # print(linha)
            cont_linha = cont_linha + 1
            texto_pdf = str(texto_pdf + linha)
            if cont_linha == 200:
                break

        print('\n \n texto_pdf')
        #print(texto_pdf)
        texto_pdf = re.sub(' +', ' ', texto_pdf) #remove espaços duplicadps
        print(texto_pdf)
        print('\n \n')

        for tribunal in lista_tribunais:
            if re.search( tribunal , texto_pdf) != None:
# ate esta parte é igual para todos os cadernos independente do tribuanal
#######################################################################################################################
# Primeiro caderno da lista
#F:\Work\Diarios\RS\Diário Oficial do TRERS\unica\2022\dezembro\suplementotrers\20221216\ArqsFull
#suplementotrers_20221216
#F:\Work\Diarios\SC\Diário Oficial do TRESC\Unica\2022\dezembro\trescsup\20221216
#DOTRESC_Sup_20221216
                if tribunal == lista_tribunais[0]: #TRE
                    #print(tribunal)
                    for estado in nome_estado:
                        #print(estado)
                        if re.search(estado, texto_pdf) != None:
                            #print(estado)
                            nome_parte4 = ""
                            if re.search("Edição Eleitoral", texto_pdf) != None:
                                nome_parte3 = "Sup_"
                                nome_parte4 = ""
                            elif re.search("Edição Extraordinária", texto_pdf) != None:
                                nome_parte3 = "Sup_"
                                #nome_parte4 = str("_") #para colocar um "_" no final do nome
                            else:
                                nome_parte3 = ""
                                nome_parte4 = ""
                            #if  (re.search('Disponibilização', texto_pdf)) != None:
                            print('tre ok')
                            data_texto = re.split(r"Disponibilização|Publicação",texto_pdf)  # separa a informação entre as palavras
                            data_texto = str(data_texto[1])  # texto depois da disponibilização
                            print("data do tesxto", data_texto)
                            data = extrair_data(data_texto)
                            nome_parte0 = ""
                            #print('parte 0',nome_parte0)
                            nome_parte1 = dicionaria_tibunais_siglas.get(tribunal)
                            #print('parte 1',nome_parte1)
                            nome_parte2 = str(estado_sigla.get(estado)) + "_"
                            #print('parte 2',nome_parte2)
                            #print('parte 3',nome_parte3)
                            nome_parte4 = str((str(data).replace('-', '')) + nome_parte4)
                            #print('parte 4',nome_parte4)
                            #print('\n')
                            abrindo_pdf.close()
                            renomear_arquivo(nome_parte0, nome_parte1, nome_parte2, nome_parte3, nome_parte4, iten)
                            break
                    #break
#######################################################################################################################
# Segundo caderno da lista
                elif (tribunal == lista_tribunais[1]) or (tribunal == lista_tribunais[2]) : #djrs
                    if re.search("ADMINISTRATIVA E JUDICIAL", texto_pdf) != None:
                        nome_parte3 = "AdminJud "
                    elif re.search("Interior 1º Grau", texto_pdf) != None:
                        nome_parte3 = "Int1 "
                    elif re.search("Capital 1º Grau", texto_pdf) != None:
                        nome_parte3 = "Cap1 "
                    elif re.search("Capital 2º Grau", texto_pdf) != None:
                        nome_parte3 = "Cap2 "
                    elif re.search("EDITAIS 1º E 2º GRAU", texto_pdf) != None:
                        nome_parte3 = "Edit1e2 "
                    elif (re.search("Extra", texto_pdf)) or (re.search("EXTRA", texto_pdf)) != None:
                        nome_parte3 = "Extra "
                    else:
                        nome_parte3 = ""
                    #if(re.search('Disponibilização', texto_pdf)) != None:
                    data_texto = re.split(r"Disponibilização: | - Página",texto_pdf)  # separa a informação entre as palavras
                    data_texto = str(data_texto[1])  # texto depois da disponibilização
                    print("data do tesxto", data_texto)
                    data = extrair_data(data_texto)
                    nome_parte0 = ""
                    #print('parte 0', nome_parte0)
                    nome_parte1 = dicionaria_tibunais_siglas.get(tribunal) + " "
                    #print('parte 1', nome_parte1)
                    nome_parte2 = ""
                    #print('parte 2', nome_parte2)
                    #print('parte 3',nome_parte3)
                    nome_parte4 = str(data).replace('-', '')
                    #print('parte 4',nome_parte4)
                    #print('\n')
                    abrindo_pdf.close()
                    renomear_arquivo(nome_parte0, nome_parte1, nome_parte2, nome_parte3, nome_parte4, iten)
                    break
                    #break
#######################################################################################################################
#modelo certo
# terceiro caderno da lista
# F:\Work\Diarios\RN\Diário do Tribunal de Contas do RN\Unica\2023\janeiro\unica
# NOME: TCERN unica 202301
                elif (tribunal == lista_tribunais[3]) :  # djrs
                    #if (re.search('Disponibilização', texto_pdf)) != None:
                    data_texto = re.split(r"Disponibilização, |Tribunal", texto_pdf)# separa a informação entre as palavras
                    data_texto=str(data_texto[1]) # texto depois da disponibilização
                    print("data do tesxto", data_texto)
                    data = extrair_data(data_texto)
                    nome_parte0 = ""
                    #print('parte 0', nome_parte0)
                    nome_parte1 = dicionaria_tibunais_siglas.get(tribunal) + " "
                    #print('parte 1', nome_parte1)
                    nome_parte2 = "unica "
                    #print('parte 2', nome_parte2)
                    nome_parte3 = ""
                    #print('parte 3',nome_parte3)
                    nome_parte4 = str(data).replace('-', '')
                    #print('parte 4',nome_parte4)
                    #print('\n')
                    abrindo_pdf.close()
                    renomear_arquivo(nome_parte0, nome_parte1, nome_parte2, nome_parte3, nome_parte4, iten)
                    break
                    #break
#######################################################################################################################
# quarto caderno da lista
# F:\Work\Diarios\MA\Diário da Justiça do Maranhão\Unica\2022\Dezembro\unica
# djma_Unica_202212
                elif (tribunal == lista_tribunais[4]):
                    #if (re.search('Disponibilização', texto_pdf)) != None:
                    data_texto = re.split(r"Disponibilização : |. Publicação",texto_pdf)  # separa a informação entre as palavras
                    data_texto = str(data_texto[1])  # texto depois da disponibilização
                    print("data do tesxto",data_texto)
                    data = extrair_data(data_texto)
                    nome_parte0 = ""
                    #print('parte 0', nome_parte0)
                    nome_parte1 = dicionaria_tibunais_siglas.get(tribunal) + ""
                    #print('parte 1', nome_parte1)
                    nome_parte2 = "_Unica_"
                    #print('parte 2', nome_parte2)
                    nome_parte3 = ""
                    #print('parte 3',nome_parte3)
                    nome_parte4 = str(data).replace('-', '')
                    #print('parte 4',nome_parte4)
                    abrindo_pdf.close()
                    renomear_arquivo(nome_parte0, nome_parte1, nome_parte2, nome_parte3, nome_parte4, iten)
                    break
                    #break
#######################################################################################################################
# Quinto caderno da lista
# F:\Work\Diarios\MT\Diário da Justiça de Mato Grosso\Unica\2022
# djmt Unica 20221207
                elif (tribunal == lista_tribunais[5]):
                    #if (re.search('DISPONIBILIZADO', texto_pdf)) != None:
                    data_texto = re.split(r"DISPONIBILIZADO | - Edição ",texto_pdf)  # separa a informação entre as palavras
                    data_texto = str(data_texto[1])  # texto depois da disponibilização
                    print("data do tesxto", data_texto)
                    data = extrair_data(data_texto)
                    print("ok")
                    nome_parte0 = ""
                    #print('parte 0', nome_parte0)
                    nome_parte1 = dicionaria_tibunais_siglas.get(tribunal) + ""
                    #print('parte 1', nome_parte1)
                    nome_parte2 = " Unica "
                    #print('parte 2', nome_parte2)
                    nome_parte3 = ""
                    #print('parte 3', nome_parte3)
                    nome_parte4 = str(data).replace('-', '')
                    #print('parte 4', nome_parte4)
                    #print('\n')
                    abrindo_pdf.close()
                    renomear_arquivo(nome_parte0, nome_parte1, nome_parte2, nome_parte3, nome_parte4, iten)
                    break
                    #break
#######################################################################################################################
# DJPI
# F:\Work\Diarios\PI\Diário da Justiça do Piauí\Unica\2022\dezembro\unica
# dodjpi unica 202212
                elif (tribunal == lista_tribunais[6]):
                    #if (re.search('Disponibilização', texto_pdf)) != None:
                    print("ok")
                    data_texto = re.split(r"Disponibilização: | Publicação:", texto_pdf)  # separa a informação entre as palavras
                    data_texto = str(data_texto[1])  # texto depois da disponibilização
                    print("data do tesxto", data_texto)
                    data = extrair_data(data_texto)
                    print("ok")
                    #print(data)
                    nome_parte0 = ""
                    #print('parte 0', nome_parte0)
                    nome_parte1 = dicionaria_tibunais_siglas.get(tribunal) + ""
                    #print('parte 1', nome_parte1)
                    nome_parte2 = " Unica "
                    #print('parte 2', nome_parte2)
                    nome_parte3 = ""
                    #print('parte 3', nome_parte3)
                    nome_parte4 = str(data).replace('-', '')
                    #print('parte 4', nome_parte4)
                    abrindo_pdf.close()
                    renomear_arquivo(nome_parte0, nome_parte1, nome_parte2, nome_parte3, nome_parte4, iten)
                    break
                    #break
#######################################################################################################################
# DOEAP
# F:\Work\Diarios\AP\Diário Oficial do Amapá\Unica\2023\janeiro\unica
# DOEAP Unica 20221201
                elif (tribunal == lista_tribunais[7]):
                    #print("######################################achou caderno 7")
                    #if (re.search('Amapá', texto_pdf)) != None:
                    print("ok")
                    data_texto = re.split(r"Amapá| Ano ", texto_pdf)  # separa a informação entre as palavras
                    data_texto = str(data_texto[1])  # texto depois da disponibilização
                    print("data do tesxto", data_texto)
                    data = extrair_data(data_texto)
                    print("ok")
                    #print(data)
                    nome_parte0 = ""
                    #print('parte 0', nome_parte0)
                    nome_parte1 = dicionaria_tibunais_siglas.get(tribunal) + ""
                    #print('parte 1', nome_parte1)
                    nome_parte2 = " Unica "
                    #print('parte 2', nome_parte2)
                    nome_parte3 = ""
                    #print('parte 3', nome_parte3)
                    nome_parte4 = str(data).replace('-', '')
                    #print('parte 4', nome_parte4)
                    abrindo_pdf.close()
                    renomear_arquivo(nome_parte0, nome_parte1, nome_parte2, nome_parte3, nome_parte4, iten)
                    break
                    #break
#######################################################################################################################
# DOEAM
#F:\Work\Diarios\AM\Diário Oficial do Amazonas\Unica\2023\Janeiro\unica\20230101
#DOEAM unica 20230101
                elif (tribunal == lista_tribunais[8]):
                    #print("######################################achou caderno 8")
                    #if (re.search('estado do amazonas', texto_pdf)) != None:
                    print("ok")
                    data_texto = re.split(r".am.gov.br", texto_pdf)  # separa a informação entre as palavras
                    print("data do tesxto", data_texto)
                    data_texto = data_texto[1][:30]
                    print("data do tesxto", data_texto)
                    data = extrair_data(data_texto)
                    print("ok")
                    #print(data)
                    data = data - datetime.timedelta(1) # data dia anterior
                    #print(data)
                    nome_parte0 = ""
                    # print('parte 0', nome_parte0)
                    nome_parte1 = dicionaria_tibunais_siglas.get(tribunal) + ""
                    # print('parte 1', nome_parte1)
                    nome_parte2 = " unica "
                    # print('parte 2', nome_parte2)
                    nome_parte3 = ""
                    # print('parte 3', nome_parte3)
                    nome_parte4 = str(data).replace('-', '')
                    # print('parte 4', nome_parte4)
                    abrindo_pdf.close()
                    renomear_arquivo(nome_parte0, nome_parte1, nome_parte2, nome_parte3, nome_parte4, iten)
                    break
                    #break
#######################################################################################################################
# DOEPE
#F:\Work\Diarios\PB\Diário Oficial da Paraíba\Cadernos\2023\Janeiro\unica\20230106
# DOEAM unica 20230101
                elif (tribunal == lista_tribunais[9]):
                    #print("######################################achou caderno 9")
                    #if (re.search('ESTADO DA PARAÍBADIÁRIO OFICIAL', texto_pdf)) != None:
                    print("ok")
                    data_texto = re.split(r"João Pessoa - | DA PARAÍBADIÁRIO", texto_pdf)  # separa a informação entre as palavras
                    data_texto = str(data_texto[1])  # texto depois da disponibilização
                    print("data do tesxto", data_texto)
                    data = extrair_data(data_texto)
                    print("ok")
                    data = data - datetime.timedelta(1)  # data dia anterior
                    #print(data)
                    nome_parte0 = ""
                    #print('parte 0', nome_parte0)
                    nome_parte1 = dicionaria_tibunais_siglas.get(tribunal) + " "
                    #print('parte 1', nome_parte1)
                    if (re.search('SUPLEMENTO', texto_pdf)) != None:
                        nome_parte2 = "sup "
                    else:
                        nome_parte2 = "Unica "
                    #print('parte 2', nome_parte2)
                    nome_parte3 = ""
                    #print('parte 3',nome_parte3)
                    nome_parte4 = str(data).replace('-', '')
                    #print('parte 4',nome_parte4)
                    abrindo_pdf.close()
                    renomear_arquivo(nome_parte0, nome_parte1, nome_parte2, nome_parte3, nome_parte4, iten)
                    break
                    #break
#######################################################################################################################
# DOEPE
# F:\Work\Diarios\RS\Diário Oficial do Rio Grande do Sul\Cadernos\2023\Janeiro\unica\20230108
# doers_Unica20230108
                elif (tribunal == lista_tribunais[10]):
                    #if (re.search('Diário Oficial Eletrônicodo Estado do Rio Grande do Sul', texto_pdf)) != None:
                    print("ok")
                    data_texto = re.split(r"Porto Alegre, |ANO ", texto_pdf)  # separa a informação entre as palavras
                    data_texto = str(data_texto[1])  # texto depois da disponibilização
                    print("data do tesxto", data_texto)
                    data = extrair_data(data_texto)
                    print("ok")
                    data = data - datetime.timedelta(1)  # data dia anterior
                    #print(data)
                    nome_parte0 = ""
                    #print('parte 0', nome_parte0)
                    nome_parte1 = dicionaria_tibunais_siglas.get(tribunal)
                    #print('parte 1', nome_parte1)
                    if(re.search('LXXXI', texto_pdf)) != None:
                        nome_parte2 = "_Unica"
                    elif (re.search('L', texto_pdf)) != None:
                        nome_parte2 = "_IndComdoers"
                    elif numero_paginas_pdf > 50:
                        nome_parte2 = "_Unica"
                    else:
                        nome_parte2 = "_IndComdoers"
                    #print('parte 2', nome_parte2)
                    nome_parte3 = ""
                    #print('parte 3',nome_parte3)
                    nome_parte4 = str(data).replace('-', '')
                    #print('parte 4',nome_parte4)
                    abrindo_pdf.close()
                    renomear_arquivo(nome_parte0, nome_parte1, nome_parte2, nome_parte3, nome_parte4, iten)
                    break
                    #break
#F:\Work\Diarios\BA\Diário do Tribunal de Contas da Bahia\Unica\2022\dezembro\unica\20221229\ArqsFull
#F:\Work\Diarios\BA\Diário do Tribunal de Contas da Bahia\Unica\2022\dezembro\extra\20221228\ArqsFull
#TCEBA unica 20221229
#TCEBA extra 20221228
                elif (tribunal == lista_tribunais[11]):
                    #if (re.search('Tribunal de Contas do Estado da Bahia', texto_pdf)) != None:
                    print("ok")
                    data_texto = re.split(r" Bahia|Ano ", texto_pdf)  # separa a informação entre as palavras
                    data_texto = str(data_texto[1])  # texto depois da disponibilização
                    print("data do texto", data_texto)
                    data = extrair_data(data_texto)
                    print("ok")
                    #data = data - datetime.timedelta(1)  # data dia anterior
                    #print(data)
                    nome_parte0 = ""
                    #print('parte 0', nome_parte0)
                    nome_parte1 = dicionaria_tibunais_siglas.get(tribunal)
                    #print('parte 1', nome_parte1)
                    if (re.search('Extra', texto_pdf)) != None:
                        nome_parte2 = " extra "
                    else:
                        nome_parte2 = " unica "
                    #print('parte 2', nome_parte2)
                    nome_parte3 = ""
                    #print('parte 3',nome_parte3)
                    nome_parte4 = str(data).replace('-', '')
                    #print('parte 4',nome_parte4)
                    abrindo_pdf.close()
                    renomear_arquivo(nome_parte0, nome_parte1, nome_parte2, nome_parte3, nome_parte4, iten)
                    break
                    #break
# F:\Work\Diarios\GO\Diário Oficial de Goiás\Unica\2023\Março\doegosup\20230308\ArqsFull
# doego_doegosup-20230308
# F:\Work\Diarios\GO\Diário Oficial de Goiás\Unica\2023\Março\unica\20230308
# doego_unica 20230308
                elif (tribunal == lista_tribunais[12]):
                    print("\nCaderno 12\n")
                    #if (re.search('Diário OficialEstado de Goiás', texto_pdf)) != None:
                    print("ok")
                    data_texto = re.split(r"GOIÂNIA, | Ano ", texto_pdf)  # separa a informação entre as palavras
                    data_texto = str(data_texto[1])  # texto depois da disponibilização
                    print("data do texto", data_texto)
                    data = extrair_data(data_texto)
                    print("ok")
                    #data = data - datetime.timedelta(1)  # data dia anterior
                    #print(data)
                    nome_parte0 = ""
                    #print('parte 0', nome_parte0)
                    nome_parte1 = dicionaria_tibunais_siglas.get(tribunal)
                    #print('parte 1', nome_parte1)
                    if (re.search('SUPLEMENTOATOS', texto_pdf)) != None:
                        nome_parte2 = "_doegosup-"
                    else:
                        nome_parte2 = "_unica "
                    #print('parte 2', nome_parte2)
                    nome_parte3 = ""
                    #print('parte 3',nome_parte3)
                    nome_parte4 = str(data).replace('-', '')
                    #print('parte 4',nome_parte4)
                    abrindo_pdf.close()
                    renomear_arquivo(nome_parte0, nome_parte1, nome_parte2, nome_parte3, nome_parte4, iten)
                    break
                    #break
#tceal
#F:\Work\Diarios\AL\Diário do Tribunal de Contas de Alagoas\Unica\2023\março\unica\20230312\ArqsFull
#TCEAL unica 20230312
                elif (tribunal == lista_tribunais[13]):
                    print("\nCaderno 13\n")
                    #if (re.search('Diário Oficial Eletrônico Instituido', texto_pdf)) != None:
                    print("ok")
                    data_texto = re.split(r"Ano |TRIBUNAL ", texto_pdf)  # separa a informação entre as palavras
                    data_texto = str(data_texto[1])  # texto depois da disponibilização
                    print("data do texto", data_texto)
                    data = extrair_data(data_texto)
                    print("ok")
                    data = data - datetime.timedelta(1)  # data dia anterior
                    #print(data)
                    nome_parte0 = ""
                    #print('parte 0', nome_parte0)
                    nome_parte1 = dicionaria_tibunais_siglas.get(tribunal)
                    #print('parte 1', nome_parte1)
                    nome_parte2 = " unica "
                    #print('parte 2', nome_parte2)
                    nome_parte3 = ""
                    #print('parte 3',nome_parte3)
                    nome_parte4 = str(data).replace('-', '')
                    #print('parte 4',nome_parte4)
                    abrindo_pdf.close()
                    renomear_arquivo(nome_parte0, nome_parte1, nome_parte2, nome_parte3, nome_parte4, iten)
                    break
                    #break
#tcema
#F:\Work\Diarios\MA\Diário do Tribunal de Contas do Maranhão\Unica\2023\Março\unica\20230313\ArqsFull
#TCEMA Unica 20230313
                elif (tribunal == lista_tribunais[14]):
                    print("\nCaderno 14\n")
                    #if (re.search('MARANHÃOTRIBUNAL DE CONTAS DO ESTADODIÁRIO OFICIAL ELETRÔNICO', texto_pdf)) != None:
                    print("ok")
                    data_texto = re.split(r"São Luís, |COMPOSIÇÃO", texto_pdf)  # separa a informação entre as palavras
                    data_texto = str(data_texto[1])  # texto depois da disponibilização
                    print("data do texto", data_texto)
                    data = extrair_data(data_texto)
                    print("ok")
                    #data = data - datetime.timedelta(1)  # data dia anterior
                    #print(data)
                    nome_parte0 = ""
                    #print('parte 0', nome_parte0)
                    nome_parte1 = dicionaria_tibunais_siglas.get(tribunal)
                    #print('parte 1', nome_parte1)
                    nome_parte2 = " Unica "
                    #print('parte 2', nome_parte2)
                    nome_parte3 = ""
                    #print('parte 3',nome_parte3)
                    nome_parte4 = str(data).replace('-', '')
                    #print('parte 4',nome_parte4)
                    abrindo_pdf.close()
                    renomear_arquivo(nome_parte0, nome_parte1, nome_parte2, nome_parte3, nome_parte4, iten)
                    break
                    #break
#tcemt
# F:\Work\Diarios\MT\Diário do Tribunal de Contas do Mato Grosso\Unica\2023\Março\tcemtsup\20230313\ArqsFull
# TCEMT tcemtsup 20230313
# F:\Work\Diarios\MT\Diário do Tribunal de Contas do Mato Grosso\Unica\2023\Março\unica\20230313\ArqsFull
# TCEMT Unica 20230313
                elif (tribunal == lista_tribunais[15]):
                    print("\nCaderno 14\n")
                    #if (re.search('doc_tce@tce.mt.gov.br', texto_pdf)) != None:
                    print("ok")
                    data_texto = re.split(r"Divulgação |Publicação", texto_pdf)  # separa a informação entre as palavras
                    data_texto = str(data_texto[1])  # texto depois da disponibilização
                    print("data do texto", data_texto)
                    data = extrair_data(data_texto)
                    print("ok")
                    #data = data - datetime.timedelta(1)  # data dia anterior
                    #print(data)
                    nome_parte0 = ""
                    #print('parte 0', nome_parte0)
                    nome_parte1 = dicionaria_tibunais_siglas.get(tribunal)
                    #print('parte 1', nome_parte1)
                    if (re.search('Diário Oficial de ContasTribunal de Contas de Mato Grosso', texto_pdf)) != None:
                        nome_parte2 = " tcemtsup "
                    else:
                        nome_parte2 = " Unica "
                    #print('parte 2', nome_parte2)
                    nome_parte3 = ""
                    #print('parte 3',nome_parte3)
                    nome_parte4 = str(data).replace('-', '')
                    #print('parte 4',nome_parte4)
                    abrindo_pdf.close()
                    renomear_arquivo(nome_parte0, nome_parte1, nome_parte2, nome_parte3, nome_parte4, iten)
                    break
                    #break
# tcepe
# F:\Work\Diarios\PE\Diário do Tribunal de Contas de Pernambuco\Unica\2023\Março\unica\20230313\ArqsFull
# TCEPEunica 20230313
                elif (tribunal == lista_tribunais[16]):
                    print("\nCaderno 16\n")
                    #if (re.search('Tribunal de Contas do EstadoPernambucoDiário Eletrônico', texto_pdf)) != None:
                    print("ok")
                    data_texto = re.split(r"autorizo. Recife, |.NOTIFICAÇÃO", texto_pdf)  # separa a informação entre as palavras
                    data_texto = str(data_texto[1])  # texto depois da disponibilização
                    print("data do texto", data_texto)
                    data = extrair_data(data_texto)
                    print("ok")
                    # data = data - datetime.timedelta(1)  # data dia anterior
                    # print(data)
                    nome_parte0 = ""
                    # print('parte 0', nome_parte0)
                    nome_parte1 = dicionaria_tibunais_siglas.get(tribunal)
                    # print('parte 1', nome_parte1)
                    nome_parte2 = "unica "
                    # print('parte 2', nome_parte2)
                    nome_parte3 = ""
                    # print('parte 3',nome_parte3)
                    nome_parte4 = str(data).replace('-', '')
                    # print('parte 4',nome_parte4)
                    abrindo_pdf.close()
                    renomear_arquivo(nome_parte0, nome_parte1, nome_parte2, nome_parte3, nome_parte4, iten)
                    break
                    #break
# tcepr
# F:\Work\Diarios\PR\Diário do Tribunal de Contas do Paraná\Unica\2023\Março\unica\20230314\ArqsFull
# TCEPR Unica 20230314
                elif (tribunal == lista_tribunais[17]):
                    print("\nCaderno 17\n")
                    #if (re.search('DIÁRIO ELETRÔNICO DO TRIBUNAL DE CONTAS DO ESTADO DO PARANÁ', texto_pdf)) != None:
                    print("ok")
                    data_texto = re.split(r" ANO |PÁGINA 1 DE",texto_pdf)  # separa a informação entre as palavras
                    data_texto = str(data_texto[1])  # texto depois da disponibilização
                    print("data do texto", data_texto)
                    data = extrair_data(data_texto)
                    print("ok")
                    # data = data - datetime.timedelta(1)  # data dia anterior
                    # print(data)
                    nome_parte0 = ""
                    # print('parte 0', nome_parte0)
                    nome_parte1 = dicionaria_tibunais_siglas.get(tribunal)
                    # print('parte 1', nome_parte1)
                    nome_parte2 = " Unica "
                    # print('parte 2', nome_parte2)
                    nome_parte3 = ""
                    # print('parte 3',nome_parte3)
                    nome_parte4 = str(data).replace('-', '')
                    # print('parte 4',nome_parte4)
                    abrindo_pdf.close()
                    renomear_arquivo(nome_parte0, nome_parte1, nome_parte2, nome_parte3, nome_parte4, iten)
                    break
                    #break
#tcero
#F:\Work\Diarios\RO\Diário do Tribunal de Contas de Rondônia\Unica\2023\março\Unica\20230313\ArqsFull
#TCERO Unica 20230313
                elif (tribunal == lista_tribunais[18]):
                    print("\nCaderno 18\n")
                    # if (re.search('DIÁRIO ELETRÔNICO DO TRIBUNAL DE CONTAS DO ESTADO DO PARANÁ', texto_pdf)) != None:
                    print("ok")
                    data_texto = re.split(r" - RO | nº ", texto_pdf)  # separa a informação entre as palavras
                    data_texto = str(data_texto[1])  # texto depois da disponibilização
                    print("data do texto", data_texto)
                    data = extrair_data(data_texto)
                    print("ok")
                    # data = data - datetime.timedelta(1)  # data dia anterior
                    # print(data)
                    nome_parte0 = ""
                    # print('parte 0', nome_parte0)
                    nome_parte1 = dicionaria_tibunais_siglas.get(tribunal)
                    # print('parte 1', nome_parte1)
                    nome_parte2 = " Unica "
                    # print('parte 2', nome_parte2)
                    nome_parte3 = ""
                    # print('parte 3',nome_parte3)
                    nome_parte4 = str(data).replace('-', '')
                    # print('parte 4',nome_parte4)
                    abrindo_pdf.close()
                    renomear_arquivo(nome_parte0, nome_parte1, nome_parte2, nome_parte3, nome_parte4, iten)
                    break
                    # break
# tceto
# F:\Work\Diarios\TO\Diário do Tribunal de Contas do Tocantins\Unica\2023\Março\unica\20230313\ArqsFull
# TCETO Unica 20230313
                elif (tribunal == lista_tribunais[19]):
                    print("\nCaderno 19\n")
                    # if (re.search('DIÁRIO ELETRÔNICO DO TRIBUNAL DE CONTAS DO ESTADO DO PARANÁ', texto_pdf)) != None:
                    print("ok")
                    data_texto = re.split(r"Disponibilizado em |POR TARIASPORTARIA", texto_pdf)  # separa a informação entre as palavras
                    data_texto = str(data_texto[1])  # texto depois da disponibilização
                    print("data do texto", data_texto)
                    data = extrair_data(data_texto)
                    print("ok")
                    # data = data - datetime.timedelta(1)  # data dia anterior
                    # print(data)
                    nome_parte0 = ""
                    # print('parte 0', nome_parte0)
                    nome_parte1 = dicionaria_tibunais_siglas.get(tribunal)
                    # print('parte 1', nome_parte1)
                    nome_parte2 = " Unica "
                    # print('parte 2', nome_parte2)
                    nome_parte3 = ""
                    # print('parte 3',nome_parte3)
                    nome_parte4 = str(data).replace('-', '')
                    # print('parte 4',nome_parte4)
                    abrindo_pdf.close()
                    renomear_arquivo(nome_parte0, nome_parte1, nome_parte2, nome_parte3, nome_parte4, iten)
                    break
                    # break

        abrindo_pdf.close()

# def renomear_arquivo(nome_parte0, nome_parte1, nome_parte2, nome_parte3, nome_parte4, iten):
#
#     nome = (nome_parte0 + nome_parte1 + nome_parte2 + nome_parte3 + nome_parte4 + '.pdf')
#     print("nome:", nome)
#     lugar = iten
#     inicio = os.path.split(lugar)
#     #print(inicio[0])
#     #print(lugar)
#     print(inicio[0] + "\\" + nome)
#     try:
#         os.rename(lugar, inicio[0] + "\\" + nome)
#         print("Arquivo renomeado.")
#     except OSError as error:
#         print(error)
#ainda nao foi testado
def renomear_arquivo(nome_parte0, nome_parte1, nome_parte2, nome_parte3, nome_parte4, iten):

    nome = (nome_parte0 + nome_parte1 + nome_parte2 + nome_parte3 + nome_parte4 + '.pdf')
    print("nome:", nome)
    lugar = iten
    inicio = os.path.split(lugar)
    # print(inicio[0])
    # print(lugar)
    while os.path.exists(inicio[0] + "\\" + nome):
        nome = nome.split(".pdf")[0] + "_" + ".pdf"
    print(inicio[0] + "\\" + nome)
    try:
        os.rename(lugar, inicio[0] + "\\" + nome)
        print("Arquivo renomeado.")
    except OSError as error:
        print(error)
