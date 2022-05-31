#!/usr/bin/env python
#_*_ coding: utf8 _*_

import requests
import json
import time
from bs4 import BeautifulSoup

Webhook = "https://discord.com/api/webhooks/xxxxx"

ofertasAnteriores = []

nuevos = 5

while True:

    if len(ofertasAnteriores) >= 120:
        ofertasAnteriores = ofertasAnteriores[:30]
    
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
        
    source = requests.get('https://www.chollometro.com/nuevos').text

    soup = BeautifulSoup(source, 'lxml')

    articulos = soup.find_all('div',class_='threadGrid')

    articulos = articulos[:nuevos]


    for articulo in articulos:

        if articulo.strong.a == None:
            print('Publicidad')
        else:

            titulo = articulo.strong.a.text
            print(titulo+' | '+current_time)

            if titulo in ofertasAnteriores:

              print('Repetido')

            else:

              ofertasAnteriores.append(titulo)

              print(len(ofertasAnteriores))

              product_link = articulo.find('a', class_='cept-tt thread-link linkPlain thread-title--list')
              product_link = product_link.get('href')

              image = articulo.find('img', class_='thread-image width--all-auto height--all-auto imgFrame-img cept-thread-img')
              image = image.get('src')
              print(image)
              
              precio_descuento = articulo.find('span', class_='thread-price text--b cept-tp size--all-l size--fromW3-xl')
              
              if precio_descuento == None:
                precio_descuento = "N/A"
              else:
                precio_descuento = articulo.find('span', class_='thread-price text--b cept-tp size--all-l size--fromW3-xl').text

              print("Nuevo precio :", precio_descuento)
                
              precio_normal = articulo.find('span', class_='mute--text text--lineThrough size--all-l size--fromW3-xl cept-next-best-price')
              
              if precio_normal == None:
                precio_normal = "N/A"
              else:
                precio_normal = articulo.find('span', class_='mute--text text--lineThrough size--all-l size--fromW3-xl cept-next-best-price').text


              print("Precio PVP:", precio_normal)

              descuento = articulo.find('span', class_='space--ml-1 size--all-l size--fromW3-xl cept-discount')
              
              if descuento == None:
                descuento = "N/A"
              else:
                descuento = articulo.find('span', class_='space--ml-1 size--all-l size--fromW3-xl cept-discount').text

              print("Descuento :", descuento)

              def sendwebhook():
                    data={
                        "content": "Nuevo Chollo",
                        "embeds": [
                                 {
                      "title": titulo,
                      "url": product_link,
                      "color": 0,
                      "fields": [
                        {
                          "name": "Precio Rebaja",
                          "value": precio_descuento,
                          "inline": True
                        },
                        {
                          "name": "Precio PVP",
                          "value": precio_normal,
                          "inline": True
                        },
                        {
                          "name": "Descuento",
                          "value": descuento,
                          "inline": True
                        }
                      ],
                      "author": {
                        "name": "J Monitors For Chollometro!"
                      },
                      "footer": {
                        "text": "Chollometro by jjandula22#8402 | " + current_time,
                        "icon_url": "https://wallpaperaccess.com/full/5298740.jpg"
                      },
                      "thumbnail": {
                        "url": image
                        }
                    }
                  ]
                }

                    try:
                        response = requests.post(Webhook, data=json.dumps(data), headers={'Content-Type': 'application/json'})
                    except:
                        print("Error al enviar el Webhook")


                    matches = ['uber','apple','vuelo','hotel','vacaciones','oferton','ofertón','chollazo','iphone','masaje']

                    try:

                        for articulo in matches:
                            if articulo in titulo.lower():
                                keyword = articulo
                                here={
                                    "username": "J's monitors",
                                    "content": "Keyword detected: "+keyword+" @here"
                                }
                                r = requests.post(Webhook, data=json.dumps(here), headers={"Content-Type": "application/json"})
                    except:
                        print("error checking for keywords")

              sendwebhook()

              print('Sended')
                

                

    time.sleep(3)
