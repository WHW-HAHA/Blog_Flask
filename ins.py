"""
Hanwei Wang
Time: 19-3-2020 21:08
Contact: hanwei_wang_94@outlook.com
Naming standard:
    name of a class: AbcdAbcd
    name of a method/function: abcdabcd
    name of a variable: abcd_abcd
    name of a instantiation: abcd_abcd
    # in English is the comments
    # 中文的话是需要特别注意的地方以及需要检查的地方
"""
import requests
import re
import time
import random
import os

class InstaSpider(object):

    def __init__(self, user_name, path_name=None):
        # 初始化要传入ins用户名和保存的文件夹名
        self.path_name = path_name if path_name else user_name
        # 不能多余链接
        s = requests.session()
        s.keep_alive = False  # 关闭多余连接

        # self.url = 'https://www.instagram.com/real__yami/'
        self.url = 'https://www.instagram.com/{}/'.format(user_name)
        self.headers = {
            'user-agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            'cookie':'_zap=db73c2ad-e8d1-49ea-8c62-4b513a6aa596; d_c0="AMDjV5PmFw-PTsfRAO25A2y7EQGzTHCOYaE=|1552081985"; _xsrf=ufNC1DAMcMRnyiw5eUtBxXTqaDvRbDEV; __gads=ID=efda01f93a32a139:T=1554219498:S=ALNI_MZ_cBvUuhxh0N5lxzE6EVbbksOi4w; __utmv=51854390.100-1|2=registration_date=20150812=1^3=entry_date=20150812=1; z_c0=Mi4xRm56NEFRQUFBQUFBd09OWGstWVhEeGNBQUFCaEFsVk5URWFFWGdDbjFab19pNUhreW9fa2RWa0haaG9WbmJtVWZ3|1570175052|dce69e5af1b87b69fb7d25066f043ffa6d35d43a; __utmz=51854390.1577956485.5.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=51854390.1286199945.1557578357.1577956485.1578404420.6; _ga=GA1.2.1286199945.1557578357; tst=r; _gid=GA1.2.655072404.1584093349; q_c1=b7c323f0929742e285f8140cb173ec33|1584178686000|1552081988000; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1584613586,1584614186,1584648253,1584651772; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1584651772; _gat_gtag_UA_149949619_1=1; KLBRSID=0a401b23e8a71b70de2f4b37f5b4e379|1584651800|1584648250'
                # 'mid=XSwv4QAEAAFW11cdpyy8JA7wApon; shbid=15221; shbts=1564034657.7138138; rur=PRN; csrftoken=2e3tilTgSaWFNM6edEVPrVVw3Cg3yDoM; urlgen="{\"124.248.219.228\": 38478}:1hqZEL:RsTRCP2YQEvHXqKa_VBZLFXDM58"'
        }
        # 保存所有的图片和视频地址
        self.img_url_list = []
        self.uri = 'https://www.instagram.com/graphql/query/?query_hash=f2405b236d85e8296cf30347c9f08c2a&variables=%7B%22id%22%3A%22{user_id}%22%2C%22first%22%3A12%2C%22after%22%3A%22{cursor}%22%7D'


    def parse_html(self):
        # 获取信息:刚开始的12条图片,id,cursor
        html_str = requests.get(url=self.url, headers=self.headers).text
        # 获取12条图片地址
        url_list = re.findall('''display_url":(.*?)\\u0026''', html_str)
        # print(len(url_list))
        self.img_url_list.extend(url_list)
        # 获取用户id
        user_id = re.findall('"profilePage_([0-9]+)"', html_str, re.S)[0]
        # print(user_id)
        # 获取有值的cursor
        cursor_list = re.findall('"has_next_page":true,"end_cursor":(.*?)}', html_str, re.S)
        while len(cursor_list) > 0:
            # 默认访问12张图片
            try:
                next_page_url = self.uri.format(user_id=user_id, cursor=cursor_list[0]).replace('"', '')
                print(next_page_url)
                next_html_str = requests.get(next_page_url, headers=self.headers).text
                # 获取12条图片地址
                next_url_list = re.findall('''display_url":(.*?)\\u0026''', next_html_str)
                video_list = re.findall('"video_url":(.*?),', next_html_str)
                if len(video_list) > 0:
                    next_url_list.extend(video_list)
                self.img_url_list.extend(next_url_list)
                cursor_list = re.findall('"has_next_page":true,"end_cursor":(.*?)}', next_html_str, re.S)
                print(len(cursor_list))
                time.sleep(random.random())
            except Exception as e:
                print(e)
                break
        print(len(self.img_url_list))
        self.img_url_list = list(set(self.img_url_list))
        print('去重后', len(self.img_url_list))
        self.download_img()


    def download_img(self):
        # 开始下载图片，生成文件夹再下载
        dirpath = 'C:/Users/907932/Desktop/instagram/{}'.format(self.path_name)
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)
        for i in range(len(self.img_url_list)):
            print('\n正在下载第{0}张：'.format(i), '还剩{0}张'.format(len(self.img_url_list)-i-1))
            try:
                response = requests.get(self.img_url_list[i].replace('"', ''), headers=self.headers, timeout=10)
                if response.status_code == 200:
                    content = response.content
                    # 判断后缀
                    endw = 'mp4' if r'mp4?_nc_ht=scontent.cdninstagram.com' in self.img_url_list[i] else 'jpg'
                    file_path = r'C:/Users/907932/Desktop/instagram/{path}/{name}.{jpg}'.format(path=self.path_name, name='%04d' % random.randint(0, 9999), jpg=endw)
                    with open(file_path, 'wb') as f:
                        print('第{0}张下载完成： '.format(i))
                        f.write(content)
                        f.close()
                else:
                    print('请求照片二进制流错误, 错误状态码：', response.status_code)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    # 输入用户名和保存的文件夹名，如果没有文件夹名就和用户名同名
    ins_spider = InstaSpider(user_name='cathrynli')
    ins_spider.parse_html()
