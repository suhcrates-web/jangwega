import requests, re, time, os, math
from bs4 import BeautifulSoup
from toolBox import eokwon, dict_to_file
from krx_data import jonmok_history
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.font_manager as fm
font_path = r'C:\stamp\naver_font\NanumBarunpenB.ttf'
fontprop = fm.FontProperties(fname = font_path, size=9)
fontprop2 = fm.FontProperties(fname = font_path, size=15)

### dics 가져오기  #####
dics = {}
what = "last"
with open('data/after_krx.csv','r') as f:
    temp = f.readlines()
header =temp[0].replace('\n','').split(',')
corp_cd_in = header.index('corp_cd')
for i in temp[1:]:
    line = i.replace('\n','').split(',')
    dics[line[corp_cd_in]] = {}
    for ii in range(len(line)):
        dics[line[corp_cd_in]][header[ii]] = line[ii]



dics_by_time = {}
for i in dics:
    if int(dics[i]['d_len']) >=15 and dics[i]['day'] >'20160101':
        time0 = datetime.strptime(dics[i]['day'], '%Y%m%d') #일자 인식
        time0 = datetime.strftime(time0, '%Y') # %Y-%m 으로 바꾸면 월별 자료가 됨
        if time0 not in [* dics_by_time]:
            dics_by_time[time0] = {}
            dics_by_time[time0]['gongmo_r'] =[]  #공모가
            dics_by_time[time0]['sicho_r'] =[]  #시초가
            dics_by_time[time0]['first_r'] =[] #첫날 종가
            dics_by_time[time0]['last_r'] =[]   #막날 종가
            dics_by_time[time0]['day'] =[]   #날짜
            dics_by_time[time0]['len'] = 0

        jg = int(dics[i]['jangwe_jonga']) #장외종가
        gongmo_p = int(dics[i]['gongmo_p'])
        sicho_p = int(dics[i]['sicho_p'])
        d_first = int(dics[i]['d_first'])
        d_last = int(dics[i]['d_last'])
        day = datetime.strptime(dics[i]['day'], '%Y%m%d')

        dics_by_time[time0]['gongmo_r'].append( (gongmo_p - jg) / jg )
        dics_by_time[time0]['sicho_r'].append( (sicho_p - jg) / jg )
        dics_by_time[time0]['first_r'].append( (d_first - jg) / jg )
        dics_by_time[time0]['last_r'].append( (d_last - jg) / jg )
        dics_by_time[time0]['day'].append(day)

fig = plt.figure()
ax = fig.add_subplot(111)
plt.xticks([], '')
plt.yticks([], '') #
ax.spines['bottom'].set_color('white')
ax.spines['top'].set_color('white')
ax.spines['left'].set_color('white')
ax.spines['right'].set_color('white')

#막대용#
x_result = []
y_result = []
##


dics_by_time = {k:v for k, v in sorted(dics_by_time.items(), reverse=False, key=lambda item: item[0])}
dics_result = {}
n=0
for i in dics_by_time:
    temp_list = dics_by_time[i][f'{what}_r']
    day_list = dics_by_time[i]['day']
    result = sum(temp_list) / len(temp_list)
    dics_result[i] = result
    print(f"{i} :  {round(result, 4)}  / {len(temp_list)}")

    tot_num = len([*dics_result])
    tot_num = math.ceil(tot_num / 4)

    n += 1
    ax = fig.add_subplot(tot_num, 4, n)
    plt.plot(day_list, temp_list, 'o', color='navy', markersize=1)
    plt.xticks([], '')  # 눈금과 라벨링을 없앰
    plt.yticks([], '')
    ra = ax.get_data_ratio()
    ax.set_aspect(aspect=1 / ra)

    x_result.append(i)
    y_result.append(result)

# x_result = x_result[::-1]
# y_result = y_result[::-1]

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
plt.bar(x_result, y_result, color= 'skyblue')
for i, v in enumerate(y_result): # i 에는 그냥 숫자 0~n 가 나옴. v에는 y밸류가 나옴
    ax.text( i-0.3, v+0.05 if v > 0 else v - 0.07 , str(round(v,3)), color="blue", fontsize=7, rotation=30)
# ax.set_xticks(x_result[::12])
plt.xticks(rotation = 45)
plt.title(f"장외시장 종가 대비 상장 한달뒤 수익률", fontproperties = fontprop2)
ax.set_ylim(min(y_result)-0.2, max(y_result)+0.2)   #y축 상한 하한선
# ax.set_aspect('equal',adjustable='box')
plt.show()

