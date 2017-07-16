import requests
from bs4 import BeautifulSoup
from functools import lru_cache


@lru_cache()
def search(keyword):
    resp = requests.get('http://www.doutula.com/search', {'keyword': keyword})
    soup = BeautifulSoup(resp.text, 'lxml')
    result = ((i.get('data-original'), i.get('data-backup')[:-4]) for i in soup.select('img[data-original]') if i.get('class') != ['gif'])
    return [[url if not url.startswith('//') else 'http:' + url for url in imgs] for imgs in result]


def download_gif(f, *url):
    for u in url:
        resp = requests.get(u, allow_redirects=False)
        if resp.status_code == 200:
            f.write(resp.content)
            f.flush()
            return
