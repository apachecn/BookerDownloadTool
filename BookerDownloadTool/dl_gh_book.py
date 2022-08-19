import requests
import json
import subprocess as subp
from pyquery import PyQuery as pq
import sys
from .util import *
import re
import os

MARKDOWN_PANEL = 'article'

tmpl = {
    "link": f"{MARKDOWN_PANEL} li a",
    "title": f"{MARKDOWN_PANEL}>h1",
    "content": f"{MARKDOWN_PANEL}",
    "remove": "a.anchor",
    "optiMode": "none",
}

def dl_gh_book(args):
    url = args.url
    proxy = None
    if args.proxy:
        proxy = {
            'http': args.proxy,
            'https': args.proxy,
        }
    
    if not url.endswith('SUMMARY.md'):
        print('请提供目录链接！')
        return
    print(url)
    readme_url = url.replace('SUMMARY.md', 'README.md')
    html = request_retry('GET', readme_url, proxies=proxy).text
    title = pq(html).find('article>h1, title').eq(0).text().strip()
    
    config = tmpl.copy()
    config['name'] = title
    config['url'] = url
    config['imgThreads'] = args.threads
    config['textThreads'] = args.threads
    config['proxy'] = args.proxy
    open('config.json', 'w', encoding='utf8') \
        .write(json.dumps(config))
    subp.Popen('crawl-epub', shell=True).communicate()
    os.remove('config.json')
            