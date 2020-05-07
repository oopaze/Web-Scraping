from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
from time import sleep
try:
    from Crawlers.MainCrawler import MainCrawler
except ModuleNotFoundError:
    from MainCrawler import MainCrawler

class FacePrices(MainCrawler):
    """
    Take the price of products on Facebook's MarketPlace searched for a key passed
    It needs you facebook login to make a more specified searching 
    """
    def __init__(self, arquivo: str, driver: object):
        super().__init__(driver)
        
        self.link = "https://www.facebook.com"
        self.arquivo = arquivo

    def _start(self, email, pw, key):
        """
        This function make log in the facebook login passed and go to market place
        """
        
        self.products = {}
        self.test_file(self.arquivo)

        if email and pw:
            self.driver.get(self.link)

            try:
                #Finding the Text box to input email and password        
                input_email = self.driver.find_element_by_id("email")
                input_pw = self.driver.find_element_by_id("pass")

                #Putting our data logs
                input_email.send_keys(email)
                input_pw.send_keys(pw)      
                
                #Pressing enter and come in on facebook
                self.driver.find_element_by_id("u_0_b").click()
                self.login = True
                
            except Exception as e:
                pass
            
            sleep(self.transition_page+2)
            
            #Controling the loop and erros
            if self.enter_marketplace():
                sleep(self.transition_page)
                try:
                    self.driver.find_element_by_css_selector('._1c2z > a:nth-child(1) > div:nth-child(1)').click()
                    sleep(self.transition_page)
                except Exception as e:
                    print(e)
                
                for prod in key.split(','):

                    sleep(self.transition_page)

                    if self.search_prod(prod):
                        self.take_prices()
                        self.saving_prices(prod) #Saving data in a csv document

                    else:
                        print("Problemas ao procurar produtos. Tentando Novamente!")
                        sleep(self.transition_page)
                        self.search_prod(prod)
                        self.take_prices()
                        self.saving_prices(prod)
            else:
                print("Problemas ao entrar no MarketPlace. Tentando Novamente!")
                sleep(self.transition_page)
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
            
            sleep(self.transition_page)
            return True
            
        except Exception:
            return False

    def search_prod(self, prod: str):
        
        """
        Making our searching in Market Place with the key passed
        """
        try:
            sleep(self.transition_page)
            try:
                prod_search = self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[1]/div/div[4]/div/div/span/span/label/input")
            except Exception as e:
                prod_search = self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[1]/div/div[4]/div/div/span/span")
                               
            prod_search.clear()
            prod_search.send_keys(prod)

            prod_search.send_keys(Keys.ENTER)

            
            return True
            
        except Exception as e:
            return False

    def take_prices(self):
        """
        Save the Prices of all products found on a Dictionary like dic[product] = price
        """
        html = bs(self.driver.page_source, "html.parser") #taking the HTML to the page
        data = html.find_all("div", {'class':'_7yd _4-u3'}) #finding the "div" that has our info
        for e in list(data): #Running each data to take de product and the price 
            price = e.find('div', {'class':'_f3l _4x3g'}).text
            
            product = e.find('img', {'class':'_7ye img'})["alt"]
            product = product.replace(',', ' ')
            image = e.find('img', {'class':'_7ye img'})['src']
            link = None
            
            
            if price[0][0] == "G" or price[0][0] == "C":
                pass
            else:
                self.products[product.replace('\n', '')] = [price, link, image]
      
    def saving_prices(self, key):
        """
        Save each key with its values in a csv document like:
              "dic[key] = value" to csv "key,value"
        """
        data = open(self.arquivo, 'a')
        products = list(self.products.keys())
        for prod in products:
            produto = self.name_formatter(prod)
            data.write(f'{key},{produto},{self.products[prod][0]},{self.products[prod][1]},{self.products[prod][2]},\n')
        data.close()
        
    def see_prices(self):
        """
        Shows the products and prices in dictionary products
        """
        products = list(self.products.keys())
        for prod in products:
            print(f'{prod} - {self.products[prod]}\n')
        

if __name__ == '__main__':
    arquivo = 'FBdata.csv'
    
    key = input('Product: ')
    email = input('Facebook Email: ')
    password = input('Facebook Password: ')
    driver = webdriver.Firefox()

    FBBot = FacePrices(arquivo, driver)
    FBBot._start(email, password, key)
