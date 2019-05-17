from requests_html import HTMLSession
import os
from pathlib import Path

session = HTMLSession()
session.get('http://kns.cnki.net/kns/brief/result.aspx')
r = session.get('http://kns.cnki.net/kcms/detail/frame/list.aspx?dbcode=CJFQ&filename=syxb201202010&dbname=CJFD2012&RefType=3&vl=')
# before = r.html.text
#print('rendering')
#r.html.render()
'''
after = r.html.text
if r.html.find('div.map'):
  map_div = r.html.find('div.map', first=True)
if before == after:
    print("failed")
else:

    print(before)
    print("=========================")
    print(after)
#print(map_div.text)
'''
dblist = ['CJFQ','CDFD','CMFD','CPFD','IPFD','CCND','CCJD']
for i in dblist:
  span = r.html.find("span[id=%s]"%i, first=True)
  if span:
      if span.search('共{num}页'):
          print('dodo')
      else:
          print("non")

# print(int(span.search('共{num}页')['num']))

