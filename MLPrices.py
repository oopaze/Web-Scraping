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

class MLPrices(MainCrawler):
    """
    Get some prices of a Mercado Livre product by a keyword 
    """
    def __init__(self, file: str, driver: object):
        super().__init__(driver)
        self.link = "https://www.mercadolivre.com.br" #starter link
        self.file = file #file that receives all product found
        self.page_html = None #Html for the page that we're scraping
        self.wait = WebDriverWait(self.driver, 10)
                 
    def _start(self, key, pages = 1):
        """
        Enter in Mercado Livre website and take Prices
        """
        
        self.driver.get(self.link)
        self.test_file(self.file)

        sleep(self.transition_page)

        for prod in key.split(','): #Taking prices of each product passed
            self.products = {}
            sleep(5)
            self.search_prod(prod) #looking for products
            sleep(5)
            
            for e in range(pages):
                if self.take_prices(): #take the price of the products
                    pass

                else:
                    print('Problems to take prices. Trying again!')
                    self.take_prices() #trying to take prices again
                    
            self.saving_prices(prod) #traying to save data in a file
                 
        
    def search_prod(self, key: str):
        """
        Make a research in website by a keyword passed
        """
        
        #wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.nav-search-input'))))
        input_key = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.nav-search-input'))) #Searching the input bar 
        
        input_key.clear() #Clearing if it has some keys
        input_key.send_keys(key) #Writing our keys 
        
        input_key.send_keys(Keys.ENTER)
        
    def take_prices(self):
        """
        Taking the price of all product to the page that webdriver is in
        """
        self.page_html = bs(self.driver.page_source, 'html.parser')  #Taking the HTML of the Page
        
        data1 = self.page_html.find_all('li', {'class':'results-item highlighted article stack product'})
        data2 = self.page_html.find_all('li', {'class':'results-item highlighted article stack product item-with-attributes'}) 
        data = data1 + data2
    
        data1 = self.page_html.find_all('li', {'class':'results-item highlighted article grid product item-info-height-210'})
        data2 = self.page_html.find_all('li', {'class':'results-item highlighted article grid product item-with-attributes item-info-height-210'})
        data += data1 + data2
        
        data1 = self.page_html.find_all('div', {'class':'rowItem item product-item highlighted item--grid new with-reviews'})
        data2 = self.page_html.find_all('div', {'class':'rowItem item highlighted item--grid new'})
        data3 = self.page_html.find_all('div', {'class':'rowItem item padItem highlighted item--grid new'})
        data += data1+data2+data3
            
                    
        for i in data: # Going through the div list
            prices = i.find('span', {'class':'price__fraction'})
            
            if prices:
                prices = prices.text #Taking the element price for div[i]
                name = i.find('span', {'class':'main-title'}).text #Taking the description of the product for div[i]
                
                link = i.find('a', {'class':'item__info-link item__js-link'})
                
                if not link:
                    link = i.find('a', {'class':'item__info-title'})

                link = link['href']
                link = f'{self.link}{link}'
                image = i.find('img', {'class':'lazy-load'})


                if image:
                    image = image['src']
                elif not image:
                    image = i.find('img')['data-src']
                else:
                    image = None
                    
                try: #Testing if the track is constant
                    track = i.find('span', {'class':'text-shipping'}).text #Take the track price
                except AttributeError:
                    track = 'Contatar o vendedor' #Setting "Contatar o vendedor" like a track price
                name = name.replace(',', '-')
                self.products[name] = [prices, track, link, image] #saving the data scrapped 
                
        return True


if __name__ == '__main__':

    file = 'MLdata.csv'
    key = input('Product(s): ') #can be only one product or more than it if they are separed by commom. ex.: screen, sdd

    driver = webdriver.Firefox()
    
    MLBot = MLPrices(file, driver) #Creating de MLPrices Objects
    MLBot._start(key) #Sending the key_words reference
