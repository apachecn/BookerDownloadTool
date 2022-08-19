import requests
import json
import os
import sys
from os import path
from moviepy.editor import VideoFileClip
from io import BytesIO
import tempfile
import uuid
from urllib.parse import quote_plus
from .util import *

def batch_home_bili(args):
    mid = args.mid
    st = args.start
    ed = args.end
    to_audio = args.audio
    for i in range(st, ed + 1):
        url = f'https://api.bilibili.com/x/space/arc/search?search_type=video&mid={mid}&pn={i}&order=pubdate'
        j = requests.get(url, headers=headers).json()
        if j['code'] != 0:
            print('解析失败：' + j['message'])
            return
        for it in j['data']['list']['vlist']:
            bv = it['bvid']
            args.id = bv
            download_bili_safe(args)

def batch_kw_bili(args):
    kw = args.kw
    st = args.start
    ed = args.end
    to_audio = args.audio
    kw_enco = quote_plus(kw)
    for i in range(st, ed + 1):
        url = f'https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword={kw_enco}&page={i}&order=pubdate'
        j = requests.get(url, headers=headers).json()
        if j['code'] != 0:
            print('解析失败：' + j['message'])
            return
        for it in j['data']['result']:
            bv = it['bvid']
            args.id = bv
            download_bili_safe(args)

def download_bili_safe(args):
    try: download_bili(args)
    except Exception as ex: print(ex)

def download_bili(args):
    id = args.id
    to_audio = args.audio
    av = ''
    bv = ''
    if id.lower().startswith('av'):
        av = id[2:]
    else:
        bv = id
        
    url = f'https://api.bilibili.com/x/web-interface/view?bvid={bv}&aid={av}'
    j = requests.get(url, headers=headers).json()
    if j['code'] != 0:
        print('获取 CID 失败：' + j['message'])
        return
    av = j['data']['aid']
    bv = j['data']['bvid']
    cid = j['data']['cid']
    title = fname_escape(j['data']['title'])
    author = fname_escape(j['data']['owner']['name'])
    print(title, author)
    name = f'{title} - {author} - {bv}'
    fname = f'out/{name}'
    if to_audio:
        fname += '.mp3'
    else:
        fname += '.flv'
    if path.isfile(fname):
        print(f'{fname} 已存在')
        return
    try: os.mkdir('out')
    except: pass
    url = f'https://api.bilibili.com/x/player/playurl?cid={cid}&otype=json&bvid={bv}&aid={av}'
    j = requests.get(url, headers=headers).json()
    if j['code'] != 0:
        print('解析失败：' + j['message'])
        return
    video_url = j['data']['durl'][0]['url']
    video = requests.get(video_url, headers=headers).content
    if not to_audio:
        open(fname, 'wb').write(video)
        return
    tmp_fname = path.join(tempfile.gettempdir(), uuid.uuid4().hex + '.flv')
    open(tmp_fname, 'wb').write(video)
    vc = VideoFileClip(tmp_fname)
    vc.audio.write_audiofile(fname)
    vc.reader.close()
    os.unlink(tmp_fname)
