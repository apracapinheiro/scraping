import time

import bs4
import requests
import openpyxl
from openpyxl.styles import Font, NamedStyle


def request_site(url, headers, num_pagina):
    """
    Realiza a requisicao da pagina
    :param url: url da página que será realizado o scraping
    :param headers: cabeçalhos contendo informacoes sobre o browser. Necessario para passar pela validacao no servidor
    alvo
    :param num_pagina:
    :return:
    """
    if not num_pagina:
        num_pagina = 1
    time.sleep(3)
    res = requests.get(url, headers=headers)
    status_request = res.raise_for_status()
    return res, status_request


def scraping_insumos(requisicao, status, num_pagina, lista_insumos, headers, site):
    """
    Funcao que realiza o scraping dos insumos.
    :param requisicao: objeto requisicao da pagina
    :param status: status da requisicao, só continua se o valor for None. Valores diferentes de None indicam o erro
    que o servidor enviou
    :param num_pagina: numero da pagina que sera realizado o scraping
    :param lista_insumos: lista que contem os insumos das outras paginas que ja passaram por scraping
    :param cabecalho enviado para o servidor alvo
    :param url do site que será realizado scraping
    :return: lista de insumos com todas as paginas.
    """
    qtde_precos = 0  # guarda a quantidade de precos na primeira pagina

    while status == None:
        if site == 'BREWHEAD':
            pagina = bs4.BeautifulSoup(requisicao.text)
            insumo = pagina.select('div h4')
            precos = pagina.select('p[class="price"]')
            proximo = pagina.select('ul[class="pagination"]')
            url_inicial = 'https://brewheadshop.com.br/insumos/maltes?' + 'page='  # BREWHEAD
        elif site == 'LAMAS':
            pagina = bs4.BeautifulSoup(requisicao.text)
            insumo = pagina.select('div[class="list-conteiner-name"]')
            precos = pagina.select('span[class="regular-price"]')
            proximo = pagina.select('a[class="next i-next"]')
            url_inicial = 'http://loja.lamasbrewshop.com.br/insumos/malte-cereais.html?' + 'p='  # LAMAS
        elif site == 'WE':
            pagina = bs4.BeautifulSoup(requisicao.text)
            insumo = pagina.select('div[class="product-name"]')
            precos = pagina.select('b[class="sale"]')
            proximo = pagina.select('span[class="page-next"]')
            url_inicial = 'http://loja.weconsultoria.com.br/maltes-s10038/?' + 'pagina='  # WE
        elif site == 'CERVEJADACASA':
            pagina = bs4.BeautifulSoup(requisicao.text)
            insumo = pagina.select('div[itemprop="name"]')
            precos = pagina.select('meta[itemprop="price"]')
            proximo = pagina.select('a[rel="next"]')
            url_inicial = 'http://www.cervejadacasa.com/loja/catalogo.php?loja=420472&categoria=53&pg='  # CERVEJA DA CASA
        elif site == 'ARTEBREW':
            pagina = bs4.BeautifulSoup(requisicao.text)
            insumo = pagina.select('h5 a')
            precos = pagina.select('span[class="regular-price"]')
            # proximo = pagina.select('a[class="next i-next"]')
            proximo = pagina.find('a', {'class': 'next i-next'})
            url_inicial = 'http://cervejacaseira.com.br/materias-primas.html?cat=23&p='  # ARTBREW

        if qtde_precos == 0:
            qtde_precos = len(precos)  # atualiza a quantidade de precos uma vez, quando captura a primeira pagina

        if len(precos) > 0:
            for i in range(len(precos)):
                if site == 'CERVEJADACASA':
                    nome_insumo = insumo[i].get_text()
                    preco_insumo = str(precos[i].attrs['content'])
                    insumos_preco = {nome_insumo: preco_insumo}
                    lista_insumos.append(insumos_preco)
                else:  # BREWHEAD, LAMAS, WE
                    nome_insumo = insumo[i].get_text().strip()
                    preco_insumo = precos[i].get_text().strip()
                    # if not esgotado[i].get_text() == 'Esgotado':
                    insumos_preco = {nome_insumo: preco_insumo}
                    lista_insumos.append(insumos_preco)

            if len(proximo) > 0:
                if qtde_precos == len(precos):
                    num_pagina += 1
                    url = url_inicial + str(num_pagina)
                    requisicao, status = request_site(url, headers, num_pagina)
                    # res = requests.get(url, headers=headers)
                    # status_request = res.raise_for_status()
                else:
                    break
            else:
                break
        else:
            break

    return lista_insumos


def gera_planilha(lista_insumos, wb, planilha, site):
    """
    Funcao que exporta a lista de insumos para uma planilha no formato xlsx
    :param lista_insumos: a lista com os insumos depois do scraping
    :param wb: WORKBOOK, arquivo principal da planilha
    :param planilha: sheet (planilha) dentro do WORKBOOK
    :param site: nome do site que está sendo realizado o scraping
    :return: sem retorno. Grava a planilha.
    """
    fonte = Font(bold=True, size=14)
    planilha['A1'].font = fonte
    planilha['A1'] = 'Insumo'
    planilha['B1'].font = fonte
    planilha['B1'] = 'Preço'

    for numeroLinha in range(len(lista_insumos)):
        insumo_preco = str(lista_insumos[numeroLinha]).split(":")
        # insere na primeira coluna o nome dos insumos
        planilha.cell(row=numeroLinha+2, column=1).value = insumo_preco[0].replace('{', '').replace('\'', '').replace('\\n', '')
        # insere na segunda coluna o preco dos insumos
        planilha.cell(row=numeroLinha+2, column=2).value = insumo_preco[1].replace('\'', '').replace('\' ', '').replace('}', '')

    wb.save(site + '.xlsx')