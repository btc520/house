#coding:utf-8

from bs4 import BeautifulSoup
import urllib2

url = 'http://reeoo.com'
request = urllib2.Request(url)
response = urllib2.urlopen(request, timeout=20)

content = response.read()
soup = BeautifulSoup(content, 'html.parser')

print soup