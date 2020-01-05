#!/usr/bin/env python3

import urllib.request as urllib2
import time
import os
import shutil
import json
import sys

cur_path='/home/'
profile_num=0
config={}
auto_save=0

def get_cur_path():
    global cur_path
    cur_path=sys.argv[0]
    while cur_path[-1]!='/':cur_path=cur_path[0:len(cur_path)-1]
    if not os.path.exists(cur_path+'/config/'):
        os.makedirs(cur_path+'/config/')

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
        try:
            config=json.loads(s)
            auto_save=config['auto_save']
        except:
            print('Config file broken!')

def show_last_mod_time(config_id):
    last_mod_time=config['config'][config_id]['last_mod_time']
    localtime=time.localtime(last_mod_time)
    dt=time.strftime('%Y-%m-%d %H:%M:%S',localtime)
    return dt

def download_profile(pid):
    global config
    print('Profile %d last modified: %s'%(pid,show_last_mod_time(pid)))
    config_path=cur_path+'/config/%d.yaml'%(pid)
    header = config['custom_header']
    url=config['config'][pid]['url']
    req=urllib2.Request(url,headers=header)
    resp=urllib2.urlopen(req,timeout=10)
    res=resp.read().decode('utf-8')
    with open(config_path,'w') as f:
        f.write(res)
    print('Update Profile %d Success!'%pid)
    config['config'][pid]['last_mod_time']=time.time()

def move_profile(pid):
    config_path=cur_path+'/config/%d.yaml'%(pid)
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

def edit_profile(pid):
    print('Choose what to modify?')
    print('[0]name [1]subscribe link')
    c=input('Please input your choice: ')
    if(c=='0'):
        c=input('Please input what is new: ')
        config['config'][pid]['name']=c
    else:
         c=input('Please input what is new: ')
         config['config'][pid]['url']=c
    print('Edit profile %d success!'%(pid))
    config['config'][pid]['last_mod_time']=time.time()
    if auto_save:save_config()

def delete_profile(pid):
    now=config['config'][pid]
    print('[%d]%s | last modified:%s'%(pid,now['name'],show_last_mod_time(pid)))
    c=input('Are you sure to delete it? [y/n] ' )
    if c=='y':
        config['config'].pop(pid)
        print('Deleted!')
    else:
        print('Cancelled')
    if auto_save:save_config()

def main():
    get_cur_path()
    print(cur_path)
    update_config()
    while(1):
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
        c=input('Please input your choice: ')
        if c=='0':
            show_profiles()
            c=input('Please input your choice: ')
            try:
                if(int(c)<len(config['config'])):
                    download_profile(int(c))
                else:
                    print('Invalid input')
            except:
                print('Invalid input')
        elif c=='1':
            show_profiles()
            c=input('Please input your choice: ')
            try:
                if(int(c)<len(config['config'])):
                    move_profile(int(c))
                else:
                    print('Invalid input')
            except:
                print('Invalid input')
        elif c=='2':
            add_profile()
        elif c=='3':
             show_profiles()
             c=input('Please input your choice: ')
             try:
                if int(c)<len(config['config']):
                    edit_profile(int(c))
                else:
                    print('Invalid input')
             except:
                print('Invalid input')
        elif c=='4':
            show_profiles()
            c=input('Please input your choice: ')
            try:
                if int(c)<len(config['config']):
                    delete_profile(int(c))
                else:
                    print('Invalid input')
            except:
                print('Invalid input')
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
