import requests, json, time
from bs4 import BeautifulSoup
from toolBox import fullcode_finder
from datetime import datetime, timedelta, date

#kos_cd : kospi / kosdaq
#corp_cd : 기업번호
#strDd : 상장일  20210303  형식
def jonmok_history(corp_cd='', strtDd=''):
    time.sleep(3)
    url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'

    header = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7',
        'Connection': 'keep-alive',
        'Content-Length': '315',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': '__smVisitorID=mgX3gboq6Sf; __utmz=139639017.1612159881.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=('
                  'none); __utma=139639017.1458902062.1612159881.1614737745.1615958375.5; ',
        # 'finder_stkisu_finderCd=finder_stkisu; finder_stkisu_param1=STK; finder_stkisu_typeNo=0; JSESSIONID=K9rSGrpfJ1s7Hw4LCKMDumbkzaITTI2I08tBy9q5v8zIUswQJM4i1zICE9FYfepM.bWRjX2RvbWFpbi9tZGNvd2FwMS1tZGNhcHAwMQ==; finder_stkisu_codeVal2=KR7334970001; finder_stkisu_tbox=138930%2FBNK%EA%B8%88%EC%9C%B5%EC%A7%80%EC%A3%BC; finder_stkisu_codeNm=BNK%EA%B8%88%EC%9C%B5%EC%A7%80%EC%A3%BC',#; finder_stkisu_codeVal=KR7138930003',
        'Host': 'data.krx.co.kr',
        'Origin': 'http://data.krx.co.kr',
        'Referer': 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.90 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    # corp_cd = '361390'
    # kos_cd = 'kosdaq'
    temp_date = datetime.strptime(strtDd, '%Y%m%d')
    endDd = datetime.strftime(temp_date + timedelta(days=30), '%Y%m%d')
    # print(strtDd)
    # print(endDd)

    data = {
        'bld': 'dbms/MDC/STAT/standard/MDCSTAT01701',
        # 'tboxisuCd_finder_stkisu0_0': '138930/BNK금융지주',
        'isuCd': fullcode_finder(corp_cd), ##이게 무조건 있어야됨.
        # 'isuCd2': corp_cd,
        # 'codeNmisuCd_finder_stkisu0_0': 'BNK금융지주',
        # 'param1isuCd_finder_stkisu0_0': 'STK',
        'strtDd': strtDd,
        'endDd': endDd,
        'share': '1',
        'money': '1',
        'csvxls_isNo': 'false'
    }
    temp = requests.post(url, data=data, headers = header)
    temp = json.loads(temp.content.decode('utf-8'))['output']
    d_len = len(temp)
    if d_len < 5:
        d_len = 0
    d_first = temp[-1]['TDD_CLSPRC'].replace(',','') #상장첫날
    d_last = temp[0]['TDD_CLSPRC'].replace(',', '')
    return d_first, d_last, d_len




# print(jonmok_history('kosdaq', '334970', '20210317'))



#종목 시계열 크롤링식.
#krx에서 종목별  월 첫날 끝날, 증가율 추출식.
def jonmok_for_seongjang(kos_cd = 'kospi', corp_cd='', strtDd='', endDd=''):
    url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'

    header = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7',
        'Connection': 'keep-alive',
        'Content-Length': '315',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': '__smVisitorID=mgX3gboq6Sf; __utmz=139639017.1612159881.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=('
                  'none); __utma=139639017.1458902062.1612159881.1614737745.1615958375.5; ',
        # 'finder_stkisu_finderCd=finder_stkisu; finder_stkisu_param1=STK; finder_stkisu_typeNo=0; JSESSIONID=K9rSGrpfJ1s7Hw4LCKMDumbkzaITTI2I08tBy9q5v8zIUswQJM4i1zICE9FYfepM.bWRjX2RvbWFpbi9tZGNvd2FwMS1tZGNhcHAwMQ==; finder_stkisu_codeVal2=KR7334970001; finder_stkisu_tbox=138930%2FBNK%EA%B8%88%EC%9C%B5%EC%A7%80%EC%A3%BC; finder_stkisu_codeNm=BNK%EA%B8%88%EC%9C%B5%EC%A7%80%EC%A3%BC',#; finder_stkisu_codeVal=KR7138930003',
        'Host': 'data.krx.co.kr',
        'Origin': 'http://data.krx.co.kr',
        'Referer': 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.90 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    # corp_cd = '361390'
    # kos_cd = 'kosdaq'
    # temp_date = datetime.strptime(strtDd, '%Y%m%d')
    # endDd = datetime.strftime(temp_date + timedelta(days=30), '%Y%m%d')
    # print(strtDd)
    # print(endDd)

    data = {
        'bld': 'dbms/MDC/STAT/standard/MDCSTAT01701',
        # 'tboxisuCd_finder_stkisu0_0': '138930/BNK금융지주',
        'isuCd': fullcode_finder(kos_cd,corp_cd), ##이게 무조건 있어야됨.
        # 'isuCd2': corp_cd,
        # 'codeNmisuCd_finder_stkisu0_0': 'BNK금융지주',
        # 'param1isuCd_finder_stkisu0_0': 'STK',
        'strtDd': strtDd,
        'endDd': endDd,
        'share': '1',
        'money': '1',
        'csvxls_isNo': 'false'
    }
    temp = requests.post(url, data=data, headers = header)
    temp = json.loads(temp.content.decode('utf-8'))['output']
    time.sleep(3)
    if len(temp) < 5:
        return "0"
    else:
        d_1 = temp[-1]['TDD_CLSPRC'].replace(',','') #월 첫날
        d_30 = temp[0]['TDD_CLSPRC'].replace(',','')  #월 마지막날
        d_1 = int(d_1)
        d_30 = int(d_30)
        rate = (d_30 - d_1)/d_1
        return [d_1,d_30,rate]



#주식수 알아냄
def jusiksu(kos = 'kospi', corp_cd='', strtDd='', endDd=''):
    if kos == 'kospi':
        kos_code = 'STK'
    elif kos == 'kosdaq':
        kos_code = 'KSQ'
    url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'

    header = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7',
        'Connection': 'keep-alive',
        'Content-Length': '315',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': '__smVisitorID=mgX3gboq6Sf; __utmz=139639017.1612159881.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=('
                  'none); __utma=139639017.1458902062.1612159881.1614737745.1615958375.5; ',
        # 'finder_stkisu_finderCd=finder_stkisu; finder_stkisu_param1=STK; finder_stkisu_typeNo=0; JSESSIONID=K9rSGrpfJ1s7Hw4LCKMDumbkzaITTI2I08tBy9q5v8zIUswQJM4i1zICE9FYfepM.bWRjX2RvbWFpbi9tZGNvd2FwMS1tZGNhcHAwMQ==; finder_stkisu_codeVal2=KR7334970001; finder_stkisu_tbox=138930%2FBNK%EA%B8%88%EC%9C%B5%EC%A7%80%EC%A3%BC; finder_stkisu_codeNm=BNK%EA%B8%88%EC%9C%B5%EC%A7%80%EC%A3%BC',#; finder_stkisu_codeVal=KR7138930003',
        'Host': 'data.krx.co.kr',
        'Origin': 'http://data.krx.co.kr',
        'Referer': 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDCSTAT02103',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.90 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    # corp_cd = '361390'
    # kos_cd = 'kosdaq'
    # temp_date = datetime.strptime(strtDd, '%Y%m%d')
    # endDd = datetime.strftime(temp_date + timedelta(days=30), '%Y%m%d')
    # print(strtDd)
    # print(endDd)
    # print(corp_cd)
    data = {
        'bld': 'dbms/MDC/STAT/standard/MDCSTAT02103',
        # 'tboxisuCd_finder_stkisu0_0': '000660/SK하이닉스',
        'isuCd': fullcode_finder(kos = kos, corp_cd=corp_cd),
        # 'isuCd2': '000660',
        # 'codeNmisuCd_finder_stkisu0_0': 'SK하이닉스',
        'param1isuCd_finder_stkisu0_0': kos_code,
        'csvxls_isNo': 'false'
    }
    # print(data)
    temp = requests.post(url, data=data, headers = header)
    temp = json.loads(temp.content.decode('utf-8'))
    # print(temp)
    tot_jusic = temp['LIST_SHRS'].replace(',','') #총 주식수
    time.sleep(3)
    return tot_jusic


### 결과물 : d_l, d_f , rate /  끝날, 첫날 가격, 증가율
def jonmok_for_jusiksu(kos_cd = 'kospi', corp_cd='', strtDd='', endDd=''):
    url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'

    header = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7',
        'Connection': 'keep-alive',
        'Content-Length': '315',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': '__smVisitorID=mgX3gboq6Sf; __utmz=139639017.1612159881.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=('
                  'none); __utma=139639017.1458902062.1612159881.1614737745.1615958375.5; ',
        # 'finder_stkisu_finderCd=finder_stkisu; finder_stkisu_param1=STK; finder_stkisu_typeNo=0; JSESSIONID=K9rSGrpfJ1s7Hw4LCKMDumbkzaITTI2I08tBy9q5v8zIUswQJM4i1zICE9FYfepM.bWRjX2RvbWFpbi9tZGNvd2FwMS1tZGNhcHAwMQ==; finder_stkisu_codeVal2=KR7334970001; finder_stkisu_tbox=138930%2FBNK%EA%B8%88%EC%9C%B5%EC%A7%80%EC%A3%BC; finder_stkisu_codeNm=BNK%EA%B8%88%EC%9C%B5%EC%A7%80%EC%A3%BC',#; finder_stkisu_codeVal=KR7138930003',
        'Host': 'data.krx.co.kr',
        'Origin': 'http://data.krx.co.kr',
        'Referer': 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.90 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    # corp_cd = '361390'
    # kos_cd = 'kosdaq'
    # temp_date = datetime.strptime(strtDd, '%Y%m%d')
    # endDd = datetime.strftime(temp_date + timedelta(days=30), '%Y%m%d')
    # print(strtDd)
    # print(endDd)

    data = {
        'bld': 'dbms/MDC/STAT/standard/MDCSTAT01701',
        # 'tboxisuCd_finder_stkisu0_0': '138930/BNK금융지주',
        'isuCd': fullcode_finder(kos_cd,corp_cd), ##이게 무조건 있어야됨.
        # 'isuCd2': corp_cd,
        # 'codeNmisuCd_finder_stkisu0_0': 'BNK금융지주',
        # 'param1isuCd_finder_stkisu0_0': 'STK',
        'strtDd': strtDd,
        'endDd': endDd,
        'share': '1',
        'money': '1',
        'csvxls_isNo': 'false'
    }
    temp = requests.post(url, data=data, headers = header)
    temp = json.loads(temp.content.decode('utf-8'))['output']
    time.sleep(3)
    d_f = int(temp[-1]['TDD_CLSPRC'].replace(',','')) #기간 첫날
    d_l = int(temp[0]['TDD_CLSPRC'].replace(',',''))  #기간 마지막날
    rate = (d_l - d_f)/d_f
    return [d_l,d_f,rate]


####코스닥, 코스피 기준일 전종목 시가총액, 업종, 종가 뽑음.
#결과 dics : (키는 corp_cd)  corp_cd, corp_nm, upjong, sichong, jongga, date0
def sichong_crawl(kos = 'kosdaq', date0 = ''): #20210414 형식
    if kos == 'kospi':
        kos_code = 'STK'
    elif kos == 'kosdaq':
        kos_code = 'KSQ'
    url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'

    header = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7',
        'Connection': 'keep-alive',
        'Content-Length': '315',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': '__smVisitorID=mgX3gboq6Sf; __utmz=139639017.1612159881.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=('
                  'none); __utma=139639017.1458902062.1612159881.1614737745.1615958375.5; ',
        # 'finder_stkisu_finderCd=finder_stkisu; finder_stkisu_param1=STK; finder_stkisu_typeNo=0; JSESSIONID=K9rSGrpfJ1s7Hw4LCKMDumbkzaITTI2I08tBy9q5v8zIUswQJM4i1zICE9FYfepM.bWRjX2RvbWFpbi9tZGNvd2FwMS1tZGNhcHAwMQ==; finder_stkisu_codeVal2=KR7334970001; finder_stkisu_tbox=138930%2FBNK%EA%B8%88%EC%9C%B5%EC%A7%80%EC%A3%BC; finder_stkisu_codeNm=BNK%EA%B8%88%EC%9C%B5%EC%A7%80%EC%A3%BC',#; finder_stkisu_codeVal=KR7138930003',
        'Host': 'data.krx.co.kr',
        'Origin': 'http://data.krx.co.kr',
        'Referer': 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.90 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    # corp_cd = '361390'
    # kos_cd = 'kosdaq'
    # temp_date = datetime.strptime(strtDd, '%Y%m%d')
    # endDd = datetime.strftime(temp_date + timedelta(days=60), '%Y%m%d')
    # print(strtDd)
    # print(endDd)

    data = {
        'bld': 'dbms/MDC/STAT/standard/MDCSTAT03901',
        'mktId': kos_code,
        'trdDd': date0,
        'money': '1',
        'csvxls_isNo': 'false'
    }
    temp = requests.post(url, data=data, headers = header)
    temp = json.loads(temp.content.decode('utf-8'))['block1'] #리스트임
    # print(temp)
    dics = {}
    for i in temp:
        corp_cd = i['ISU_SRT_CD']

        dics[corp_cd] ={}
        dics[corp_cd]['corp_cd'] =corp_cd
        dics[corp_cd]['corp_nm'] =i['ISU_ABBRV'] #회사이름
        dics[corp_cd]['upjong'] =i['IDX_IND_NM'].replace(',','') #업종
        dics[corp_cd]['sichong'] =int(i['MKTCAP'].replace(',','')) #시총
        dics[corp_cd]['jongga'] =int(i['TDD_CLSPRC'].replace(',','')) #기준일 종가
        dics[corp_cd]['date0'] = date0  #기준일
    return dics


if __name__ == '__main__':
    print(jusiksu(corp_cd='005930'))