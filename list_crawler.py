#http://www.38.co.kr/html/fund/index.htm?o=nw&page=1   리스트만 쭉 뽑음

import requests, re, time
from bs4 import BeautifulSoup
from toolBox import eokwon, dict_to_file
from krx_data import jonmok_history


def list_crawler():

    url = 'http://www.38.co.kr/html/fund/index.htm?o=nw&page=' #전체 리스트화면 url
    url2 = 'http://www.38.co.kr/chart/chart_page_new.php3?code=' #개별 장외종가 url
    login_url = 'https://www.38.co.kr/member/login/login_process.php' #로그인url

    ##로그인 ####
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
        'passwd':'seoseoseo7'
    }
    temp = session_requests.post(
        login_url,
        data = payload,
        headers=header
    )




    ##### 38커뮤 리스트뽑기 ####
    dics = {}
    for n in range(1,31):
        url_0 = url + str(n)
        temp = session_requests.get(url_0)
        temp = BeautifulSoup(temp.content, 'html.parser')
        temp = temp.find('table', {'summary':'신규상장종목'})

        trs = temp.find_all('tr')
        print(f'페이지 {n}')
        dics_page = {}
        for i in trs:
            dic={}
            td_list = []
            tds = i.find_all('td')
            for ii in tds:
                td_list.append(ii.text.replace('\xa0',''))

            try:
                #이름구간
                name = td_list[0]
                type = ''#시장
                if bool(re.search('\(유가\)',name)): #코스피
                    type = 'kospi'
                    name.replace('(유가)','')
                else:
                    type = 'kosdaq'
                dic['name'] = name  #회사이름
                dic['type'] = type  #시장종류
                dic['day'] = td_list[1].replace('/','')  #상장일
                dic['now_p'] = td_list[2].replace(',','') #현재가
                dic['gongmo_p'] = td_list[4].replace(',','') #공모가
                dic['sicho_p'] = td_list[6].replace(',','') #시초가
                dic['first_p'] = td_list[8].replace(',','') #첫날 종가
                if dic['sicho_p'] in ['-']:
                    raise Exception('데이터 없음')

                corp_cd = re.search("(?<=\=)\d*$",tds[-1].find('a')['href'])[0]
                dic['corp_cd'] =corp_cd  # 종목코드
                dics_page[corp_cd] = dic
                dics = {**dics, **dics_page}
            except:
                pass
        time.sleep(5)
    dict_to_file(dics, 'list_crawled')

if __name__ == '__main__':
    list_crawler()