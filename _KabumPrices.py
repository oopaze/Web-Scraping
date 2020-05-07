from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup as bs
from time import sleep
try:
    from Crawlers.MainCrawler import MainCrawler
except ModuleNotFoundError:
    from MainCrawler import MainCrawler

class KBPrices(MainCrawler):
    """
    Get some prices of a Kabum product by a keyword 
    """
    def __init__(self, file: str, driver: object):
        super().__init__(driver)

        self.link = "https://www.kabum.com.br" #starter link
        self.file = file #file that receives all product found
        self.page_html = None #Html for the page that we're scraping
        self.wait = WebDriverWait(self.driver, 10)
  
    def _start(self, keys, pages = 1):
        """
        Entrando na Kabum e pegandos preços a partir de uma chave passada
        """
        self.driver.get(self.link) #Abrindo driver no link passado
        self.test_file(self.file) #Vendo se o arquivo para persistencia existe
        
        sleep(self.transition_page) 

        for key in keys.split(','): #Percorrendo apartir de cada key passada
            
            self.products = {} #Reinicializando o dicionario products
            
            self.search_prod(key) #Escrevendo na barra de pesquisa a key
            sleep(self.transition_page) #Tempo de Transição entre páginas
            
            for page in range(pages): #percorrendo a partir da quantidade de paginas desejadas

                self.take_prices() #Extraindo as informações

                self.driver.find_element_by_css_selector('#bt-busca').click() #Passando a pagina

            self.saving_prices(key) #Salvando os preços achados
        
    def search_prod(self, key):
        """
        Função responsavel por localizar a barra de pesquisa e fazer a busca
        """
        search_bar = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.sprocura'))) #Localizando barra
        
        search_bar.clear() #Limpando barra de pesquisa
        search_bar.send_keys(key) #Inserindo a key na barra
        search_bar.send_keys(Keys.ENTER) #Pressionando enter

    def take_prices(self):
        """
        Função responsavel por percorrer o HTML e extrair as informações
        """
        self.page_html = bs(self.driver.page_source, 'html.parser') #Extraindo HTML da pagina
        products = self.page_html.find_all('div', {'class':'sc-fzqARJ eITELq'}) #Localizando cada conteiner com produtos

        for prod in products: #Percorrendo cada conteiner
            marca = prod.find('div', {'class':'sc-fzplWN fOLGVq'}) #Extraindo marca
            marca = marca.find('img', {'class':'sc-fznyAO brXUpP'})['alt'] #Extraindo o tex
            name = prod.find('a', {'class':'sc-fzoLsD gnrNhT item-nome'}).text #Extraindo a descrição
            price = prod.find('div', {'class':'sc-fznWqX qatGF'}).text #Extraindo
            image = prod.find('img')['src'] #Extraindo o link da Imagem
            link = prod.find('a')['href']
            link = f'{self.link}{link} '

            

            track = 'Contatar o Vendedor'
            
            name = name.replace(',', '-')
            self.products[name] = [price, track, link, image, marca] #Salvando dados encontrados em um dicionario 

            

if __name__ == '__main__':
    file = 'KBdata.csv'
    key = input('Product: ')
    
    driver = webdriver.Firefox()
    
    KBBot = KBPrices(file, driver)
    KBBot._start(key)
