# 종목시세 이어붙임

import requests, re, time, os
from bs4 import BeautifulSoup
from toolBox import eokwon, dict_to_file
from krx_data import jonmok_history

### dics 가져오기  #####
dics = {}

with open('data/after_jangwega.csv','r') as f:
    temp = f.readlines()
header =temp[0].replace('\n','').split(',')
corp_cd_in = header.index('corp_cd')
for i in temp[1:]:
    line = i.replace('\n','').split(',')
    dics[line[corp_cd_in]] = {}
    for ii in range(len(line)):
        dics[line[corp_cd_in]][header[ii]] = line[ii]

dics_list = [* dics]
new_dics={}
if os.path.exists('data/after_krx.csv') :
    with open('data/after_krx.csv','r') as f:
        temp = f.readlines()
    header =temp[0].replace('\n','').split(',')
    corp_cd_in = header.index('corp_cd')
    for i in temp[1:]:
        line = i.replace('\n','').split(',')
        new_dics[line[corp_cd_in]] = {}
        for ii in range(len(line)):
            new_dics[line[corp_cd_in]][header[ii]] = line[ii]
    last_one = [*new_dics][-1]
    dics_list = dics_list[dics_list.index(last_one) + 1:]
else:
    pass


for i in dics_list:
    temp = dics[i]
    kos_cd = temp['type']
    d_first, d_last, d_len = jonmok_history(corp_cd=i, strtDd=temp['day'])
    if d_len in ['0', 0]:
        print(f"{i}  없음")
    else:
        dics[i]['d_first'] = d_first
        dics[i]['d_last'] = d_last
        dics[i]['d_len'] = d_len
        new_dics[i] = dics[i]
        print(dics[i])
        print(f"{len([* new_dics])}/{len([* dics])}")
        dict_to_file(new_dics, 'after_krx')
# 결과물 출력
