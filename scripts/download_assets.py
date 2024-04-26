import argparse
from os.path import join, exists
from requests import get
from bs4 import BeautifulSoup
import sys
import re
import aiohttp
import asyncio


IMAGE_PATH = 'https://www.michaelfogleman.com/static/nes'
URL = 'https://www.michaelfogleman.com/static/nes/index.html'

def get_name(img, name):
    ext = img.split('.')[1]
    pattern = re.compile(r'[^a-zA-Z0-9]+')
    filename = re.sub(pattern, '_', name.lower())
    return f'{filename}.{ext}'

async def download_image(session, url, filename):
    if exists(filename):
        return
    async with session.get(url) as response:
        if response.status == 200:
            with open(filename, 'wb') as f:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)
            print(f"Downloaded: {url} -> {filename}")
        else:
            print(f"Failed to download: {url}")

async def download_images(urls):
    async with aiohttp.ClientSession() as session:
        for name, filename, url in urls:
            await download_image(session, url, filename)

def fetch_index(output_path):
    res = get(URL)
    print(res.status_code)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        div_thumbs =  soup.find('div', class_='thumbnails')
        if div_thumbs:
            divs = div_thumbs.find_all('div')
            with open(join(output_path, 'list.txt'), 'w') as fp:
                for div in divs:
                    img = div.find('img').get('src')
                    name = div.find('p').text
                    filename = get_name(img, name)
                    fp.write(f'{name};{filename}\n')
                    yield name, join(output_path, filename), f'{IMAGE_PATH}/{img}'
                    fp.flush()

async def start(path):
    index = fetch_index(path)
    await download_images(index)


def main(argv):
    parser = argparse.ArgumentParser(description='Download Assets.')

    parser.add_argument(
        '-p',
        '--path',
        metavar='PATH',
        type=str,
        help='Output PATH name',
    )

    try:
        path = 'assets/screens'
        asyncio.run(start(path))

    except argparse.ArgumentError as e:
        parser.print_help()
        exit(1)


if __name__ == '__main__':
    main(sys.argv[1:])
