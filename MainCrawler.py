from selenium import webdriver

class MainCrawler(object):
    def __init__(self, driver):
        self.landmarks = {}
        self.driver = driver
        self.transition_page = 2  #response time for each page transition
        self.products = {} #products found

    def save_landmarks(self, key, landmark, file):
        """
        Salvando marcas achadas
        """
        try:
            with open(file, 'r') as a:
                pass
            
        except FileNotFoundError:         
            a = open(file, 'w') #Criando
            a.write('category, landmarks, \n')

        self.reading_landmarks(file)
        
        key = key.split(' ')[0]
        if landmark not in self.landmarks[key]:
            a = open(file, 'a')
            a.write(f'{key},{landmark},\n')
            self.landmarks[key].append(landmark)

    def saving_prices(self, category: str):
        """
        Writing in a document all products and prices found
        """
        category = self.name_formatter(category)
        a = open(self.file, 'a')
        for elem in list(self.products.keys()):
            price = self.products[elem][0].replace('.', '')
            price = price.replace(',', '.')
            price = self.price_formatter(price)
            
            track = self.products[elem][1].replace(',', ' ')
            
            link = self.products[elem][2].replace(',', ' ')
            
            image = self.products[elem][3].replace(',', ' ')
            
            elem = self.name_formatter(elem)
            

            a.write(f'{category},{elem},{price},{track},{link},{image},\n')
        a.close()
        self.get_landmarks(category)

    def get_landmarks(self, category):
        controle = False
        if len(list(self.products.items())) > 4:
            for e in range(len(self.file)-1, -1, -1):
                if self.file[e] == '/':
                    path = self.file[:e+1]
                if self.file[e:e+2] == 'KB' or self.file[e:e+6] == 'Luiza':
                    controle = True

            
            
            if controle:
                category = category.split(' ')[0]
                self.landmarks[category] = []
                for e in self.products.keys():
                    landmarks = self.products[e][-1]
                    self.save_landmarks(category, landmarks, f'{path}/landmarks.csv')

    def test_file(self, file):
        """
        Testando se um arquivo já existe ou necessita ser criado
        """
        try: 
            a = open(file, 'r')
            a.close()

        except FileNotFoundError: #Creating a file if not exists
            a = open(file, 'w')
            a.write("Category,Product,Price,Track,link,image\n")
            a.close()

    def reading_landmarks(self, file):
        data_landmarks = open(file, 'r')
        keys = []
        for mark in data_landmarks.readlines():
            key, marca, void = mark.split(',')
            if key not in keys and key != 'category':
                keys.append(key)
                self.landmarks[key] = []
                
            if key != 'category':
                self.landmarks[key].append(marca)

    def name_formatter(self, name):
        caractesres_upper = 'abcdefghijklmnopqrstuwvxyz'.upper()
        caracteres = f' {caractesres_upper}abcdçefghijklwmnopqrstuvxyz1234567890-'
        name = name
        caracteres_tirar = []

        for i in range(0, len(name)):
            if name[i] not in caracteres:
                caracteres_tirar.append(name[i])  

        for i in caracteres_tirar:
            name = name.replace(i, '')
            
        return name

    def price_formatter(self, price: str):
        """
        Função responsavel por pegar strings e extrair precos dessas
        """
        first_num = 0
        for e in range(0, len(price)):
            if price[e] == '$':
                first_num = e
            elif price[e] == '.' or price[e] == ',':
                price = price[first_num+1:e+3]
                return price
        return price[first_num+1:]



if __name__ == '__main__':
    a = MainCrawler()
    print(a.price_formatter('R$ 1000.10'))
