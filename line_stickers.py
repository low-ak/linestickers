#!/usr/bin/python3

import sys
import os
import requests
import re
import bs4
import pathlib

if(len(sys.argv) < 2):
    print ('No argument, usage "./line_stickers.py [url]"')
    exit(-1)

url = sys.argv[1]

main = bs4.BeautifulSoup(requests.get(url).content, 'html.parser')

title = main.find('p', {'class': 'mdCMN38Item01Ttl'}).text
tar_dir = 'stickers_' + '_'.join(title.split())

print('Downloading "'+title+'" to', tar_dir)

if not os.path.exists(tar_dir):
    os.makedirs(tar_dir)

stickers = main.findAll('span', {'class', 'mdCMN09Image'})

urlm = re.compile(r'background-image:url\((.*);compress=true\)')
namem = re.compile(r'.*sticker/([0-9]*).*')
for sticker in stickers:
    img_url = urlm.search(sticker['style']).group(1)
    name = namem.search(img_url).group(1)
    filename = tar_dir+'/'+name+pathlib.Path(img_url).suffix
    os.system('curl -o "'+filename+'" '+img_url)
