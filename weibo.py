import json

import requests
import re
import time

# 这里是你要签到的超话的id，每个超话的不一样，多个的话请用英文逗号隔开，例如‘[AA’,‘BB’].获取方式：进入到超话界面，地址栏中的地址的p/和/super_index之间的这一串
ids = ['100808b0c63fc9170be777c03a2c6611774638','100808cb8f14090af3caeebba04103cc7f8ce9','100808a68f5614d6305a17228a0f7b04d54036']
# 这里是选择Server酱的推送方式，填写Sendkey，不想使用的话直接忽略
SCKEY = ''
# 推送PLUS的token
Token = '2330572e45b34328a60988310b5aa345'
# 这里填写你的COOKIE
cookie = 'tgc=TGT-NjQ2MDIwMTI2OA==-1689299995-yf-D2A7BFD0AE95F7CFBE3A23DB06708A4A-1; SUB=_2A25JtNxLDeRhGeBK7VIT8C_OzTSIHXVqwEqDrDV_PUNbm9ANLVnEkW9NR7Fy9B6dh-3lBWTYZf7ept6NWG7dKOni; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF7D5V3mc2c-c-xnO3W5HHQ5JpX5KzhUgL.FoqXSo5Eeh2ESon2dJLoIEBLxK.L1K.L1hnLxKqL1KMLBKMLxKqL1-eLB-BLxKnLB--LBo5t; ALC=ac%3D27%26bt%3D1689299995%26cv%3D6.0%26et%3D1691891995%26ic%3D2071795668%26login_time%3D1689299995%26scf%3D%26uid%3D6460201268%26vf%3D0%26vs%3D1%26vt%3D0%26es%3D999d582501d5f046c86600345a2c9031; ALF=1691891995; LT=1689299995;'
# 推送函数
def push(content):
    if SCKEY != '':
        url = "https://sctapi.ftqq.com/{}.send?title={}&desp={}".format(SCKEY, '微博超话签到', content)
        requests.post(url)
        print('推送完成')
    elif Token != '':
        headers = {'Content-Type': 'application/json'}
        json = {"token": Token, 'title': '微博超话签到', 'content': content, "template": "json"}
        resp = requests.post(f'http://www.pushplus.plus/send', json=json, headers=headers).json()
        print('push+推送成功' if resp['code'] == 200 else 'push+推送失败')
    else:
        print('未使用消息推送推送！')

url = 'https://weibo.com/p/aj/general/button?ajwvr=6'


content = ''
num = 0
header = {
    'cookie': cookie,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}
for person_id in ids:
    info_url = 'https://weibo.com/p/{}/super_index'.format(person_id)
    data = {
    'api': 'http://i.huati.weibo.com/aj/super/checkin',
    'texta': '%E5%B7%B2%E7%AD%BE%E5%88%B0',
    'textb': '%E5%B7%B2%E7%AD%BE%E5%88%B0',
    'status': '1',
    'id': person_id,
    'location': 'page_100808_super_index',
    'timezone': 'GMT+0800',
    'lang': 'zh-cn',
    'plat': 'Win32',
    'ua': 'Mozilla/5.0%20(Windows%20NT%2010.0;%20Win64;%20x64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/109.0.0.0%20Safari/537.36',
    'screen': '1536*864',
    '__rnd': '1674614466131'}
    try:
        # 获取超话社区名字
        html_info =requests.get(url=info_url, headers=header).text
        info = "".join(re.findall('<title>(.*?)</title>', html_info, re.S))
        info = info.replace('—新浪微博超话社区', '')
        #进行签到
        response = requests.get(url=url, headers=header, params=data).text
        result = json.loads(response)
        content =content+info+'   '+result['msg']+'\n\n'
        num += 1
        if num ==len(ids):
          push(content)
    except:
        content = '签到失败，可能是cookie失效,请及时更新cookie'
        push(content)
