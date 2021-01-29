#!/usr/bin/python3

import sys
import os
import requests
import re
import bs4
import pathlib
import json
import datetime

if(len(sys.argv) < 2):
    print ('No argument, usage "./line_stickers.py [url]"')
    exit(-1)

url = sys.argv[1]

main = bs4.BeautifulSoup(requests.get(url).content, 'html.parser')

title = main.find('p', {'class': 'mdCMN38Item01Ttl'}).text
tar_dir = 'stickers/' + '_'.join(title.split())

print('Downloading "'+title+'" to', tar_dir)

stickers = main.findAll('li', {'class', 'mdCMN09Li'})

if len(stickers) == 0:
    print("No sticker urls found")
    exit(0)

if not os.path.exists(tar_dir):
    os.makedirs(tar_dir)

metadata = {}
metadata['url'] = url
metadata['title'] = title
metadata['author'] = main.find('a', {'class': 'mdCMN38Item01Author'}).text
metadata['description'] = main.find('p', {'class': 'mdCMN38Item01Txt'}).text
metadata['download_date'] = datetime.date.today().strftime("%Y-%M-%d")
metadata['stickers'] = []

for sticker in stickers:
    info = json.loads(sticker['data-preview'])

    metadata['stickers'].append(info)

    dl = []

    if info['type'] == "static":
        dl.append(info['staticUrl'])
    elif info['type'] == "animation":
        dl.append(info['animationUrl'])
    elif info['type'] == "animation_sound":
        dl.append(info['animationUrl'])
        dl.append(info['soundUrl'])

    for dl_url in dl:
        suffix = pathlib.Path(dl_url).suffix.removesuffix(";compress=true")
        filename = tar_dir+'/'+info['id']+suffix
        
        img = requests.get(dl_url)
        open(filename, 'wb').write(img.content)
    
    print("Downloaded sticker " + info['id'])

open(tar_dir+'/metadata.json', 'w').write(json.dumps(metadata))
