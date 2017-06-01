# init - refer to jjs.py

#coding:utf-8

from bs4 import BeautifulSoup
import urllib2

url = 'http://reeoo.com'
request = urllib2.Request(url)
response = urllib2.urlopen(request, timeout=20)

content = response.read()
soup = BeautifulSoup(content, 'html.parser')

# title
tag = soup.title
print tag
<title>Reeoo - web design inspiration and website gallery</title>
print tag.name
# title


# attribute
...
<article class="box">
    <div id="main">
    <ul id="list">
        <li id="sponsor"><div class="sponsor_tips"></div>
            <script async type="text/javascript" src="//cdn.carbonads.com/carbon.js?zoneid=1696&serve=CVYD42T&placement=reeoocom" id="_carbonads_js"></script>
        </li>
...

tag = soup.article
c = tag['class']

print c        
# [u'box']

# find all, find
通过 . 属性只能获取到第一个tag，若想获取到所有的 li 标签，可以通过 find_all() 方法
Find 只找第一个

ls = soup.article.div.ul.find_all('li')

# find by atribute ID, class_
soup.find_all(id='footer')
# [<footer id="footer">\n<div class="box">\n<p> ... </div>\n</footer>]

#class should use class_

 class_="sister"
 