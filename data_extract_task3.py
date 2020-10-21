import requests
from lxml import html
import json
import sqlalchemy as db
from sqlalchemy import create_engine, Table, Column, Integer, VARCHAR, MetaData
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
    
    response = requests.get('https://gensdeconfiance.com/api/v2/classified?category=realestate__rent&orderColumn=displayDate&orderDirection=DESC&rootLocales\[\]=en&rootLocales\[\]=fr&hidden=true&page=' + str(x) + '&dateTo=@1602677994&itemsPerPage=50', headers=headers)
    json_file = json.loads(response.text)

    for x in json_file:

        if x['title']:
            title = str(x['title'])
        else:
            title = ''

        if x['type']:
            types = str(x['type'])
        else:
            types = ''

        if x['category']:
            category = str(x['category'])
        else:
            category = ''

        if x['city']:
            city = str(x['city'])
        else:
            city = ''

        if x['zip']:
            zips = str(x['zip'])
        else:
            zips = ''

        if x['description']:
            description = str(x['description'])
        else:
            description = ''

        url = 'https://gensdeconfiance.com/fr/annonce/'+ str(x['slug'])
        response1 = requests.get(url, headers=headers1)
        doc = html.fromstring(response1.content)



        div = doc.xpath('//div[@id="content"]/div[@id="contentInner"]')
        for d in div:
            chambre = ''.join(d.xpath('//div[@class="col-md-8"]/table[@class="table text-bold bg-default br"]/tr/td[@id="ad-extra-fields-nb_rooms"]/text()'))
            surface = ''.join(d.xpath('//div[@class="col-md-8"]/table[@class="table text-bold bg-default br"]/tr/td[@id="ad-extra-fields-nb_square_meters"]/text()'))
            phone = ''.join(d.xpath('//div[@class="m-b-md"]/a/text()'))
            price = ''.join(d.xpath('//div[@class="price-table__value"]/text()'))

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
        print(type(chambre), chambre)


# engine = db.create_engine('mysql://root:24M@y!996@localhost/gensdeconfiance')
# connection = engine.connect()
# metadata = db.MetaData()



# census = db.Table('details', metadata, autoload=True, autoload_with=engine)
# query = census.insert(), data
# connection.execute(query)

meta = MetaData()

test = Table(
   'test', meta, 
   Column('id', Integer, primary_key = True), 
   Column('url', VARCHAR(1000)), 
   Column('title', VARCHAR(1000)),
   Column('type', VARCHAR(500)), 
   Column('categorie', VARCHAR(1000)),
   Column('ville', VARCHAR(500)),
   Column('cp', VARCHAR(500)),
   Column('prix', VARCHAR(500)),
   Column('description', VARCHAR(5000)),
   Column('chambres', VARCHAR(500)),
   Column('surface', VARCHAR(500)),
   Column('telephone', VARCHAR(500)),
)

meta.create_all(engine)
conn = engine.connect()
conn.execute(students.insert(), data)