import re
import datetime
import locale
locale.setlocale(locale.LC_TIME, 'portuguese')


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
    # Tenta encontrar uma data no texto com base em cada padrão
    for padrao_data in padroes_data:
        # Procura por uma data no texto com base no padrão atual
        for match in re.finditer(padrao_data, data_texto):
            encontrado_data = match.group()
            grupos = match.groups()
            qtde_grupos = len(grupos)
            # Exibe informações de depuração
            print(grupos)
            print(qtde_grupos)
            #print(len(grupos[0]))
            #print(len(grupos[1]))
            #print(len(grupos[2]))

            print("DATA ENCONTRADA", encontrado_data)
            # Decide qual formato de data usar com base no número de grupos e no comprimento de cada grupo
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

data_texto = " QUARTA-FEIRA, 08 DE MARÇO DE 2023 "
data = extrair_data(data_texto)
print(data)

