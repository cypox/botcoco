import os
from datetime import datetime
import shlex, subprocess
import shutil
import filecmp
import urllib.request
from tqdm import tqdm
from multiprocessing import Pool
import http

debug = True
def print_debug(msg, echo = debug):
  if echo:
    print("[{}] {}".format(datetime.now().strftime("%H:%M"), msg))

file_id = 0
def fetch_url(link):
  try:
    temp_filename, headers = urllib.request.urlretrieve(link)
    if int(headers['Content-Length']) <= 513:
      os.remove(temp_filename)
      return
    content_type = headers['Content-Type'].split('/')[1]
    print_debug('downloading file {}'.format(link))
    filename = "images/{}.{}".format(link.split('/')[-1], content_type)
    shutil.move(temp_filename, filename)
  #except http.client.RemoteDisconnected:
  except:
    #print_debug('exception occured!')
    return

name = input('input username for whom to crawl: ')

links = []
for i in range(1000, 10000):
  for j in range(0, 10):
    for server in ['pix1']:
      for extention in ['png', 'jpg', 'jpeg']:
      #for extention in ['jpeg']:
        link = "https://{}.coco.fr/upload/{}/{}-{}.{}".format(server, j, name, i, extention)
        links.append(link)

print_debug('checking {} link'.format(len(links)))

with Pool(16) as p:
  r = list(tqdm(p.imap_unordered(fetch_url, links), total=len(links)))
