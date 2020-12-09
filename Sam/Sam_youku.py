import requests
import os
import re
import json
import random
import time
osenviron={}

urllist=[]
hdlist=[]
bdlist=[]

def Av(i,hd,j,k):
    print('=🔔='*k)
    try:
      
       response = requests.post(i,headers=eval(hd),data=j)
       Res=response.json()
       #print(Res)
       if(k==1):
           print(Res['msg'])
       elif(k==2):
         print(Res['msg'])
         for item in Res['data']['task_list']:
           if(json.dumps(item).find('get_coin')>0):
             
             if(item['status']==2):
               Av(urllist[2],hdlist[0],bdlist[2],3)
       elif(k==3):
          print(Res['msg'])
       elif(k==4):
       	     print(Res['data']['score'])
    except Exception as e:
      print(str(e))


def watch(flag,list):
   vip=''
   if flag in osenviron:
      vip = osenviron[flag]
   if flag in os.environ:
      vip = os.environ[flag]
   if vip:
       for line in vip.split('\n'):
         if not line:
            continue 
         list.append(line.strip())
       return list
   else:
       print(f'''【{flag}】 is empty,DTask is over.''')
       exit()
       




def start():
   global bdlist,urllist,hdlist
   time.sleep(random.randint(1,5))
   watch('sam_url',urllist)
   watch('sam_headers',hdlist)
   for j in range(10):
       print('====count===='+str(j))
       bdlist=[]
       watch('sam_body'+str(j),bdlist)
       if(len(bdlist)==0):
            break
       for k in range(len(urllist)):
          if(k==2):
             continue
          Av(urllist[k],hdlist[0],bdlist[k],(k+1))
       time.sleep(random.randint(1,3))
   print('🔔'*15)
   
   

if __name__ == '__main__':
       start()
    
