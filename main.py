#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Copyright:    Wu_Zh
Filename:     a.py
Description:

@author:      wuzhipeng
@email:       763008300@qq.com
@website:     https://wuzhipeng.cn/
@create on:   11/28/2021 9:36 PM
@software:    PyCharm
"""


import requests
import re
import os
import getpass
import datetime

print('Please enter the username and password of https://asf.alaska.edu/')
username = input('username:')
password = getpass.getpass("password (will not be displayed):")
dataFolder = input('Data folder (containing *.zip):')
saveFolder = input('EOF to save:')

auxUrl = 'https://s1qc.asf.alaska.edu/aux_poeorb/'
if not os.path.exists(saveFolder):
    os.makedirs(saveFolder)


for idx in range(5):
    ret = requests.get(auxUrl,headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36'}).text
    # names = re.findall('S1.*?.EOF', ret)
    # with open('html.txt','r') as f:
    #     ret = f.read()

    names = []
    for file in os.listdir(dataFolder):
        if not file.endswith('.zip'):
            continue
        t = file.split('T',1)[0][-8:]
        t = datetime.datetime.strptime(t,'%Y%m%d')
        t1 = datetime.datetime.strftime(t-datetime.timedelta(days=1),'%Y%m%d')
        t2 = datetime.datetime.strftime(t+datetime.timedelta(days=1),'%Y%m%d')
        title = file[0:3]

        name = re.findall(f'{title}.*?V{t1}.*?{t2}.*?.EOF', ret)[-1]
        names.append(name)


    print(f'{len(names)} files to download')

    existedTmp = os.listdir(saveFolder)
    existed = [i for i in existedTmp if os.path.getsize(os.path.join(saveFolder,i))>4000141]

    toDown = [i for i in names if i not in existed]
    toDown = [auxUrl+i for i in toDown]
    tmpFile = os.path.join(saveFolder,'toDownload.txt')
    with open(tmpFile,'w') as f:
        f.write('\n'.join(toDown))

    exe_path = r'aria2c.exe'
    command = f'{exe_path} -i {tmpFile} -d {saveFolder} --http-passwd={password} --http-user={username}'
    os.system(command)

    existedTmp = os.listdir(saveFolder)
    existed = [i for i in existedTmp if os.path.getsize(os.path.join(saveFolder,i))>4000141]

    toDown = [i for i in names if i not in existed]
    toDown = [auxUrl+i for i in toDown]
    with open(tmpFile,'w') as f:
        f.write('\n'.join(toDown))

    print(f'{len(toDown)} files failed!')
    
    if(len(toDown)<1):
        break
