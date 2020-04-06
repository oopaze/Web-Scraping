from requests import get
from bs4 import BeautifulSoup as bs

URL = 'https://pt.wikipedia.org/wiki/Lista_de_epis%C3%B3dios_de_Os_Simpsons'

request = get(URL)

page = bs(request.content, 'lxml')

tables = page.find_all('table', {'class': 'wikitable plainrowheaders wikiepisodetable'})

info = []
season_control = 1
for  table in tables:
    
    linha = table.find_all('tr', {'class':'vevent'})
    controller = 1
    for elem in linha:
        if elem.find('th'):
            num_ep = elem.find('th').text
            dados = elem.find_all('td')
            
            ep_season, name_ep, director, writer, data, cod, espec = dados
            

            info.append((season_control, num_ep, ep_season.text, name_ep.text, data.text))

        controller += 1
    season_control += 1

with open('episodios_simpsons.csv', 'w') as arquivo:
    arquivo.write('')
    arquivo.close()


with open('episodios_simpsons.csv', 'a') as arquivo:
    arquivo.write('Temporada; Num. Episodio; Num.Episodio na Temp.; Titulo; Data;\n')
    for linha in info:
        controller = 1
        for elem in linha:
            if controller%4 == 0:    
                elem = elem.replace('" "','|')
                elem = elem.replace('"  "','|')
                elem = elem.split('|')[1]
                elem = elem.replace('"', '')
            controller += 1
            arquivo.write(f'{elem};')
        arquivo.write('\n')

    arquivo.close()


