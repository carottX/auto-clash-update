#!/usr/bin/env python3

import yaml
import re
import copy

def filter(f,pattern):
    y=yaml.load(f)
    res=copy.deepcopy(y)
    res['Proxy']=[]
    res['Proxy Group']=[]
    p=re.compile(pattern)
    cnt1=cnt2=0
    for node in y['Proxy']:
        r=re.search(p,node['name'])
        if r:
            res['Proxy'].append(node)
            cnt2+=1
        else:
            cnt1+=1
    gn=['Rule','Global','DIRECT']
    for node in y['Proxy Group']:
        tmp=copy.deepcopy(node)
        gn.append(tmp['name'])
        tmp['proxies']=[]
        for e in node['proxies']:
            r=re.search(p,e)
            if r or (e in gn):
                tmp['proxies'].append(e)
        res['Proxy Group'].append(tmp)
    f3.close()
    s=yaml.dump(res,allow_unicode=True)
    return s