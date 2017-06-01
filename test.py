from bs4 import BeautifulSoup
import urllib2

url = "http://zhongshan.jjshome.com/xq/detail/6217"
url2 = "http://zhongshan.jjshome.com/esf/a10/?n=1&s=3"
def soup_init(url):
    ## init
    request = urllib2.Request(url)
    response = urllib2.urlopen(request, timeout=20)
    
    content = response.read()
    #soup = BeautifulSoup(content, 'lxml')
    soup = BeautifulSoup(content, 'html.parser')
    
    #print soup
    return soup

def test(soup):
    soup = soup_init(url)
    data = soup.find('em', class_="total cred").string
    sd_year = soup.find(class_="intro-box2 clearfix").find_all(class_="value")[0].string[:4]
    print sd_year




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
        attr1_temp = i.find_all('p', class_="attr")[0].find_all('span')[0].string
        print attr1_temp.strip()
        attr2_temp = i.find_all('p', class_="attr")[0].find_all('span')[1].string
        attr3_temp = i.find_all('p', class_="attr")[0].find_all('span')[2].string
        attr = "%s - %s - %s" % (attr1_temp, attr2_temp, attr3_temp)
        #print attr
        item_dict['attr'] = attr
        
        #finally append to list
        items_list_temp.append(item_dict)
        
    return items_list_temp
    
soup = soup_init(url2)
web_data(soup)
