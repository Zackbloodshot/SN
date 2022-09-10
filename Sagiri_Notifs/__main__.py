from telethon import events, Button
from Sagiri_Notifs import bot
from mangakalotapi import mangakalot as manga
from telegraph import upload_file
from telegraph.exceptions import TelegraphException
import page_store
import requests 
from bs4 import BeautifulSoup as bs
import asyncio
import os, zipfile 
import img2pdf
import re
from html_telegraph_poster import TelegraphPoster 
import logging
import concurrent.futures as future
import traceback

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)

logger = logging.getLogger("__name__")

loop = asyncio.get_event_loop()

poster = TelegraphPoster(use_api=True)
poster.create_api_token('Sagiri Mangas')

def plus(pagecount):
    pagecount = pagecount
    if pagecount.startswith('00'):
      to_plus = pagecount[2:]
      plus = str(int(to_plus) + 1)
      if plus == '10':
        result = f'0{plus}'
      else:
        result = f'00{plus}'
      return result 
    elif pagecount.startswith('0'):
      to_plus = pagecount[1:]
      plus = str(int(to_plus) + 1)
      if plus == '100':
        result = f'100'
      else:
        result = f'0{plus}'
      return result
    else:
	    to_plus = pagecount 
	    plus = str(int(to_plus) + 1)
	    result = plus 
	    return result 
	 
def down(page_data, direc, count):
    try:
      r = requests.get(page_data, headers={'referer': 'https://mangakakalot.com/'}) 
      file_name = f'{count}.png' 
      peth = os.path.join(direc, file_name)
      with open(peth, 'wb') as file:
        for chunk in r.iter_content(1024):
            if chunk:
              file.write(chunk)
      nyah = ['']
      try:
        nyah = upload_file(peth)
      except TelegraphException as te:
        print(te)
        pass
      #tx += f'<img src="https://telegra.ph/{nyah[0]}">'
      print(f"{direc} {file_name} done...")
      return peth, nyah[0], count
    except Exception:
      traceback.print_exc()

async def manga_downloader(mid=None, chap=None):
  tx ='Powered by <a href = "https://t.me/SagiriiRoBot">Sagiri</a>'
  sop = []
  hek = manga.read(mid, chap)
  name = manga.get_manga_details(mid)
  bru = name[0].replace(' ', '-')
  bru = re.sub('[^\w-]', '', bru)
  title = f'{bru.lower()}-chapter-{chap}'
  if title.startswith('-'):
    title = title[1:]
  direc = title
  tg='yes'
  if os.path.exists(direc):
    os.system(f'rm -rf {direc}')
    os.system(f'mkdir {direc}')
  else:
    os.system(f'mkdir {direc}')
    count = '000'
    images = []
    images_to_sort = {}
    with future.ThreadPoolExecutor() as exec_:
      exec_res = []
      for i in hek:
        proc = exec_.submit(down, i, direc, count)
        exec_res.append(proc)
        count = plus(count)
      for u in future.as_completed(exec_res):
        peth, tg_url, count = u.result()
        images_to_sort[count] = (peth, tg_url)
    for i in sorted(images_to_sort.keys()):
      value = images_to_sort.get(i)
      images.append(value[0])
      if value[1] == '':
        tg = 'no'
      tx += f'<img src="https://telegra.ph/{value[1]}">'
      print(value)
    out = direc + '.cbz'
    print(f'Writing {out}')
    z = zipfile.ZipFile(out, 'w')
    try:
      for img in images:
        z.write(img)
        print(f'{img} done...')
    finally:
      print('\n')
      z.close()
  if tg=='no':
    h = page_store.store(direc, '')
    url = 'None'
  else:
    pu = poster.post(title=f'{name[0]} chapter {chap}',author='Sagiri Mangas', text=tx, )
    url = pu['url']
    print(url)
    h = page_store.store(direc, url)
  try:
      fp = open(f'{direc}.pdf', 'wb')
      pek = img2pdf.convert(images)
      fp.write(pek)
      fp.close()
      pocu = await bot.send_file(-1001559667005, file=f'{direc}.pdf', thumb=images[0], caption=url)
  except BaseException as e:
      print(e)
      pass
  docu = await bot.send_file(-1001559667005, file=out, thumb=images[0], caption=url)
  os.remove(out)
  os.remove(f'{direc}.pdf')
  os.system(f'rm -rf {direc}')

async def send_update():
  chat = await bot.get_entity(f"https://t.me/Sagiri_manga_updates")
  while True:
      print('Loop: Running Loop...')
      r = requests.get('https://manganato.com/')
      soup = bs(r.text, 'lxml')
      divs = soup.findAll('div', class_='content-homepage-item')
      #f.write(str(divs))
      results=[]
      #check_last = page_store.get_stored("last_update")
      for i in divs:
        try:
          res = []
          res.append(i.h3.a["href"].split('/')[3])
          res.append(i.h3.a.text)
          res.append(i.p.a.text)
          msg = f'`{res[0]}`\n**•{res[1]}\n{res[2]}**'
          chap = re.sub('[^0-9\.]' , '' ,res[2].split('Chapter ')[1].split(' ')[0]) 
          print(f'{res} + {chap}')
          results.append(res)
          past_chap = ''
          if page_store.get_stored(res[0]):
            mk = page_store.get_stored(res[0])
            past_chap = re.sub('[^0-9\.]' , '' ,mk.split('Chapter ')[1].split(' ')[0])
          if past_chap == chap:
              print(f'{res[1]}-{res[2]} passed!')
          else:
             if page_store.exists(f'notif_{res[0]}'):
                 bru = res[1].replace(' ', '-')
                 bru = re.sub('[^\w-]', '', bru)
                 title = f'{bru.lower()}'
                 await manga_downloader(mid=res[0], chap=chap)
                 button = [Button.url(text = "Read", url = f'https://t.me/SagiriiRoBot?start={title}_{chap.replace(".", "o")}')]
                 #smsg = msg + f'[­ ]({url})'
                 await bot.send_message(chat, msg, buttons=button, parse_mode='md')
                 print(f'Sucess for {res[1]}')
             else:
                 print(f'No Notifs on for {res[1]}')
             page_store.store(res[0], msg)
        except Exception as e:
          txt = f'Notifs Err:\n\n{e}'
          traceback.print_exc()
          #await bot.send_message(-1001562997064, txt)
      #store = f'**•{results[0][1]}\n{results[0][2]}**'
      #print(store)
      await asyncio.sleep(180)
 
loop.run_until_complete(send_update())

bot.start()



bot.run_until_disconnected()
