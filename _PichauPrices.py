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


class PIPrices(MainCrawler):
    """
    Get some prices of a Pichau product by a keyword 
    """
    def __init__(self, file: str, driver: object):
        super().__init__(driver)

        self.link = "https://www.pichau.com.br/" #starter link 
        self.file = file #file that receives all product found 
        self.page_html = None #Html for the page that we're scraping
        self.wait = WebDriverWait(self.driver, 10)

    def _start(self, keys, pages=1):
        """
        Entrando na Pichau e pegandos preços a partir de uma chave passada
        """
        self.driver.get(self.link) #Abrindo o browser no link passado
        self.test_file(self.file) #Testando se o arquivo para persistencia existe
        
        sleep(self.transition_page) #Tempo para transição de pagina

        for key in keys.split(','): #Percorrendo as keywords
            
            self.products = {} #Reinicializando o dicionario produtos
            
            self.search_prod(key) #Fazendo pesquisa
            sleep(self.transition_page) #Tempo para transição de tel
            try:
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.toolbar:nth-child(1) > div:nth-child(4) > div:nth-child(1) > select:nth-child(1) > option:nth-child(3)'))).click() #Setando 46 produtos por page
            except Exception as e:
                print(e)
                
            sleep(self.transition_page)
            for page in range(pages): #Percorrendo paginas
                self.take_prices() #Salvando as informações dos produtos
                    
                if pages > 1:
                    self.driver.find_element_by_css_selector('div.toolbar:nth-child(3) > div:nth-child(2) > ul:nth-child(1) > li:nth-child(5) > a:nth-child(1)').click() #Passando pagina

            self.saving_prices(key) #Salvando precos 
            
                
    def search_prod(self, key):
        """
        Função responsavel por localizar a barra de pesquisa e fazer a busca
        """
        search_bar = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#search')))

        search_bar.clear() #Limpando barra de pesquisa
        search_bar.send_keys(key) #Enviando chave
        search_bar.send_keys(Keys.ENTER) #Pressionando Enter
       
    def take_prices(self):
        """
        Função responsavel por percorrer o HTML e extrair as informações
        """
        self.page_html = bs(self.driver.page_source, 'html.parser') #Extraindo o HTML da page
        products = self.page_html.find_all('li', {'class':'item product product-item'}) #Pega cada conteiner achado no html da page

        for prod in products: #Percorrendo produtos

            name = prod.find('a', {'class':'product-item-link'}).text.replace('\n', '') #Extraindo name
            name = name.replace(',', '-')
            
            price = prod.find('span', {'price-boleto'}) #Extraindo preco
            if price: 
            
                price = price.text #Formatando preco

                link = prod.find('a', {'class':'product photo product-item-photo'})['href'] #Extraindo link

                image = prod.find('img', {'class':'product-image-photo'})['src'] #Extraindo link da imagem

                track = 'Contatar Vendedor' #Setando envio para contatar vendedor

                self.products[name] = [price, track, link, image] #Salvando em products




if __name__ == '__main__':
    file = 'Pichaudata.csv'
    driver = webdriver.Firefox()

    PichauBot = PIPrices(file, driver)
    PichauBot._start('ssd')
