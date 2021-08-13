import requests, re, time, os
from bs4 import BeautifulSoup
from toolBox import eokwon, dict_to_file
from krx_data import jonmok_history

### dics 가져오기  #####
dics = {}
with open('data/list_crawled.csv','r') as f:
    temp = f.readlines()
header =temp[0].replace('\n','').split(',')
corp_cd_in = header.index('corp_cd')
for i in temp[1:]:
    line = i.replace('\n','').split(',')
    dics[line[corp_cd_in]] = {}
    for ii in range(len(line)):
        dics[line[corp_cd_in]][header[ii]] = line[ii]

dics_list = [* dics]#[::-1]

new_dics = {}
if os.path.exists('data/after_jangwega.csv') :
    with open('data/after_jangwega.csv','r') as f:
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


url = 'http://www.38.co.kr/html/fund/index.htm?o=nw&page='  # 전체 리스트화면 url
url2 = 'http://www.38.co.kr/chart/chart_page_new.php3?code='  # 개별 장외종가 url
login_url = 'https://www.38.co.kr/member/login/login_process.php'  # 로그인url
session_requests = requests.session()
header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
              '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Length': '147',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': '__utmb=105967361.9.10.1616586757',
    'Host': 'www.38.co.kr',
    'Origin': 'http://www.38.co.kr',
    'Referer': 'http://www.38.co.kr/',
    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
}
payload = {
    'reurl': '%2Fhtml%2Ffund%2Findex.htm%3Fo%3Dnw',
    'time': '1616588438',
    'dauto': '8eb4c13d81e667badd6c2c626336ce64',
    'x': '34',
    'y': '12',
    'id': 'suhcrates',
    'passwd': 'seoseoseo7'
}
temp = session_requests.post(
    login_url,
    data=payload,
    headers=header
)


delete_list = []

n=1
for corp_cd in dics_list:
    temp = session_requests.get(url2 + corp_cd)
    temp = BeautifulSoup(temp.content.decode('euc_kr','replace'), 'html.parser')#, from_encoding='euc-kr')
    table = temp.find_all('table')
    tds = table[0].find_all('tr')[1].find_all('td')

    # 장외종가
    jangwe_jonga = table[1].find_all('tr')[1].find('td').text.replace('\xa0', '')  # 장외종가
    jangwe_jonga = eokwon(jangwe_jonga)
    if jangwe_jonga in ['', '0', '-', 0]:
        print(f'{dics[corp_cd]["name"]} 없음')
        delete_list.append(corp_cd)
    else:
        # print(f'{corp_cd}here2')
        dics[corp_cd]['jangwe_jonga'] = jangwe_jonga

        # 자본
        jabon = tds[0].text  # 자본금
        dics[corp_cd]['jabon'] = eokwon(jabon)

        jusicsu = tds[1].text.replace(',', '')  # 주식수
        dics[corp_cd]['jusicsu'] = jusicsu.replace(',', '')
        akmyen = tds[2].text  # 액면가
        dics[corp_cd]['akmyen'] = eokwon(akmyen)

        # 시가총액
        sigachong = eokwon(tds[3].text) #시가총액
        dics[corp_cd]['sigachong'] = sigachong
        # 공모가, 주식수 기준 시가총액
        # print(dics[i])
        dics[corp_cd]['sigachong_gyesan'] = int(dics[corp_cd]['gongmo_p']) * int(jusicsu)
        print(dics[corp_cd])
        new_dics[corp_cd] = dics[corp_cd]
        dict_to_file(new_dics, 'after_jangwega')

    print(f"지금까지 총 {n} / {len([*dics_list])}")
    n+=1
    time.sleep(7)


# print(delete_list)
# for iii in delete_list:
#     del dics[iii]


