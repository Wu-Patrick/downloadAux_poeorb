#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Copyright:    Wu_Zh
Filename:     main.py
Description:

@author:      wuzhipeng
@email:       763008300@qq.com
@website:     https://wuzhipeng.cn/
@create on:   11/28/2021 9:36 PM
@software:    PyCharm
"""

import re
import os
import getpass
import datetime

try:
    import requests
except:
    os.system('pip install requests')
    import requests
    
text = '''==================================================================
Download precise orbit data of Sentinel-1 satellite

This script can help you download the orbit file of S1 data from 
https://s1qc.asf.alaska.edu/aux_poeorb/.

@author:      wuzhipeng
@email:       763008300@qq.com
@website:     https://wuzhipeng.cn/
@version:     2022.04.29.1
==================================================================
'''
print(text)

print('Please enter the username and password of https://asf.alaska.edu/')
username = input('username:')
password = getpass.getpass("password (will not be displayed):")

dataFolder = input('Data folder (containing *.zip or *.SAFE):')
while not os.path.isdir(dataFolder):
    print(f'Path does not exist: "{dataFolder}", please re-enter.')
    dataFolder = input('Data folder (containing *.zip or *.SAFE):')

saveFolder = input('Download folder path:')
while not saveFolder:
    saveFolder = input('Please re-enter download folder path:')
os.makedirs(saveFolder,exist_ok=True)

print('Processing, please wait...')
auxUrl = 'https://s1qc.asf.alaska.edu/aux_poeorb/'

for idx in range(5):


    names = []
    for file in os.listdir(dataFolder):
        if not (file.endswith('.zip') or file.endswith('.SAFE')):
            continue
        t = file.split('T',1)[0][-8:]
        t = datetime.datetime.strptime(t,'%Y%m%d')
        t1 = datetime.datetime.strftime(t-datetime.timedelta(days=1),'%Y%m%d')
        t2 = datetime.datetime.strftime(t+datetime.timedelta(days=1),'%Y%m%d')
        title = file[0:3]

        try:
            ret
        except:
            ret = requests.get(auxUrl, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36'}).text

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
        os.remove(tmpFile)
        break

input('Press any key to exit...')