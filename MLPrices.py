from selenium import webdriver
from bs4 import BeautifulSoup as bs
from time import sleep

class MLPrices(object):
    """
    Get some prices of a Mercado Livre product by a keyword 
    """
    def __init__(self, driver: object, file: str, transition_page = 10):
        self.driver = driver
        self.link = "https://www.mercadolivre.com.br/" #starter link
        self.products = {} #products found
        self.file = file #file that receives all product found
        self.transition_page = transition_page #response time for each page transition
        self.page_html = None #Html for the page that we're scraping
            
        
    def _start(self, key):
        """
        Enter in Mercado Livre website and take Prices
        """
        self.driver.get(self.link)

        sleep(self.transition_page)

        for prod in key.split(','): #Taking prices of each product passed
            self.search_prod(prod) #looking for products
            sleep(self.transition_page)

            if self.take_prices(): #take the price of the products
                self.saving_prices(prod) #saving data in a file

            else:
                print('Problems to take prices. Trying again!')
                self.take_prices() #trying to take prices again
                self.saving_prices(prod) #traying to save data in a file
        
        self.driver.close() #Closing the Browser

    def pass_page(self):
       pass 

    def search_prod(self, key: str):
        """
        Make a research in website by a keyword passed
        """
        input_key = self.driver.find_element_by_css_selector(".nav-search-input") #Searching the input bar 
        input_key.clear() #Clearing if it has some keys
        input_key.send_keys(key) #Writing our keys 
    
        self.driver.find_element_by_css_selector(".nav-search-btn").click() #Clilcking on the search button
        
        
    def take_prices(self):
        """
        Taking the price of all product to the page that webdriver is in
        """
        try:
            self.page_html = bs(self.driver.page_source, 'html.parser')  #Taking the HTML of the Page
            data = list(self.page_html.find_all('div', {'class':'item__info item__info--with-reviews'})) #Find a list of div that has this class 
            for i in data: # Going through the div list
                prices = i.find('span', {'class':'price__fraction'}).text #Taking the element price for div[i]
                product = i.find('span', {'class':'main-title'}).text #Taking the description of the product for div[i]
                try: #Testing if the track is constant
                    track = i.find('span', {'class':'text-shipping'}).text #Take the track price
                except AttributeError:
                    track = 'Contatar o vendedor' #Setting "Contatar o vendedor" like a track price

                self.products[product] = [prices, track] #saving the data scrapped 
            
            return True
        
        except Exception:
            return False

    def saving_prices(self, category: str):
        """
        Writing in a document all products and prices found
        """
        a = open(self.file, 'a')
        for elem in list(self.products.keys()):
            price = self.products[elem][0]
            track = self.products[elem][1]
            a.write(f'{category},{elem},{price},{track}\n')
        a.close()

if __name__ == '__main__':

    file = 'DataSets/MLdata.csv'
    try: #Creating a file if not exists
        a = open(file, 'r')
        a.close()

    except FileNotFoundError:
        a = open(file, 'w')
        a.write("Category,Product,Price,Track\n")
        a.close()

    key = input('Product(s): ') #can be only one product or more than it if they are separed by commom. ex.: screen, sdd

    firefox = webdriver.Firefox() #Starting the WebDriver

    MLBot = MLPrices(firefox, file) #Creating de MLPrices Objects
    MLBot._start(key) #Sending the key_words reference
