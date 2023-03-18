import requests
from bs4 import BeautifulSoup
from db import connection

def getImages(soup):
    containerImages = soup.find('div',{'class':'ui-pdp-gallery__column'})
    images = containerImages.find_all('img',{'class':'ui-pdp-image'})
    data = []
    for image in images:
        if (image != ''):
            data.append(image.get('data-srcset'))
    return set(data)

def getDescription(soup):
    descriptions = soup.find_all('li',{'class':'ui-vpp-highlighted-specs__features-list-item ui-pdp-color--BLACK ui-pdp-size--XSMALL ui-pdp-family--REGULAR'})
    if descriptions:
        return descriptions.text
    return None

def getOffer(soup):
    containerOffer = soup.find('span',{'class':'andes-money-amount__discount'})
    if (containerOffer):
        resultOffer = int(containerOffer[:2])
        return resultOffer
    return 0

def getQuantity(soup):
    quantity = soup.find('span',{'class':'ui-pdp-buybox__quantity__available'})
    if quantity:
        chars = '(,),disponbiles'
        resultQuantity = quantity.text.translate(str.maketrans('','',chars))
        return resultQuantity
    return 1

class Product:
    def __init__(self,title,subtitle,description,price,descriptionContent,images,offer,quantity):
        self.title = title
        self.subtitle = subtitle
        self.description = description
        self.price = int(price)
        self.descriptionContent = descriptionContent
        self.images = list(images)
        self.offer = int(offer)
        self.quantity = int(quantity)
        
    def __str__(self) -> str:
        return f'Title: {self.title}, Subtitle: {self.subtitle}, Description: {self.description}, Price: {self.price}, Description Content: {self.descriptionContent}, Images: {self.images}'
    

def getAtributtes(http):
    try:
        page = requests.get(http)
        soup = BeautifulSoup(page.content, 'html.parser')
        title = soup.find('h1',{'class':'ui-pdp-title'}).text
        subtitle = soup.find('span',{'class':'ui-pdp-subtitle'}).text
        price = soup.find('span',{'class':'andes-money-amount__fraction'}).text
        price = price.translate(str.maketrans('','','.'))
        descriptionContent = soup.find('p',{'class':'ui-pdp-description__content'}).text
        images = getImages(soup)
        description = getDescription(soup)
        offer = getOffer(soup)
        quantity = getQuantity(soup)
        if offer:
            print(http)
            print(f'Price:{price} Offer:{offer}')
        product = Product(title,subtitle,description,price,descriptionContent,images,offer,quantity)
        newProduct = (product.title,product.subtitle,product.description,product.price,product.descriptionContent,product.offer,product.quantity)
       
        try:
            with connection.cursor() as cursor:
                insertProduct = "INSERT INTO products (title, subtitle, description, price, descriptionContent, offer, quantity) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(insertProduct,newProduct)
                connection.commit()
                idProduct = cursor.lastrowid
                images = []
                for image in product.images:
                    images.append((idProduct,image))
                insertImage = "INSERT INTO images (id,image) VALUES (%s,%s)"
                cursor.executemany(insertImage,images)
                print('Producto añadido con exito!')
                connection.commit()
        except Exception as e:
            print(e)
    except Exception as e:
        print(f'ERROR: {e} HTTP: {http}')

with open('urls.txt', 'r') as f:
    for line in f:
        getAtributtes(line)
    connection.close()
