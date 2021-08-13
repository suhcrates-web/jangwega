import re
import requests, json, time
from datetime import date, timedelta
from bs4 import BeautifulSoup
import os, glob, json

#'억원'을 일반 수로 환산. 쉼표 떼줌
def eokwon(x):
    x = x.replace('원', '').replace(',','')
    if bool(re.search('억',x)):
        x = x.replace('억','')
        x = int(x) * 100000000
    return str(x)

#krx에서  스톡코드 (123123) 넣으면 풀코드(kr1244593945959)로 환산. 이게 있어야 krx에서 종목별 검색이 됨.
def fullcode_finder(corp_cd=''):
    # if kos == 'kospi':
    #     kos_code = 'STK'
    # elif kos == 'kosdaq':
    #     kos_code = 'KSQ'
    url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'

    header = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7',
        'Connection': 'keep-alive',
        'Content-Length': '315',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': '__smVisitorID=mgX3gboq6Sf; __utmz=139639017.1612159881.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); finder_stkisu_finderCd=finder_stkisu; finder_stkisu_param1=ALL; finder_stkisu_typeNo=0; JSESSIONID=K9rSGrpfJ1s7Hw4LCKMDumbkzaITTI2I08tBy9q5v8zIUswQJM4i1zICE9FYfepM.bWRjX2RvbWFpbi9tZGNvd2FwMS1tZGNhcHAwMQ==; finder_stkisu_codeVal2=KR7334970001; __utma=139639017.1458902062.1612159881.1615958375.1616638506.6; __utmc=139639017; __utmt=1; __utmb=139639017.1.10.1616638506; finder_stkisu_tbox=282330%2FBGF%EB%A6%AC%ED%85%8C%EC%9D%BC; finder_stkisu_codeNm=BGF%EB%A6%AC%ED%85%8C%EC%9D%BC; finder_stkisu_codeVal=KR7282330000',
        'Host': 'data.krx.co.kr',
        'Origin': 'http://data.krx.co.kr',
        'Referer': 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.90 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    data = {
        'mktsel': 'ALL', # 코스닥은 KSQ,  코스피는 STK 인듯.
        'typeNo': '0',
        'searchText':corp_cd,
        'bld': """dbms/comm/finder/finder_stkisu"""
    }
    # print(data)
    temp = requests.post(url, data=data, headers = header)
    temp = json.loads(temp.content.decode('utf-8'))
    # print(temp)
    time.sleep(3)
    return temp['block1'][0]['full_code']

#딕셔너리를 csv파일로
def dict_to_file(dic, filename ):
    with open(f'data/{filename}.csv', 'w') as f:
        list = []
        for i in [*dic[[*dic][0]]]:
            list.append(str(i))
            list.append(',')
        list[-1] = '\n'
        # print(list)
        f.writelines(list)

        for i in [*dic]:
            list = []
            for ii in [*dic[i]]:
                list.append(str(dic[i][ii]))
                list.append(',')
            list[-1] = '\n'
            # print(list)
            f.writelines(list)



#딕셔너리 순서정렬
def dict_sort(dict0, key0='key0'):
    dict0 = {k:v for k, v in sorted(dict0.items(), reverse=True, key=lambda item: item[1][key0])}
    return dict0


# print(fullcode_finder(kos='kosdaq',corp_cd='361390'))



#코스피200 의 이름과 넘버, 코스닥 150의 이름과 넘버를 뱉음. 목록은 한달마다 업데이트.
#결과값은 dict 이며 키값은'kospi_name' 'kospi_num' 'kosdaq_name' 'kosdaq_num'. 'all_name' 'all_num' 각각 리스트로 불려옴.
def kos_list():
    tomonth = date.today().strftime('%Y%m')
    today = date.today().strftime('%Y%m%d')
    w1_ago =  (date.today() - timedelta(days=7)).strftime('%Y%m%d')
    url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
    result_dict = {}
    result_dict['all_name'] = []
    result_dict['all_num'] = []
    #이 펑션이 두번 반복됨. 파일 검색, 없으면 만들고 있으면 가져와 result_dict를 채움.

    glob_temp_nums = [] # maek_and_get 세번 반복하는 과정에서 중복 등록 방지 위함.
    def make_and_get(kowhat):

        if kowhat in ['byeondong_wanhwa']:
            filename = kowhat+str(today)+'.csv'
        else:
            filename = kowhat+str(tomonth)+'.csv'
        if not os.path.isfile(f'data_share/{kowhat}/'+ filename):
            with open(f'data_share/{kowhat}/'+ filename,'w') as f:
                if kowhat == 'kospi':
                    q_data = {
                        'bld': 'dbms/MDC/STAT/standard/MDCSTAT00601',
                        'tboxindIdx_finder_equidx0_0': '코스피 200',
                        'indIdx': '1',
                        'indIdx2': '028',
                        'codeNmindIdx_finder_equidx0_0': '코스피 200',
                        'param1indIdx_finder_equidx0_0': '',
                        'trdDd': str(today),
                        'money': '3',
                        'csvxls_isNo': 'false'
                    }
                elif kowhat== 'kosdaq':
                    q_data = {
                        'bld': 'dbms/MDC/STAT/standard/MDCSTAT00601',
                        'tboxindIdx_finder_equidx0_0': '코스닥 150',
                        'indIdx': '2',
                        'indIdx2': '203',
                        'codeNmindIdx_finder_equidx0_0': '코스닥 150',
                        'param1indIdx_finder_equidx0_0': '',
                        'trdDd': str(today),
                        'money': '3',
                        'csvxls_isNo': 'false'
                    }
                elif kowhat== 'byeondong_wanhwa': #변동성완화장치 발동종목 현황
                    q_data = {
                        'bld': 'dbms/MDC/STAT/issue/MDCSTAT22401',
                        'mktId': 'ALL',
                        'inqTpCd1': '01',
                        'viKindCd': 'ALL',
                        'tboxisuCd_finder_stkisu1_2': '전체',
                        'isuCd': 'ALL',
                        'isuCd2': 'ALL',
                        'codeNmisuCd_finder_stkisu1_2':'',
                        'param1isuCd_finder_stkisu1_2': 'ALL',
                        'strtDd': str(w1_ago),
                        'endDd': str(today),
                        'csvxls_isNo': 'true'
                    }
                result = requests.post(url, q_data)
                dicts = json.loads(result.content.decode(encoding='utf-8'))
                dicts = dicts['output']
                if kowhat in ['byeondong_wanhwa' ]: #변동성완화대상일 경우. 7일치를 비교하므로 중복이 많아
                    temp_nums = []
                    for i in dicts:
                        temp_num = i['ISU_NM']
                        if not temp_num in temp_nums:  #중복된거 걸러주는 장치
                            temp_nums.append(temp_num)
                            try:
                                f.writelines([i['ISU_NM'],',',i['ISU_CD'], '\n'])
                            except:
                                pass
                        else:
                            pass
                else:
                    for i in dicts:
                        try:
                            f.writelines([i['ISU_ABBRV'],',',i['ISU_SRT_CD'], '\n'])
                        except:
                            pass
                time.sleep(3)  # sleep은 해당 파일이 없어서 새로 만들때만 적용됨.
        try:
            with open(f'data_share/{kowhat}/'+ filename) as f:
                name_list= []
                num_list = []
                result = f.readlines()
                for i in result:
                    i = i.split(',')
                    temp_num = i[1]
                    if not temp_num in glob_temp_nums:
                        glob_temp_nums.append(temp_num)
                        name_list.append(i[0])
                        num_list.append(i[1].strip())
                        result_dict['all_name'].append(i[0])
                        result_dict['all_num'].append(i[1].strip())
                    else:
                        pass

        except:
            list = glob.glob(f'data_share/{kowhat}/*')
            latest = max(list, key= os.path.getctime)
            with open(latest) as f:
                name_list= []
                num_list = []
                result = f.readlines()
                for i in result:
                    i = i.split(',')
                    temp_num = i[1]
                    if not temp_num in glob_temp_nums:
                        glob_temp_nums.append(temp_num)
                        name_list.append(i[0])
                        num_list.append(i[1].strip())
                        result_dict['all_name'].append(i[0])
                        result_dict['all_num'].append(i[1].strip())
                    else:
                        pass

        result_dict[f'{kowhat}_name'] = name_list
        result_dict[f'{kowhat}_num'] = num_list
        return None

    make_and_get('kospi')
    make_and_get('kosdaq')
    make_and_get('byeondong_wanhwa')
    return result_dict