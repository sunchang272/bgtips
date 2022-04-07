# -*- coding: utf-8 -*-
"""
-------------------------------------------------
Project Name: bgtips
File Name: main.py
Author: sunch
Create Date: 2022/4/7 8:36 
-------------------------------------------------
"""
from apscheduler.schedulers.background import BlockingScheduler
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import requests
import ctypes
import os


class GetGZFInfo:
    def __init__(self):
        self.wf = 'https://www.bphc.com.cn/front/noroomstaff/checkHavePlanShow'
        self.ss = 'https://www.bphc.com.cn/front/sspz/checkHavePlanShow'
        self.ks = 'https://www.bphc.com.cn/front/first/checkHavePlanShow'
        self.gk = 'https://www.bphc.com.cn/front/register/checkHavePlanShow'
        self.name = ['无房', '实时', '快速', '公开']

    def get(self):
        res = [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        for i, url in enumerate([self.wf, self.ss, self.ks, self.gk]):
            try:
                r = f'{self.name[i]}:{requests.get(url).json()}'
            except Exception as e:
                r = f'error: {url}:{e}'
            res.append(str(r))
        return '\n'.join(res)


def write_bg(pth, text, out):
    img = Image.open(pth)
    x, y = img.size
    print(x, y)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('simhei.ttf', 25, encoding='utf-8')
    draw.rectangle([(int(x * 0.74), 90), (int(x * 0.999), 255)], fill=(245, 245, 245), outline=(245, 245, 245))
    for i, line in enumerate(text.split('\n')):
        draw.text((int(x * 0.75), i * 30 + 100), line, (255, 0, 0), font=font)
    os.makedirs(out, exist_ok=True)
    out_path = os.path.join(os.getcwd(), out, os.path.basename(pth))
    img.save(out_path)
    return out_path


def change_bg(pth):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, pth, 0)


def set_bg_tips(inp):
    print(inp)
    text = GetGZFInfo().get()
    nbg = write_bg(inp, text, 'tmp')
    change_bg(nbg)


if __name__ == '__main__':
    bg = 'C:/Windows/Web/Wallpaper/Windows/img0.jpg'
    set_bg_tips(bg)
    sd = BlockingScheduler()
    sd.add_job(set_bg_tips, 'interval', minutes=1, args=(bg, ))
    sd.start()

