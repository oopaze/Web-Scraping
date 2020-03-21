from selenium import webdriver
from bs4 import BeautifulSoup as bs
from time import sleep



class FacePrices(object):
    """
    Take the price of products searched for a key passed on Facebook MarketPlace
    It needs you facebook login to make a more specified searching 
    """
    def __init__(self, driver: object, arquivo: str, transition_page_time = 10):
        self.driver = driver
        self.produtcs = {}
        self.arquivo = arquivo
        self.transition_page_time = transition_page_time

    def _start(self, email, pw, key):
        if email and pw:
            """
            This function make log in the facebook login passed and go to market place
            """
            self.driver.get("https://www.facebook.com/")

            #Finding the Text box to input email and password        
            input_email = self.driver.find_element_by_id("email")
            input_pw = self.driver.find_element_by_id("pass")

            #Putting our data logs
            input_email.send_keys(email)
            input_pw.send_keys(pw)      
            
            #Pressing enter and come in facebook
            self.driver.find_element_by_id("u_0_b").click()
            self.login = True
            
            sleep(self.transition_page_time)
            
            #Controling the loop and erros
            if self.enter_marketplace():
                
                if self.search_prod(key):
                    self.take_prices()

                else:
                    print("Problems to search products. Trying again!")
                    sleep(self.transition_page_time)
                    self.take_prices()
            else:
                print("Problems to enter in MarketPlace. Trying again!")
                sleep(self.transition_page_time)
                self.search_prod(key)

        else:
            print("Email or Password incorrect")

    def enter_marketplace(self):
        """
        Find the button on screen and click to enter on market place from facebook
        """
        try:
            marketplace_button = self.driver.find_element_by_id("navItem_1606854132932955")
            marketplace_button.click()
            
            sleep(self.transition_page_time)
            return True
            
        except Exception:
            return False

        
    def search_prod(self, prod: str):
        """
        Making our searching in Market Place with the key passed
        """
        try:    
            prod_search = self.driver.find_element_by_css_selector("#js_4 > input:nth-child(1)")
            prod_search.send_keys(prod)

            self.driver.find_element_by_class_name("_1vi5").click()
            sleep(self.transition_page_time)
            return True
            
        except Exception:
            return False

    
    def take_prices(self):
        """
        Save the Prices of all products found on a Dictionary like dic[product] = price
        """

        html = bs(self.driver.page_source, "html.parser") #taking the HTML to the page
        data = html.find_all("div", {'class':'_7yd _4-u3'}) #finding the "div" that has our info
        for e in list(data): #Running each data to take de product and the price 
            price = e.find('div', {'class':'_f3l _4x3g'}).text.split("\xa0")
            product = e.find('img', {'class':'_7ye img'})["alt"]

            if price[0][0] == "G":
                self.produtcs[product] = price[0]
            else:
                self.produtcs[product] = price[1]

        self.saving_prices() #Saving data in a csv document
        
    def saving_prices(self):
        """
        Save each key with its values in a csv document like:
              "dic[key] = value" to csv "key,value"
        """
        data = open(self.arquivo, 'a')
        products = list(self.produtcs.keys())
        for prod in products:
            data.write(f'{prod},{self.produtcs[prod]}\n')
        data.close()
        
        self.see_prices()

    def see_prices(self):
        """
        Shows the products and prices in dictionary Produtcs
        """
        products = list(self.produtcs.keys())
        for prod in products:
            print(f'{prod} - {self.produtcs[prod]}\n')
        

arquivo = 'data.csv'

try:
    a = open(arquivo, 'r')
except FileNotFoundError:
    a = open(arquivo, 'w')
    a.write("")
    a.close()

key = input('Product: ')
email = input('Facebook Email: ')
password = input('Facebook Password: ')

firefox = webdriver.Firefox()


price_bot = FacePrices(firefox, arquivo)
price_bot._start(email, password, key)

