import requests
from lxml import html, etree
import json
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker
import pandas as pd


# header for json page
headers = {
    'authority': 'gensdeconfiance.com',
    'accept': 'application/json',
    'x-requested-with': 'XMLHttpRequest',
    'accept-language': 'fr',
    'uniquedeviceid': '5f86bee5a7b67',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36',
    'apptoken': 'add5c5ff18e92207d58de9be8635a64c',
    'appvanity': '5f86bee5a7b67',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://gensdeconfiance.com/fr/s/immobilier/locations-immobilieres?rootLocales=en%2Cfr&currentAdSort=displayDate_desc',
    'cookie': 'session=7tn165u24eetjrqhd2oot0nidbec9johl6r8aesm6fk3o4pv;',
}

# header for each ad
headers1 = {
    'authority': 'gensdeconfiance.com',
    'content-length': '0',
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    'origin': 'https://gensdeconfiance.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://gensdeconfiance.com/fr/annonce/loue-appartement-de-fonction-99m-chatou-f14932e',
    'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'session=7tn165u24eetjrqhd2oot0nidbec9johl6r8aesm6fk3o4pv;',
}


data = []
for x in range(1, 2):
    myparser = etree.HTMLParser(encoding="utf-8")
    response = requests.get('https://gensdeconfiance.com/api/v2/classified?category=realestate__rent&orderColumn=displayDate&orderDirection=DESC&rootLocales\[\]=en&rootLocales\[\]=fr&hidden=true&page=' + str(x) + '&dateTo=@1602677994&itemsPerPage=100', headers=headers)
    json_file = json.loads(response.content)

    for x in json_file:

        if 'type' in x:
            types = str(x['type'])
        else:
            types = ''

        if 'category' in x:
            category = str(x['category'])
        else:
            category = ''

        if 'city' in x:
            city = str(x['city'])
        else:
            city = ''

        if 'price' in x:
            price = str(x['price'])
        else:
            price = ''

        if 'zip' in x:
            zips = str(x['zip'])
        else:
            zips = ''

        url = 'https://gensdeconfiance.com/fr/annonce/'+ str(x['slug'])
        response1 = requests.get(url, headers=headers1)
        doc = html.fromstring(response1.content, parser=myparser)



        div = doc.xpath('//div[@id="content"]/div[@id="contentInner"]')
        for d in div:
            title = ''.join(d.xpath('//h1[@id="post-title"]/text()'))
            title = title.replace('  ', '')
            chambre = ''.join(d.xpath('//div[@class="col-md-8"]/table[@class="table text-bold bg-default br"]/tr/td[@id="ad-extra-fields-nb_rooms"]/text()'))
            chambre = chambre.replace('\n', '')
            chambre = chambre.replace('  ', '')
            surface = ''.join(d.xpath('//div[@class="col-md-8"]/table[@class="table text-bold bg-default br"]/tr/td[@id="ad-extra-fields-nb_square_meters"]/text()'))
            surface = surface.replace('\n', '')
            surface = surface.replace('  ', '')
            phone = ''.join(d.xpath('//div[@class="m-b-md"]/a/text()'))
            phone = phone.replace('\n', '')
            phone.replace('  ', '')
            description = ''.join(d.xpath('//div[@id="ad-description"]/text()', encoding="utf-8"))
            description = description.replace('\n', '')
            description = description.replace('  ', '')

            datas = {
            'url' : url,
            'title' : title,
            'type' : types,
            'categorie': category,
            'ville': city,
            'cp': zips,
            'prix': price,
            'description' : description,
            'chambres': chambre,
            'surface': surface,
            'telephone' : phone,
            }

        data.append(datas)
        


engine = db.create_engine('mysql://root:24M@y!996@localhost/gensdeconfiance', echo=True, convert_unicode=False, encoding="utf-8")
Base = declarative_base()

class RoomDetails(Base):
   __tablename__ = 'room_details'
   
   id = Column(Integer, primary_key = True)
   url = Column(String(5000))
   title = Column(String(1000))
   types = Column(String(500))
   categorie = Column(String(1000))
   ville = Column(String(500))
   cp = Column(String(500))
   prix = Column(String(500))
   description = Column(String(5000))
   chambres = Column(String(500))
   surface = Column(String(500))
   telephone = Column(String(500))


Base.metadata.create_all(engine)
Session = sessionmaker(bind = engine)
session = Session()


for d in data: 
    print(d)  
    try:
        d1 = RoomDetails(url = d['url'], title = d['title'], types=d['type'], categorie=d['categorie'], ville=d['ville'], cp=d['cp'], 
        prix=d['prix'], description=d['description'], chambres=d['chambres'], surface=d['surface'], telephone=d['telephone'])
        session.add(d1)
        session.commit()
        print("Success")
    except:
        print("An error occured")

 
