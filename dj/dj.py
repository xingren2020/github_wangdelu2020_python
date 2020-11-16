import requests
import json
import os
import re
#by 红鲤鱼绿鲤鱼与驴 2020.11
cookiesList1 = []
cookiesList2 = []
headers={"User-Agent": "iReaderFast/3.0.0 (iPhone; iOS 12.4; Scale/2.00)"}
dj_cookies1=''
dj_cookies2=''



def dj_usettab(url):
    print('\n首页')
    msg='【我的账户】'
    response = requests.get(url)
    try:
      #print(response.text.encode('ascii').decode('unicode_escape'))
      obj=json.loads(response.text)
      msg+=f'''今日阅读(分钟) {obj['body']['read']['time']}  
      累计阅读(小时) {obj['body']['read']['time']/60} 
      我的财富(金币) {obj['body']['gold']['goldAmount']} 
      墨宝{obj['body']['amount']}'''
    except Exception as e:
        msg+=str(e)
    print(msg)
        
def dj_sign(url):
    print('\n签到')
    msg='【签到】'
    response = requests.get('https://dj.palmestore.com/zycl/gold/index?'+url)
    response = requests.get('https://dj.palmestore.com/zycl/sign/window?'+url)
    try:
      st=response.text.encode('ascii').decode('unicode_escape')
      #print(st)
      msg+='签到'+re.findall(r'签到(.*)金币<',st)[0]+'\n'
      msg+='已连续签到'+re.findall(r'已连续签到<i>(\d+)<\\\/i>',st)[0]+'天'
    except Exception as e:
        msg+=str(e)
    print(msg)

def dj_boxTask(url):
   print('\n宝箱')
   msg='【宝箱】'
   response = requests.get('https://dj.palmestore.com/zycl/gold/receive?'+url+'&type=boxTask&incrId=139')
   try:
      st=response.text.encode('ascii').decode('unicode_escape')
      print(st)
   except Exception as e:
        msg+=str(e)
        print(msg)
def dj_draw(url):
    print('\n抽奖')
    msg='【抽奖获得墨宝】'
    response = requests.get('https://dj.palmestore.com/zyam/app/app.php?'+url+'&activeId=31&drawType=1&pca=Wheel.Index')
    try:
      st=response.text
      print(st)
    except Exception as e:
      msg+=str(e)
      print(msg)
        
def dj_videoTask(url):
    print('\n看广告')
    msg='【广告】'
    response = requests.get('https://dj.palmestore.com/zycl/gold/receive?'+url+'&type=videoTask&videoId=158')
    try:
      st=response.text.encode('ascii').decode('unicode_escape')
      print(st)
    except Exception as e:
        msg+=str(e)
        print(msg)

def dj_mobaosign(url):
    print('\n墨宝签到')
    msg='【墨宝】'
    response = requests.get('https://dj.palmestore.com/zyuc/sign/index?jailbreak=0&'+url+'&source=wantold')
    try:
      st=response.text
      msg+=re.search(r'本周已签到.*天',st).group()
     
    except Exception as e:
        msg+=str(e)
    print(msg)
def dj_mobaoad(url):
    print('\n墨宝任务')
    msg='【墨宝任务看视频10次】'
    response = requests.get('https://dj.palmestore.com/zyuc/sign/drawgift?'+url+'&taskId=53&ext%5Bid%5D=53&ext%5Bamount%5D=15&ext%5BisPop%5D=0')
    try:
      msg+=json.loads(response.text)['msg']
    except Exception as e:
        msg+=str(e)
    print(msg)
    
    
def dj_mobaoav(url):
    print('\n看视频赚墨宝')
    msg='【看视频赚墨宝20次】'
    response = requests.get('https://dj.palmestore.com/zyuc/sign/getmb?'+url+'&vid=127&addNum=20')
    try:
      msg+=json.loads(response.text)['msg']
    except Exception as e:
        msg+=str(e)
    print(msg)
        
def check(st,ck,ls):
   if st in os.environ:
      ck = os.environ[st]
      for line in ck.split('\n'):
        if not line:
          continue 
        ls.append(line)
   elif ck:
       for line in ck.split('\n'):
         if not line:
            continue 
         ls.append(line.strip())
   else:
      print('没有基础数据退出')
      exit()

def main():
   check('DJ_COOKIES1',dj_cookies1,cookiesList1)
   check('DJ_COOKIES2',dj_cookies2,cookiesList2)
   for j in range(1):
      dj_usettab(cookiesList1[j])
      dj_sign(cookiesList2[j])
      dj_boxTask(cookiesList2[j])
      dj_videoTask(cookiesList2[j])
      dj_mobaosign(cookiesList2[j])
      dj_mobaoad(cookiesList2[j])
      dj_mobaoav(cookiesList2[j])
      #dj_draw(cookiesList2[j])
if __name__ == '__main__':
    main()
