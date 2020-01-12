#!/usr/bin/env python3

import urllib.request as urllib2
import time
import os
import shutil
import json
import sys
import tool

cur_path='/home/'
profile_num=0
config={}
auto_save=0

def get_cur_path():
    global cur_path
    cur_path=sys.argv[0]
    while cur_path[-1]!='/':cur_path=cur_path[0:len(cur_path)-1]
    if not os.path.exists(cur_path+'config/'):
        os.makedirs(cur_path+'config/')

def save_config():
    with open(cur_path+'config.json','w') as f:
        s=json.dumps(config)
        f.write(s)

def update_config():
    global config
    global auto_save
    with open(cur_path+'config.json','r') as f:
        l=f.readlines()
        s=''
        s=s.join(l)
        config=json.loads(s)
        auto_save=config['auto_save']

def show_last_mod_time(pid):
    last_mod_time=config['config'][pid]['last_mod_time']
    localtime=time.localtime(last_mod_time)
    dt=time.strftime('%Y-%m-%d %H:%M:%S',localtime)
    return dt

def download_profile(pid):
    global config
    print('Profile %d last modified: %s'%(pid,show_last_mod_time(pid)))
    config_path=cur_path+'config/%d.yaml'%(pid)
    header = config['custom_header']
    url=config['config'][pid]['url']
    req=urllib2.Request(url,headers=header)
    with urllib2.urlopen(req,timeout=10) as resp:
        res=resp.read().decode('utf-8')
        with open(config_path,'w') as f:
            f.write(res)
        print('Update Profile %d Success!'%pid)
        config['config'][pid]['last_mod_time']=time.time()

def move_profile(pid):
    config_path=cur_path+'config/%d.yaml'%(pid)
    dest_path=config['clash_config_path']+'config.yaml'
    shutil.copyfile(config_path,dest_path)
    print('Move Profile %d Success'%(pid))

def show_profiles():
    print('='*50)
    for i in range(len(config['config'])):
        c=config['config'][i]
        lmt=show_last_mod_time(i)
        name=c['name']
        print('[%d]%s | last modified:%s'%(i,name,lmt))

def add_profile():
    name=input('Please input the profile name: ')
    link=input('Please input the subscribe link: ')
    d={'url':link,'name':name,'last_mod_time':time.time()}
    config['config'].append(d)
    print('Profile %d added!'%(len(config['config'])-1))
    if auto_save:save_config()

def filter_profile(pid,pattern):
    config_path=cur_path+'config/%d.yaml'%(pid)
    with open(config_path,'r') as f:
        f2=open(cur_path+'config/tmp.yaml','w')
        f2.write(tool.filter(f,pattern))
        f2.close()
    shutil.copyfile(cur_path+'config/tmp.yaml',config_path)

def edit_profile(pid):
    print('Choose what to modify?')
    print('[0]name [1]subscribe link [2]nodes')
    c=input('Please input your choice: ')
    if(c=='0'):
        c=input('Please input what is new: ')
        config['config'][pid]['name']=c
    elif c=='1':
         c=input('Please input what is new: ')
         config['config'][pid]['url']=c
    elif c=='2':
        c=input('Please input the pattern:  ')
        filter_profile(pid,c)
    print('Edit profile %d success!'%(pid))
    config['config'][pid]['last_mod_time']=time.time()
    if auto_save:save_config()

def delete_profile(pid):
    now=config['config'][pid]
    print('[%d]%s | last modified:%s'%(pid,now['name'],show_last_mod_time(pid)))
    c=input('Are you sure to delete it? [y/n] ' )
    if c=='y':
        for i in range(pid,len(config['config'])-1):
            shutil.copyfile(cur_path+'config/%d.yaml'%(i+1),cur_path+'config/%d.yaml'%(i))
        config['config'].pop(pid)
        print('Deleted!')
    else:
        print('Cancelled')
    if auto_save:save_config()

def print_info():
    print('='*50)
    print('Please select your operaton:')
    print('[0]Update Profile')
    print('[1]Choose Profile')
    print('[2]Create a new profile')
    print('[3]Edit a profile')
    print('[4]Delete a profile')
    print('[5]Show all the profiles')
    print('[6]Refresh the config')
    print('[7]Save config')
    print('[8]Exit')

def input_and_op(func):
    c=input('Please input your choice: ')
    if(int(c)<len(config['config'])):
        func(int(c))
    else:
        print('Invalid input')

def main():
    get_cur_path()
    update_config()
    while(1):
        print_info()
        c=input('Please input your choice: ')
        if c=='0':
            show_profiles()
            input_and_op(download_profile)
        elif c=='1':
            show_profiles()
            input_and_op(move_profile)
        elif c=='2':
            add_profile()
        elif c=='3':
             show_profiles()
             input_and_op(edit_profile)
        elif c=='4':
            show_profiles()
            input_and_op(delete_profile)
        elif c=='5':
            show_profiles()
        elif c=='6':
            update_config()
        elif c=='7':
            save_config()
        else:
            save_config()
            break

if __name__=="__main__":
    main()
