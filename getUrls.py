import requests
from bs4 import BeautifulSoup

def getUrls(nameUrl):
    principalUrl = f'https://listado.mercadolibre.com.ar/{nameUrl}#D[A:{nameUrl}]'

    page = requests.get(principalUrl)

    soup = BeautifulSoup(page.content,'html.parser')

    products = soup.find_all('a',{'class':'ui-search-item__group__element shops__items-group-details ui-search-link'})

    urls = []

    for product in products:
        url = product.get('href')
        urls.append(url)
    with open('urls.txt','a') as f:
        for url in urls:
            f.write(f'{url}\n')
    print(f'Url producto {nameUrl} añadida con exito')
urls = [
    'iphone',
    'samsung',
    'escritorio',
    'macbook',
    'silla',
    'monitor',
    'teclado',
    'mouse',
    'termo',
    'lampara',
    'mesa de luz',
    'auriculares',
    'mopas',
    'bebida',
    'tablet',
    'aires',
    'zapatillas',
    'remera',
    'hornos',
    'heladera',
    'televisores',
    'ventiladores',
    'auto',
    'moto']
for nameUrl in urls:
    getUrls(nameUrl)



