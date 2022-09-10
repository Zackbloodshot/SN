import requests 
from bs4 import BeautifulSoup as bs 


class mangakalot:
  def __init__(self, query, mid, chap):
    self.query = query 
    self.mid = mid 
    self.chap = chap 
  
  def search(query):
    query = query.replace(' ', '_')
    url = f'https://manganato.com/https://manganato.com/search/story/{query}' 
    r = requests.get(url)
    soup = bs(r.text, 'lxml')
    rel = soup.findAll('div', class_ = 'search-story-item')
    results=[]
    for i in rel:
      res = []
      res.append(i.a['title'])
      res.append(i.a['href'].split('/')[3])
      results.append(res)
    if results == []:
      return False
    return results
    
  def get_manga_details(mid):
    r = requests.get(f'https://readmanganato.com/{mid}')
    soup = bs(r.text, 'lxml')
    #print(soup)
    img = soup.findAll('div', class_='story-info-left') 
    if img == []:
    	r = requests.get(f'https://manganato.com/{mid}')
    	soup = bs(r.text, 'lxml')
    	img = soup.findAll('div', class_='story-info-left')
    #print(img)
    info = soup.findAll('div', class_='story-info-right')
    #print(info)
    kek = []
    for f in info:
      #print(f)
      hek= f.text.split('\n') 
      #print(hek)
      for i in hek:
      	if not i == '':
          #print(i)
          kek.append(i)
    for i in img:
      kek.append(i.img['src'])
    #print(kek)
    if len(kek) < 5:
      return False
    return kek
  
  def read(mid, chap):
    r = requests.get(f"https://readmanganato.com/{mid}/chapter-{str(chap)}")
    soup = bs(r.text, 'lxml')
    img = soup.findAll('div', class_ = 'container-chapter-reader')
    try:
      pages = img[0].findAll('img')
    except IndexError:
      return False
    kek = []
    for i in pages:
      kek.append(i['src'])
    if kek == []:
      return False 
    else:
      return kek
    	