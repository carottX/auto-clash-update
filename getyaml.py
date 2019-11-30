#!/usr/bin/env python3

import urllib.request as urllib2
import time
import config as cf

#print(cf.config)

last_mod_time=0
config_path=cf.config['path']

if config_path[-1]=='/':
    config_path=config_path[0:len(cf.config['path'])-1]
try:
    with open(config_path+'/.last_mod_time') as f3:
        last_mod_time=float(f3.readline())

except:
    print('An error occured!')

localtime=time.localtime(last_mod_time)
dt=time.strftime('%Y-%m-%d %H:%M:%S',localtime)
print('Last modified:',dt)

header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
        'accept':'ext/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-language':'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
        }

url=cf.config['url']
req=urllib2.Request(url,headers=header)
#print('req ok')
resp=urllib2.urlopen(req,timeout=10)
try:
    res=resp.read().decode('utf-8')
    with open(config_path+'/config.yaml','w') as f:
        f.write(res)
    with open(config_path+'/.last_mod_time','w') as f2:
        f2.write(str(time.time()))
    print('Success!')
except:
    print('An Error Occured!')
