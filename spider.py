
import urllib.parse
import requests
import re

def get__page_html(songname):
    url = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp"
    header = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
    params = {
        'ct': 24,
        'qqmusic_ver': 1298,
        'new_json': 1,
        'remoteplace':'txt.yqq.song',
        'searchid': 62879858846249104,
        't': 0,
        'aggr': 1,
        'cr': 1,
        'catZhida': 1,
        'lossless': 0,
        'flag_qc': 0,
        'p': 1,
        'n': 20,
        'w':songname,
        'g_tk': 5381,
        'jsonpCallback':'MusicJsonCallback9344200076073452',
        'loginUin': 0,
        'hostUin': 0,
        'format':'jsonp',
        'inCharset':'utf8',
        'outCharset':'utf - 8',
        'notice': 0,
        'platform':'yqq',
        'needNewCode': 0,
    }

    response = requests.get(url, params = params, headers = header).text
    pattern_17 = re.compile('\((.*)\)')
    return_data_json = eval(pattern_17.search(response)[0])
    data = return_data_json["data"]["song"]["list"]
    for n,d in enumerate(data):
        mid = (d['mid'])
        parse_html_page(songname, mid, n+1)

def parse_html_page(songname, mid, n):
    header = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
    data = urllib.parse.quote(mid)

    url = ("https://u.y.qq.com/cgi-bin/musicu.fcg?callback=getplaysongvkey6632596514520588&g_tk=5381&jsonpCallback=getplaysongvkey6632596"
           "514520588&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&data=%7B%22req%22%3A%7B%2"
           "2module%22%3A%22CDN.SrfCdnDispatchServer%22%2C%22method%22%3A%22GetCdnDispatch%22%2C%22param%22%3A%7B%22guid%22%3A%228413346764%22%2C%22c"
           "alltype%22%3A0%2C%22userip%22%3A%22%22%7D%7D%2C%22req_0%22%3A%7B%22module%22%3A%22vkey.GetVkeyServer%22%2C%22method%22%3A%22CgiGetVkey%2"
           "2%2C%22param%22%3A%7B%22guid%22%3A%228413346764%22%2C%22songmid%22%3A%5B%22{0}%22%5D%2C%22songtype%22%3A%5B0%5D%2C%22uin%22%3"
           "A%220%22%2C%22loginflag%22%3A1%2C%22platform%22%3A%2220%22%7D%7D%2C%22comm%22%3A%7B%22uin%22%3A0%2C%22format%22%3A%22json%22%2C%22ct%22%3"
           "A20%2C%22cv%22%3A0%7D%7D").format(data)

    response = requests.get(url, headers = header)
    text = response.text
    data = eval(text[31:])
    vkey_content = data["req_0"]["data"]["midurlinfo"]
    for vkey_detail in vkey_content:
        vkey = vkey_detail['purl']
        filename = songname
        download_music(vkey,songname, n)

def download_music(vkey,songname, n):
    url = "http://110.53.180.17/amobile.music.tc.qq.com/"+vkey
    header = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
    r = requests.get(url, headers = header)
    filename = songname + str(n) +'.m4a'
    with open(filename, 'wb')as f:
        f.write(r.content)
    print("第%s首歌曲下载完成"%n)

if __name__ == '__main__':
    songname = input("请输入歌曲名：")
    get__page_html(songname)

