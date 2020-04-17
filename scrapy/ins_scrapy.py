"""
Hanwei Wang
Time: 15-4-2020 15:27
Contact: hanwei_wang_94@outlook.com
Naming standard:
    name of a class: AbcdAbcd
    name of a method/function: abcdabcd
    name of a variable: abcd_abcd
    name of a instantiation: abcd_abcd
    # in English is the comments
    # 中文的话是需要特别注意的地方以及需要检查的地方
"""
# -*- coding: utf-8 -*-

import requests
import json
from lxml import etree
import click
import os

# =========================需要自定义的参数========================================

# 在网站不变动的情况下，只需要更改此处用户名就可以获取首页的12张图片
BASE_URL = "https://www.instagram.com/marinabondarko/"

# 存储图片的文件夹的路径
path_dir = "C:/Users/907932/Desktop/intagrsm_img"


# 添加代理，指定本地代理端口
proxies = {
    'https': 'https://127.0.0.1:38251'
}

# =========================需要自定义的参数========================================


headers = {"Referer": "https://www.instagram.com/urnotchrislee/?hl=zh-cn",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}


# 存储首页图片的真实链接的列表
img_list = []


# 下载指定链接的文件到指定目录，path是文件夹的全路径，file_url必须是以后缀名结尾的文件
def download_file(file_url, path):
    # 从链接中取出文件的名称
    filename = file_url.split("/")[-1]
    response = requests.get(file_url, headers=headers, proxies=proxies)
    fb = open(path + '/' + filename, 'wb')
    fb.write(response.content)
    fb.close()


def crawl():
    click.echo('start')

    # 判断指定存储图片的文件夹是否存在，不存在则创建
    if not os.path.exists(path_dir):
        os.makedirs(path_dir)

    try:
        # 发送请求，获取源码
        res = requests.get(BASE_URL, headers=headers, proxies=proxies)
        html = etree.HTML(res.content.decode())

        # 提取所有的script标签中的文本
        all_script_tags = html.xpath('//body/script[@type="text/javascript"]/text()')

        for script_tag in all_script_tags:
            # strip()默认过滤掉空格
            if script_tag.strip().startswith(''):
                data = script_tag.replace('window._sharedData = ', '')[
                       :-1]  # 提取json数据，必须保证{}外面没有其余数据，尾部的[:-1]去除最后一个字符，这里json数据尾部有个;
                json_data = json.loads(data, encoding='utf-8')  # 将str格式化成json格式
                # 下面的节点可能会随着网站的更新而改变
                edges = json_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media'][
                    'edges']
                for edge in edges:
                    img_url = edge['node']['display_url'] # 图片的真实链接
                    img_list.append(img_url)
                    print(edge['node']['display_url'])
                    download_file(img_url, path_dir) # 下载图片
                break
                click.echo('success')

    except Exception as e:
        raise e


if __name__ == '__main__':
    crawl()