from selenium import webdriver
from bs4 import BeautifulSoup as bs
import requests as r
from time import sleep
try:
    from Crawlers.MainCrawler import MainCrawler
except ModuleNotFoundError:
    from MainCrawler import MainCrawler

    
class AmazonPrices(MainCrawler):
    """
    Get some prices of a Amazon product by a keyword 
    """
    def __init__(self, file: str, driver: object):
        super().__init__(driver)
        self.link = "https://www.amazon.com.br" #starter link
        self.file = file #file that receives all product found
        self.page_html = None #Html for the page that we're scraping
    
    def _start(self, key, pages = 1):
        """
        Entrando na Amazon e pegandos preços a partir de uma chave passada
        """
        self.driver.get(self.link) #Entrando no website 
        self.test_file(self.file) #Criando arquivo para persistencia dos dados

        sleep(self.transition_page) #Tempo para atualização da pagina

        for k in key.split(','): #Procurando produtos por cada key passada

            self.products = {} #Reinicializando os produtos para nova busca

            self.search_prod(k) #Buscando produtos no site
            sleep(self.transition_page) #Tempo para atualização da pagina

            for e in range(pages): #Procurando na quantidade de paginas passadas
                
                self.take_prices() #Pegando os preços dos produtos na pagina 
                if pages > 1:
                    self.driver.find_element_by_css_selector('.a-last > a:nth-child(1)').click() #Indo para a proxima pagina
                    sleep(self.transition_page) #Tempo para atualização da página

            self.saving_prices(k) #Salvando todos os produtos em um arquivo.csv

    def search_prod(self, key):
        """
        Fazendo a pesquisa na Amazon a partir da chave passada
        """
        search_bar = self.driver.find_element_by_css_selector('#twotabsearchtextbox') #Localizando a barra de pesquisa
        search_bar.clear() #Limpando caixa de text
        search_bar.send_keys(key) #Enviando chave

        self.driver.find_element_by_css_selector('.nav-search-submit > input:nth-child(2)').click() #Clickando em pesquisar

    def take_prices(self): 
        """
        Percorrendo o HTML da pagina e extraindo informaçõe de preco, descrição e entrega_
        """
        self.page_html = bs(self.driver.page_source, 'html.parser') #Extraindo o html da page com o Beautiful Soup

        products = self.page_html.find_all('div', {'class':'s-include-content-margin s-border-bottom s-latency-cf-section'}) #Achando todos os conteiners com produtos

        for e in products: #Percorrendo conteiners
            price = e.find('span', {'class':'a-offscreen'}) #Procurando preço
            if price: #Vendo se existe o produto em estoque
                name = e.find('span', {'class':'a-size-medium a-color-base a-text-normal'}).text #Extraindo text
                price = price.text #Extraindo preco
                track = e.find('div', {'class':'a-row a-size-base a-color-secondary s-align-children-center'}) #Procurando opções de entrega 
                image = e.find('img', {'class':'s-image'})['src'] #Procurando as imagens dos produtos
                link = e.find('a', {'class':'a-link-normal a-text-normal'})['href']
                link = f'{self.link}{link} '
                
                
                    
                if track: #Formatando Opções de entrega, para o preço ou 'Contatar Vendedor'
                    track = track.find_all('span')[1].text                 
                    for e in range(len(track)):
                        if track[e] == ',':
                            track = track[2:e].replace(',', '.')
                            break
                    
                        elif track == '\n\n':
                            track = 'Contatar o Vendendor'

                name = name.replace(',', '-')
                self.products[name] = [price, track, link,image] #Colocando todos os produtos achados no dicionario products
      



if __name__ == '__main__':
    
    file = 'AmazonData.csv'
    key =  input('Product: ')

    driver = webdriver.Firefox()
    
    AmazonBot = AmazonPrices(file, driver)
    AmazonBot._start('ssd', 1)
