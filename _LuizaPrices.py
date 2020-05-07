from selenium import webdriver
from bs4 import BeautifulSoup as bs
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

try:
    from Crawlers.MainCrawler import MainCrawler
except ModuleNotFoundError:
    from MainCrawler import MainCrawler

class LuizaPrices(MainCrawler):
    """
    Get some prices of a Magazine Luiza product by a keyword 
    """
    def __init__(self, file: str, driver: object):
        super().__init__(driver)
        
        self.link = "https://www.magazineluiza.com.br/" #starter link
        self.file = file #file that receives all product found
        self.page_html = None #Html for the page that we're scraping
        self.wait = WebDriverWait(self.driver, 10)

    def _start(self, keys, page = 1):
        """
        Entrando na Magazine Luiza e pegando preços a partir de uma chave passada
        """
        
        self.driver.get(self.link) #Abrindo o webdriver no site do magazine luiza
        self.test_file(self.file) #Testando se o arquivo para persistencia já existe

         
        for key in keys.split(','): #Percorrendo por cada chave passada
            self.products = {} #Reinicializando o dic products

            sleep(self.transition_page) #Tempo para transição de página

            self.search_prod(key) #Procurando barra de input e fazendo a pesquisa
            sleep(self.transition_page) #Tempo para transição de página

            for e in range(1, page+1): #Percorrendo as paginas a partir de uma quantidade limite passada
                self.take_prices() #Pegando preços em desenvolvimento

                #self.driver.find_element_by_css_selector('.neemu-pagination-next > a:nth-child(1)').click()ex
            self.saving_prices(key) #Salvando todos os produtos achados

    def search_prod(self, key):
        """
        Acha a barra de navegação do site faz uma busca a partir de uma key passada
        """
        search_bar = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input.field-input-search:nth-child(2)'))) #Procurando barra de pesquisa
        
        sleep(3)
        search_bar.clear() #Limpando barra de pesquisa
        search_bar.send_keys(key) #Inserindo key na barra de pesquisa

        self.driver.find_element_by_css_selector('#btnHeaderSearch').click() #Achando e clickando no botao pesquisar

    def take_prices(self):
        """
        Pega o html da pagina acessada e extrai os dados do produto
        """
        self.page_html = bs(self.driver.page_source,'html.parser')  #Extraindo HTML da página
        products = self.page_html.find_all('li', {'class':'nm-product-item'}) #Extraindo do HTML todos os conteiners com produtos

        for prod in products: #Percorrendo cada produtos
            #Achando e formatando a descrição do produto
            name = prod.find('h2', {'class':'nm-product-name'}).text
            name = name.replace('\n', '')
            name = name.replace('                ', '')
            
            price = prod.find('div', {'class':'nm-price-container'}) #Extraindo preço

            if price: 
                
                #Formatando preço
                price = price.text.replace('.','')
                price = price.replace(',','.')
                price = price.replace('\xa0', '')
                price = price.replace(' à vista', '')
                #Achando informações do produto
                prod_info = prod.find('a', {'class':'productShowCaseContainer nm-product-item-container product-li'})
                if prod_info:
                    link = prod_info['href'] #Extraindo link da venda
                    link = f'https:{link}'

                    marca = prod_info['brand'] #Extraindo a marca do produto

                    image = prod.find('img', {'class':'nm-product-img'})['src'] #Extraindo link da imagem

                    track = 'Contatar Vendedor' #Setando envio como contatar vendedor

                    name = name.replace(',', '-')
                    self.products[name] = [price, track, link, image, marca] #Salvando dados em products


if __name__ == '__main__':
    file = 'Luizadata.csv'
    firefox = webdriver.Firefox()

    LuizaBot = LuizaPrices(file, firefox)
    LuizaBot._start('ssd')

