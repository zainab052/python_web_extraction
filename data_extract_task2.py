import requests
from lxml import html
import mysql.connector
from mysql.connector import Error

# url and headers
base_url = 'https://gomedici.com/companies'
headers = {
	'authority': 'gomedici.com',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://gomedici.com/companies',
    'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': '_medici_session=cf25acf9907d87f608b9893d69a62231;',
}

      
# function to enter data into mysql
def insertVariblesIntoTable(company_title, company_logo, url, description, product, location, founded, website, linkedin, facebook, twitter):
    try:
        mydb = mysql.connector.connect(
          host="localhost",
          user="root",
          password="root",
          database="data_extraction",
          auth_plugin='mysql_native_password'
        )

        mycursor = mydb.cursor()

        sql = """INSERT INTO companies (COMPANY_NAME, URL, COMPANY_LOGO, DESCRIPTION, PRODUCT, LOCATION, HQ_COUNTRY, FOUNDED, WEBSITE_URL, LINKEDIN_URL, FACEBOOK_URL, TWITTER_URL) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        record = (company_title, url, company_logo, description, product, location, location, founded, website, linkedin, facebook, twitter)
        mycursor.execute(sql, record)
        mydb.commit()

        print("Record inserted successfully into Companies table")

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    finally:
        if (mydb.is_connected()):
            mycursor.close()
            mydb.close()
            print("MySQL connection is closed")



for x in range (1, 2):
    response = requests.get(base_url + '?model=Companies&page=' + str(x) + '&size=9&term=%2A&type=Filters', headers=headers)
    doc = html.fromstring(response.content)

    company_archives = doc.xpath('//div[@class="col-md-4 portfolio-item"]')
    for new in company_archives:
        title = new.xpath('.//div[@id="cp_data_box"]/h4')
        img_src = new.xpath('.//div[@id="cp-img"]/a/img')
        url = new.xpath('.//div[@id="cp-img"]/a')

        company_url = 'https://gomedici.com%s' % url[0].get("href")

        response1 = requests.get(company_url)
        doc1 = html.fromstring(response1.content)
       
        company_page = doc1.xpath('//div[@class="row py-3"]')
        company_page_1 = doc1.xpath('//div[@class="col-lg-12 pl_pr"]') 
        
        for element in company_page:
            description = element.xpath('//div[@id="cp__data_about"]/p')
            location = element.xpath('//div[@id="cp__data_cp__info"]/div[2]/span/strong')
            founded = element.xpath('//div[@id="cp__data_cp__info"]/div[1]/span/strong')
            categories = element.xpath('//div[@id="cp__data_cp__info"]/p')
            website = element.xpath('//ul[@class="technologies list-inline"]/li[1]/a')

        for x in company_page_1:
            product = x.xpath('//div[@id="cp__data_focus"]/p')

        # facebook linkedin and twitter url
        
        for i in range(2, 5):
            link = element.xpath('//ul[@class="technologies list-inline"]/li['+str(i)+']/a')
            
            if link:
                link_str = str(link[0].get("href"))
            else:
                link_str = ''

            if 'linkedin' in link_str:
                linkedin = link_str
            # else:
            #     linkedin = ''
                
            if 'twitter' in link_str:
                twitter = link_str
            elif 'twitter' not in link_str:
                twitter = ''

            if 'facebook' in link_str:
                facebook = link_str



            # print (facebook)

            
        # converting lxml element to string
        
        if title[0].text_content():
            title_string = str(title[0].text_content())
        else:
            title_string = ''

        if company_url:
            url_string = str(company_url)
        else:
            url_string = ''

        if img_src[0].get("src"):
            company_logo_str = str(img_src[0].get("src"))
        else:
            company_logo_str = ''

        if description[0].text_content():
            description_string = str(description[0].text_content())
        else:
            description_string = ''

        if product[0].text_content():
            product_string = str(product[0].text_content())
        else:
            product_string = ''
        
        if location[0].text_content():
            location_string = str(location[0].text_content())
        else:
            location_string = ''
        
        if founded[0].text_content():
            founded_integer = int(founded[0].text_content())
        else:
            founded_integer = 0000

        if categories[0].text_content():
            categories_string = str(categories[0].text_content())
            categories_string = categories_string.replace(' .', ';')

        if website[0].get("href"):
            website_string = str(website[0].get("href"))
        else:
            website_string = ''

        # insert into mysql
        insertVariblesIntoTable(title_string, company_logo_str, url_string, description_string, product_string, location_string, founded_integer, website_string, linkedin, facebook, twitter)
