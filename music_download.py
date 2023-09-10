import requests
import os
import time
headers = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br" ,
        "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection":"keep-alive",
        "Host": "zz123.com",
        "Referer": "https://zz123.com/search/?key=%E8%AE%B8%E5%B5%A9",
        "Sec-Fetch-Dest": "document",
         "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"
 }
# 请求键入歌手全部歌曲
singer = []
key = input("请输入歌手名，用空格隔开:\n")
key = key.split(' ')
for key in key:
    print('*' * 50)
    print('正在下载{}的歌曲...'.format(key))
    # 创建目录
    folder = os.path.exists(key)
    if not folder:
        os.mkdir(path=key)
    for i in range(1,100):
        url = "https://zz123.com/ajax/?act=search&key={}&lang=&page={}".format(key,i)
        response = requests.post(url,headers=headers,timeout=3)
        response = response.json()
        status = response.get('status')
        # 判断访问是否成功
        if status == 200:
            data = response.get('data')
            if data is not None:
                for object in data:
                    sname = object['sname']
                    if sname == key :
                        id = object['id']
                        mname = object['mname']
                        mname = mname.replace("/",'-')
                        murl = "https://zz123.com/xplay/?act=songplay&id={}".format(id)
                        music = requests.get(murl)
                        while music.content is not None:
                            try:
                                with open ('./{}/{}.mp3'.format(key,mname),'wb') as m:
                                    m.write(music.content)
                                print('{}下载成功'.format(mname))
                                break
                            except:
                                time.sleep(1)
                                print("等待中...")
            else:
                print("{}的所有歌曲已经全部下载完成！".format(key))
                print('*' * 50)
        else:
            print('网络错误，请重试...')
            exit()
print("全部下载完成!")
exit()
