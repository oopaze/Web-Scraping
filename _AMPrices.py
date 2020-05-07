from selenium import webdriver
from bs4 import BeautifulSoup as bs
from time import sleep
try:
    from Crawlers.MainCrawler import MainCrawler
except ModuleNotFoundError:
    from MainCrawler import MainCrawler

class AMPrices(MainCrawler):
    """
    Get some prices of a Americanas product by a keyword 
    """
    def __init__(self, file: str, driver: object):
        super().__init__(driver)
        self.link = "https://www.americanas.com.br" #starter link
        self.file = file #file that receives all product found
        self.page_html = None #Html for the page that we're scraping
    
    def _start(self, keys, pages = 1):
        """
        Entrando na Americanas e pegandos preços a partir de uma chave passada
        """
        self.driver.get(self.link) #Abrindo o link do site no Browser
        self.test_file(self.file) #Testando se o arquivo para persistencia foi criado
        
        sleep(self.transition_page) #Tempo para transição de páginas no navegador
        
        for key in keys.split(','): #Procurando cada key passada no Navegador
            
            self.products = {} #Reinicializando o dicionario produtos
            try:
                self.search_prod(key) #Inserindo a key na barra de pesquisa do site
            except Exception:
                sleep(self.transition_page)
                self.search_prod(key)
                
            sleep(self.transition_page) #Tempo para transição das telas
        
            for page in range(pages): #Percorrendo os dados em uma quantidade de paginas passadas
                self.take_prices() #Extraindo dados
                sleep(self.transition_page)
                if pages > 1:
                    self.driver.find_element_by_css_selector('.pagination-product-grid > li:nth-child(10) > a:nth-child(1)').click() #Clickando na próxima página
        
            self.saving_prices(key) #Salvando dados em um arquivo 

    def search_prod(self, key):
        """
        Acha a barra de navegação do site faz uma busca a partir de uma key passada
        """
        
        search_bar = self.driver.find_element_by_css_selector('#h_search-input') #Achando barra de navegação
        
        search_bar.clear() #Limpando barra de navegação
        search_bar.send_keys(key) #Enviando key para a barra de navegação

        self.driver.find_element_by_css_selector('#h_search-btn').click() #Clickando no botao pesquisar

    def take_prices(self):
        """
        Pega o html da pagina acessada e extrai os dados do produto
        """
        self.page_html = bs(self.driver.page_source, 'html.parser') #Pegando e parseando o html da page
        products = self.page_html.find_all('div', {'class':'product-grid-item ColUI-gjy0oc-0 hFbhrr ViewUI-sc-1ijittn-6 iXIDWU'}) #Achando todos os conteiners dos produtos

        for prod in products: #Percorrendo cada conteiner atrás dos dados de cada produto
            name = prod.find('h2', {'class':'TitleUI-bwhjk3-15 khKJTM TitleH2-sc-1wh9e1x-1 gYIWNc'}).text #pegando a descrição do produto
            price = prod.find('span', {'class':'PriceUI-bwhjk3-11 cmTHwB PriceUI-sc-1q8ynzz-0 dHyYVS TextUI-sc-12tokcy-0 bLZSPZ'}) #Tentando pegar preço
            link = prod.find('a', {'class':'Link-bwhjk3-2 iDkmyz TouchableA-p6nnfn-0 joVuoc'})
            if link:
                link = link['href']
                link = f'{self.link}{link}'
            else:
                link = 'Não Disponivel'

            if price:
                price = price.text
            else:
                price = prod.find('span', {'class':'PriceUI-bwhjk3-11 jtJOff PriceUI-sc-1q8ynzz-0 dHyYVS TextUI-sc-12tokcy-0 bLZSPZ'})
                if price:
                    price = price.text #Tentando pegar preço novamente
                
            
            track = 'Contatar o Vendendor' 
            image = 'Not Avaible'
            if price:
                name = name.replace(',', '-')               
                self.products[name] = [price, track, link, image]


if __name__ == '__main__':

    file = 'AMdata.csv'
    key = input('Products: ')

    driver = webdriver.Firefox()
    
    AMBot = AMPrices(file, driver)
    AMBot._start(key, 1) 
