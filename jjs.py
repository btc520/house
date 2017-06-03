#! /usr/bin/python
#-*- encoding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
from csv_handle import csv_readlist, csv_writelist



def house_data(area):
    house_list = []
    for i in range(1,9):
        url = 'http://zhongshan.jjshome.com/esf/%s/?n=%s&s=3' % (area, i)
        soup_data = soup_init(url)
        items_list_temp = web_data(soup_data)
        for items in items_list_temp:
            house_list.append(items)
    return house_list
    
def sd_price_update(house_list):
    # update subdistrict price and year
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
    
    for i in house_list:
        if i['bias'] <= 0 and 'check' in i.keys():
            i['check'] = i['check']+'/价格高'
        elif i['bias'] <= 0:
            i['check'] = '价格高'
                
    for i in house_list:
        if i['sd_year'] != '暂无数据' and float(i['sd_year']) < 2005.0 and 'check' in i.keys():
            i['check'] = i['check']+'/老小区'
        elif i['sd_year'] != '暂无数据' and float(i['sd_year']) < 2005.0:
            i['check'] = '老小区'
            
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
        attr1_temp = i.find_all('p', class_="attr")[0].find_all('span')[0].string.strip().encode('utf-8')
        attr2_temp = i.find_all('p', class_="attr")[0].find_all('span')[1].string.encode('utf-8')
        attr3_temp = i.find_all('p', class_="attr")[0].find_all('span')[2].string.encode('utf-8')
        
        attr4_temp = i.find_all('p', class_="attr")[1].find_all('span')[0].string.strip().encode('utf-8')
        attr5_temp = i.find_all('p', class_="attr")[1].find_all('span')[1].string.strip().encode('utf-8')
        
        attr_len = i.find_all('p', class_="attr")[1].find_all('span')
        if len(attr_len) == 3:
            attr6_temp = i.find_all('p', class_="attr")[1].find_all('span')[2].string.encode('utf-8')
            
            attr = "%s-%s-%s-%s-%s-%s" % (attr1_temp, attr2_temp, attr3_temp, attr4_temp, attr5_temp, attr6_temp)
        else:
            attr = "%s-%s-%s-%s-%s" % (attr1_temp, attr2_temp, attr3_temp, attr4_temp, attr5_temp)
        if attr1_temp == '车位' and 'check' in item_dict.keys():
            item_dict['check'] = item_dict['check']+'/车位'
        elif attr1_temp == '车位':
            item_dict['check'] = '车位'
            
        if (attr1_temp[0] == '0' or attr1_temp[0] == '1' or attr1_temp[0] == '2') and 'check' in item_dict.keys():
            item_dict['check'] = item_dict['check']+'/小户'
        elif attr1_temp[0] == '0' or attr1_temp[0] == '1' or attr1_temp[0] == '2':
            item_dict['check'] = '小户'
            
        if attr5_temp.decode('utf-8')[0] == u'高' and 'check' in item_dict.keys():
            item_dict['check'] = item_dict['check']+'/高楼层'
        elif attr5_temp.decode('utf-8')[0] == u'高':
            item_dict['check'] = '高楼层'
            
        item_dict['attr'] = attr
        
        #finally append to list
        items_list_temp.append(item_dict)
        
    return items_list_temp
    
if __name__ == "__main__":
    file_path = '/srv/www/idehe.com/house/'
    area = "a5"
    file = 'house_data_%s.csv' % (area)
    
    h_data = house_data(area)
    
    h_data_add_sd_price = sd_price_update(h_data)
    
    #print h_data
    
    csv_writelist(file, file_path, h_data_add_sd_price)

