import os
#import pathlib
import re
import shutil
from VerificadorNomes import selecao_caminho
import datetime

lista_movidos = []

def mover():
    if (os.path.exists('F:/')) == True:
        inicio_caminho = "F:/Work/Diarios/"
    else:
        inicio_caminho = "C:/Work/Diarios/"

    item_a_mover0 = selecao_caminho() #FUNÇÃO que carrega duas listas com o caminho do arquivo e o arquivo

    print("item a mover",item_a_mover0)

    sigla_tibunais = ['DOTRE', 'djrs', 'TCERN', 'djma', 'djmt', 'dodjpi', 'DOEAP', 'DOEAM', 'DOEPB', 'doers', 'TCEBA',
                      'doego','TCEAL','TCEMA','TCEMT','TCEPE','TCEPR','TCERO','TCETO']

    caminho_tribunais = ['/Diário Oficial do TRE',
                        'RS/Diário da Justiça do Rio Grande do Sul/Unica/',
                        'RN/Diário do Tribunal de Contas do RN/Unica/',
                        'MA/Diário da Justiça do Maranhão/Unica/',
                        'MT/Diário da Justiça de Mato Grosso/Unica/',
                        'PI/Diário da Justiça do Piauí/Unica/',
                        'AP/Diário Oficial do Amapá/Unica/',
                        'AM/Diário Oficial do Amazonas/Unica/',
                        'PB/Diário Oficial da Paraíba/Unica/',
                        'RS/Diário Oficial do Rio Grande do Sul/Cadernos/',
                        'BA/Diário do Tribunal de Contas da Bahia/Unica/',
                        'GO/Diário Oficial de Goiás/Unica/',
                        'AL/Diário do Tribunal de Contas de Alagoas/Unica/',
                        'MA/Diário do Tribunal de Contas do Maranhão/Unica/',
                        'MT/Diário do Tribunal de Contas do Mato Grosso/Unica/',
                        'PE/Diário do Tribunal de Contas de Pernambuco/Unica/',
                        'PR/Diário do Tribunal de Contas do Paraná/Unica/',
                        'RO/Diário do Tribunal de Contas de Rondônia/Unica/',
                        'TO/Diário do Tribunal de Contas do Tocantins/Unica/']


    nomes_pastas = ['unica', 'extra', 'Unica', 'Extra', 'Int1', 'Edit1e2', 'Cap2', 'Cap1', 'AdminJud','doegosup',
                    'IndComdoers','tcemtsup']

    dicionario_siglas_meiocaminho = dict(zip(sigla_tibunais, caminho_tribunais))
    print(dicionario_siglas_meiocaminho)

    dicionario_itens_a_mover = {}

    #manipula asinformaçoes dos nomes e coloca em lista para serem criados dicionarios
    for origem in item_a_mover0:
        nome_do_arquivo = origem.split("\\")[-1] # pega a ultima parte da string que contem o nome do arquivo
        print("nome do arquivo :", nome_do_arquivo)
        print("origem", origem)

        for sigla, caminho in dicionario_siglas_meiocaminho.items():

            if (re.search( sigla, nome_do_arquivo)) != None:
                caminho_origem = origem

                str_data0 = re.search("\d{8}", nome_do_arquivo)
                print(str_data0)
                if str_data0:
                    encontrado_data = str_data0.group()
                    print("encontrado data: ",encontrado_data)

                    data = datetime.datetime.strptime(encontrado_data, '%Y%m%d').date()
                    dia = data.strftime("%d")
                    mes = (data.strftime("%B")).capitalize()
                    #mes_n = data.strftime("%m")
                    ano = data.strftime("%Y")
                    print("sigla do tribunal: ", sigla)
                    print("caminho: ", caminho)
                    print("Nome do arquivo: ", nome_do_arquivo)
                    print("str_data0: ", str_data0)
                    print("data: ", data)
                    print("dia: ", dia)
                    print("mes: ", mes)
                    #print("mes_n: ", mes_n)
                    print("ano: ", ano)
                    print("caminho: ", caminho)

                    if sigla == "DOTRE":
                        str_estado_sigla = str(nome_do_arquivo[5:7])
                        str_estado_sigla_minuscula = str(str_estado_sigla.lower())
                        print("Sigla do estado:", str_estado_sigla_minuscula)

                        if (re.search('(_Sup_)', nome_do_arquivo)) != None: # suplementos
                            if str_estado_sigla == "AL":
                                caminho_destino = str(inicio_caminho + str_estado_sigla + caminho + str_estado_sigla + "/Unica/" + ano + "/" + mes + "/suptrealagoas/" + encontrado_data + "/")
                            elif str_estado_sigla == "AM":
                                caminho_destino = str(inicio_caminho + str_estado_sigla + caminho + str_estado_sigla + "/Unica/" + ano + "/" + mes + "/suptreamazonas/" + encontrado_data + "/")
                            elif str_estado_sigla == "RS":
                                caminho_destino = str(inicio_caminho + str_estado_sigla + caminho + str_estado_sigla + "/Unica/" + ano + "/" + mes + "/suplementotrers/" + encontrado_data + "/")
                            else:
                                caminho_destino = str(inicio_caminho + str_estado_sigla + caminho + str_estado_sigla + "/Unica/" + ano + "/" + mes + "/tre" + str_estado_sigla_minuscula + "sup/" + encontrado_data + "/")
                        else: # unicas
                            caminho_destino = str(inicio_caminho + str_estado_sigla + caminho + str_estado_sigla + "/Unica/" + ano + "/" + mes + "/unica/" + encontrado_data + "/")

                    elif sigla == "djrs":
                        for nome_pasta in nomes_pastas:
                            if (re.search(nome_pasta, nome_do_arquivo)) != None:
                                pasta = nome_pasta.capitalize() #coloca primeira letra em maiuscula
                        print("pasta :", pasta)
                        caminho_destino = str(inicio_caminho + caminho + ano + "/" + mes + "/" + pasta + "/" + encontrado_data + "/")

                    elif sigla == "DOEPB":
                        if (re.search('( sup )', nome_do_arquivo)) != None:  # suplementos
                            pasta = "Suplemento"
                        elif (re.search('( Unica )', nome_do_arquivo)) != None:  # suplementos
                            pasta = "unica"
                        print("pasta :", pasta)
                        caminho_destino = str(inicio_caminho + caminho + ano + "/" + mes + "/" + pasta + "/" + encontrado_data + "/")

                    else:
                        for nome_pasta in nomes_pastas:
                            if (re.search(nome_pasta, nome_do_arquivo)) != None:
                                pasta = nome_pasta.capitalize() #coloca em minuscula
                        print("pasta :", pasta)
                        caminho_destino = str(inicio_caminho + caminho + ano + "/" + mes + "/" + pasta + "/" + encontrado_data + "/")

                    caminho_destino = os.path.join(caminho_destino,nome_do_arquivo)
                    caminho_destino = os.path.normpath(caminho_destino)
                    caminho_origem = os.path.normpath(caminho_origem)
                    print("Destino do arquivo: ",caminho_destino)
                    print("Origem do aquivo: ", caminho_origem)
                    dicionario_itens_a_mover[caminho_destino] = caminho_origem
    print("Dicionario montado: ", dicionario_itens_a_mover)


    def mover_arquivo(origem, destino):
        # Obtém o caminho do diretório do destino
        caminho = os.path.dirname(destino)
        print("##########", caminho)
        # Verifica se o caminho já existe, se não existir, cria o diretório e move o arquivo

        if not os.path.exists(caminho):
            os.makedirs(caminho)
            shutil.move(origem, destino)
            lista_movidos.append(os.path.basename(origem))
            print(f"O arquivo {os.path.basename(origem)} foi movido para {destino}.")
        else:
            print(f"O arquivo {os.path.basename(origem)} já foi movido para {destino}.")


    for destino , origem in dicionario_itens_a_mover.items():
        mover_arquivo(origem, destino)