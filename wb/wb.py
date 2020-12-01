import requests
import json
import os
import urllib
cookiesList = []

headers={"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Weibo (iPhone11,8__weibo__10.10.2__iphone__os12.4)"}
result=''
weibo_sign_cookie=''
djj_bark_cookie=''
djj_sever_jiang=''

def pushmsg(title,txt,bflag=1,wflag=1):
   txt=urllib.parse.quote(txt)
   title=urllib.parse.quote(title)
   if bflag==1 and djj_bark_cookie.strip():
      print("\n【通知汇总】")
      purl = f'''https://api.day.app/{djj_bark_cookie}/{title}/{txt}'''
      response = requests.post(purl)
      #print(response.text)
   if wflag==1 and djj_sever_jiang.strip():
      print("\n【微信消息】")
      purl = f'''http://sc.ftqq.com/{djj_sever_jiang}.send'''
      headers={
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'
    }
      body=f'''text={txt})&desp={title}'''
      response = requests.post(purl,headers=headers,data=body)
    #print(response.text)
def weibo_user(url):
   print('\nuser')
   msg='【user】'
   try:
      curl=f'''https://api.weibo.cn/2/users/show?'''+url[url.find('gsid'):len(url)]
      response = requests.get(curl)
      obj=json.loads(response.text)
      #print(response.text)
      if(json.dumps(obj).find('name')>0):
          msg+=obj['name']
      else:
       	  msg+='errmsg'
   except Exception as e:
      msg+=str(e)
      #print(msg)
   loger(msg+'\n')
   
   
def weibo_sign(url):
   print('\n签到')
   msg='【签到】'
   try:
    response = requests.post(url)
    obj=json.loads(response.text)
   # print(obj)
    if(json.dumps(obj).find('10000')>0):
          msg+=obj['msg']
    else:
       	  msg+=obj['errmsg']
   except Exception as e:
      msg+=str(e)
      #print(msg)
   loger(msg+'\n')

 

    
def loger(m):
   print(m)
   global result
   result +=m
   
   
def check():
   global weibo_sign_cookie
   global djj_bark_cookie
   global djj_sever_jiang
   if "WEIBO_SIGN_COOKIE" in os.environ:
      weibo_sign_cookie = os.environ["WEIBO_SIGN_COOKIE"]
   if "DJJ_BARK_COOKIE" in os.environ:
     djj_bark_cookie = os.environ["DJJ_BARK_COOKIE"]
   if "DJJ_SEVER_JIANG" in os.environ:
      djj_sever_jiang = os.environ["DJJ_SEVER_JIANG"]
      for line in weibo_sign_cookie.split('\n'):
        if not line:
          continue 
        cookiesList.append(line)
   elif weibo_sign_cookie:
       for line in weibo_sign_cookie.split('\n'):
         if not line:
            continue 
         cookiesList.append(line.strip())
   else:
    	print('没有基础数据退出')
    	exit()

def main():
   check()
   for count in cookiesList:
      weibo_user(count)
      weibo_sign(count)

   pushmsg('weibo',result)
   print('its over')
if __name__ == '__main__':
    main()
