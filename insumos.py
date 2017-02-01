from scrapingtools import *


# NOME_SITE = 'LAMAS'
NOME_SITE = 'BREWHEAD'
# NOME_SITE = 'WE'
# NOME_SITE = 'CERVEJADACASA'
# NOME_SITE = 'ARTEBREW'

# headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}  # MAC
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'} # CHROME
# headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}  # FIREFOX

wb = openpyxl.Workbook()
sheet = wb.get_active_sheet()
sheet.title = 'Precos maltes ' + NOME_SITE


num_pagina = 1
# url = 'http://loja.lamasbrewshop.com.br/insumos/malte-cereais.html?' + 'p=%d' % num_pagina  # LAMAS
url = 'https://brewheadshop.com.br/insumos/maltes?' + 'page=%d' % num_pagina  # BREWHEAD
# url = 'http://loja.weconsultoria.com.br/maltes-s10038/?' + 'pagina=%d' % num_pagina  # WE
# url = 'http://www.cervejadacasa.com/loja/catalogo.php?loja=420472&categoria=53&pg=%d' % num_pagina # CERVEJA DA CASA
# url = 'http://cervejacaseira.com.br/materias-primas.html?cat=23&p=%d' %num_pagina  # ARTEBREW
lista_insumos = []

requisicao, status = request_site(url, headers, num_pagina)
lista_precos_insumos = scraping_insumos(requisicao, status, num_pagina, lista_insumos, headers, NOME_SITE)
gera_planilha(lista_insumos, wb, sheet, NOME_SITE)