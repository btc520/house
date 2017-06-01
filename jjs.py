#! /usr/bin/python
#-*- encoding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
from csv_handle import csv_readlist, csv_writelist



def house_data():
    house_list = []
    for i in range(1,6):
        url = 'http://zhongshan.jjshome.com/esf/a10/?n=%s&s=3' % (i)
        soup_data = soup_init(url)
        items_list_temp = web_data(soup_data)
        for items in items_list_temp:
            house_list.append(items)
    return house_list
    
def sd_price_update(house_list):
    sd_list = []
    for i in house_list:
        if i['sd_url'] not in sd_list:
            sd_list.append(i['sd_url'])
    
    for i in sd_list:
        url = "http://zhongshan.jjshome.com%s" % (i)
        soup = soup_init(url)
        sd_price = soup.find('em', class_="total cred").string
        sd_year = soup.find(class_="intro-box2 clearfix").find_all(class_="value")[0].string[:4]
        for j in house_list:
            if i == j['sd_url']:
                j['sd_price'] = sd_price
                j['bias'] = float(sd_price) - float(j['price'])
                j['sd_year'] = sd_year.encode('utf-8')
    return house_list
                
        
def soup_init(url):
    ## init
    request = urllib2.Request(url)
    response = urllib2.urlopen(request, timeout=20)
    
    content = response.read()
    #soup = BeautifulSoup(content, 'lxml')
    soup = BeautifulSoup(content, 'html.parser')
    
    #print soup
    return soup


def web_data(soup):
    ## make dict
    items_list_temp = []
    
    get_items = soup.find_all(class_='item clearfix')
    
    for i in get_items:
        item_dict = {}
        # find unit price
        price_temp = i.find(class_='sub').string.encode('utf-8') ## unicode to utf
        price_temp_digi = filter(str.isdigit, price_temp)
        
        item_dict['price'] = price_temp_digi
    
        # find url
        url_temp = i.find(class_="tit").find('a', href=True)['href']
        
        item_dict['url'] = url_temp
        
        # find title
        title_temp = i.find(class_="tit").find('a', href=True).string.encode('utf-8')
        item_dict['title'] = title_temp
        
        # find subdistrict
        sd_temp = i.find_all(class_="attr")[2].find('a', href=True).string.encode('utf-8')
        sd_url_temp = i.find_all(class_="attr")[2].find('a', href=True)['href']
        item_dict['sd'] = sd_temp
        item_dict['sd_url'] = sd_url_temp
        
        
        # find floor, size
        attr11_temp = i.find_all('p', class_="attr")[0].find_all('span')[0].string.strip().encode('utf-8')
        attr12_temp = i.find_all('p', class_="attr")[0].find_all('span')[1].string.encode('utf-8')
        attr13_temp = i.find_all('p', class_="attr")[0].find_all('span')[2].string.encode('utf-8')
        #attr1 = "%s-%s-%s" % (attr11_temp, attr12_temp, attr13_temp)
        attr21_temp = i.find_all('p', class_="attr")[1].find_all('span')[0].string.strip().encode('utf-8')
        attr22_temp = i.find_all('p', class_="attr")[1].find_all('span')[1].string.encode('utf-8')
        #attr23_temp = i.find_all('p', class_="attr")[1].find_all('span')[2].string.encode('utf-8')
        #attr2 = "%s-%s" % (attr21_temp, attr22_temp)
        attr = "%s-%s-%s-%s-%s" % (attr11_temp, attr12_temp, attr13_temp, attr21_temp, attr22_temp)
        #print attr
        item_dict['attr'] = attr
        #item_dict['attr2'] = attr2
        
        #finally append to list
        items_list_temp.append(item_dict)
        
    return items_list_temp
    
if __name__ == "__main__":
    file_path = '/srv/www/idehe.com/house/'
    file = 'house_data.csv'
    
    h_data = house_data()
    
    h_data_add_sd_price = sd_price_update(h_data)
    
    #print h_data
    
    csv_writelist(file, file_path, h_data_add_sd_price)

