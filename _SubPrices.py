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

class SubPrices(MainCrawler):
    """
    Get some prices of a Submarino product by a keyword 
    """
    def __init__(self, file: str, driver: object):
        super().__init__(driver)

        self.link = "https://www.submarino.com.br/" #starter link 
        self.file = file #file that receives all product found 
        self.page_html = None #Html for the page that we're scraping

    def _start(self, keys, pages=1):
        """
        Entrando na Submarino e pegandos preços a partir de uma chave passada
        """
        self.driver.get(self.link) #Abrindo browser no link passado
        self.test_file(self.file) #Testando se arquivo para persistencia já existe
        self.wait = WebDriverWait(self.driver, 10)
        
        for key in keys.split(','): #Percorrendo a partir de cada keyword
            sleep(self.transition_page+3) #Tempo para transição de página
            self.products = {} #Reinicializando Products
            self.search_prod(key) #Fazendo busca

            
            sleep(self.transition_page+3) #Tempo para transição da página

            for page in range(pages): #Percorrendo cada página
                self.take_prices() #Extraindo dados
                
                if pages > 1:
                    self.driver.find_element_by_css_selector('.pagination-product-grid > li:nth-child(10) > a:nth-child(1)').click() #Passando a página

            self.saving_prices(key) #Salvando dados
            sleep(self.transition_page+3)
        
    def search_prod(self, key):
        """
        Função responsavel por localizar a barra de pesquisa e fazer a busca
        """
        search_bar = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#h_search-input'))) #Achando a barra de busca
        
        search_bar.clear() #Limpando a barra de busca
        search_bar.send_keys(key) #Escrevendo a key na barra de busca

        search_bar.send_keys(Keys.ENTER) #Pressionando enter

    def take_prices(self):
        """
        Função responsavel por percorrer o HTML e extrair as informações
        """
        self.page_html = bs(self.driver.page_source, 'html.parser') #Extraindo HTML da página
        products = self.page_html.find_all('div', {'class':'product-grid-item ColUI-gjy0oc-0 ifczFg ViewUI-sc-1ijittn-6 iXIDWU'}) #Extraindo os conteiners com produtos
        url_page = self.driver.current_url #Extraindo url da page pra gerar a url da venda

        for prod in products: #Percorrendo cada produto
            try:
                name = prod.find('h2', {'class':'TitleUI-bwhjk3-15 khKJTM TitleH2-sc-1wh9e1x-1 fINzxm'}).text #Extraindo descrição do produto
                name = name.replace(',', '-')
                
                price = prod.find('span', {'class':'PriceUI-bwhjk3-11 cmTHwB PriceUI-sc-1q8ynzz-0 inNBs TextUI-sc-12tokcy-0 CIZtP'}) #Extraindo elemento contendo os preços do produto
                
                if not price: #Se houver o elemento tiver em estoque
                    price = prod.find('span', {'class':'PriceUI-bwhjk3-11 jtJOff PriceUI-sc-1q8ynzz-0 inNBs TextUI-sc-12tokcy-0 CIZtP'}) #Extraindo elemento contendo os preços do produto

                if price:
                    price = price.text #Extraindo preço 
                    
                    link = prod.find('a', {'class':'Link-bwhjk3-2 iDkmyz TouchableA-p6nnfn-0 joVuoc'})['href'] #Extraindo link da venda
                    link = f'{url_page}/{link}' #Gerando o link

                    image = prod.find('img', {'class':'ImageUI-sc-9rtsvr-0 kJNtKk ImageUI-sc-1je0itq-2 eAYdMC'}) #Em desenvolvimento
                    if image:
                        image = image['src']
                    else:
                        image = 'Not Avaible'

                    track = 'Contatar o Vendedor'
                    self.products[name] = [price, track, link, image] #Armezenando dados em products

            except Exception as e:
                print(e)




if __name__ == '__main__':
    file = 'Subdata.csv'
    driver = webdriver.Firefox()

    SubBot = SubPrices(file, driver)
    SubBot._start('ssd', 3)
