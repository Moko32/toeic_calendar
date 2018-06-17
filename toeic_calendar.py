# -*- coding: utf-8 -*-
import urllib2
import re
from bs4 import BeautifulSoup
import httplib2
import os
 
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
 
import datetime
 
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar'
# 以下の変数にクライアントのクレデンシャル情報が入ったJSONファイルの名前を書いておく
CLIENT_SECRET_FILE = 'hogehoge.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def toeic_scraip():
    # アクセスするURL
    url = "https://www.iibc-global.org/toeic/test/lr/guide01.html"

    # htmlテキストの読み込み
    html = urllib2.urlopen(url)

    # htmlをBeautifulSoupで扱う
    soup = BeautifulSoup(html, "html.parser")

    # 対象の大枠のタグを読み込む
    div = soup.find_all("div")
    p = soup.find_all("p")

    # 試験の回番号
    toeic_number = []
    # 試験の日時
    toeic_exam_date_y = []
    toeic_exam_date_m = []
    toeic_exam_date_d = []
    # 試験結果の送付日時
    toeic_result_date_y = []
    toeic_result_date_m = []
    toeic_result_date_d = []
    # 試験の申し込み締め切り日時
    toeic_apply_date_y = []
    toeic_apply_date_m = []
    toeic_apply_date_d = []


    # 試験の日時はこちらで処理する
    for tag in p:
        try:
            # class属性から抽出する
            string_ = tag.get("class").pop(0)
            # 所定のパラメータがclass属性として定義されているタグを扱う
            if string_ in "mod-schedule-vertical_main_date":
                # 年，月，日を正規表現で抽出 & それぞれタグを除いて配列に格納
                #年
                year = re.search(r'<p class="">[0-9]*年',str(tag))
                year = year.group(0).replace('<p class="">','').replace('年','')
                toeic_exam_date_y.append(year)
                #月
                month = re.search(r'<em>[0-9]*</em>月',str(tag))
                month = month.group(0).replace('<em>','').replace('</em>月','')
                toeic_exam_date_m.append(month)
                #日
                day = re.search(r'<em>[0-9]*</em>日',str(tag))
                day = day.group(0).replace('<em>','').replace('</em>日','')
                toeic_exam_date_d.append(day)

        except:
            # パス→何も処理を行わない
            pass

    # 試験の回番号と締切はこちらで処理する
    for tag in div:
        try:
            # class属性から抽出する
            string_ = tag.get("class").pop(0)

            # 所定のパラメータがclass属性として定義されているタグを扱う
            if string_ in "mod-schedule-vertical_sub_body":
                # 年，月，日を正規表現で抽出 & それぞれタグを除いて配列に格納
                years = re.findall(r'<p>[0-9]*年',str(tag))
                for year in years:
                    year = year.replace('<p>','').replace('年','')
                    toeic_apply_date_y.append(year)

                months = re.findall(r'<em>[0-9]*</em>月',str(tag))
                for month in months:
                    month = month.replace('<em>','').replace('</em>月','')
                    toeic_apply_date_m.append(month)

                days = re.findall(r'<em>[0-9]*</em>日',str(tag))
                for day in days:
                    day = day.replace('<em>','').replace('</em>日','')
                    toeic_apply_date_d.append(day)

            elif string_ in 'mod-schedule-vertical_head':
                num = re.search(r'<em>.*</em>',str(tag))
                num = num.group(0).replace('<em>','').replace('</em>','')
                toeic_number.append(num)

        except:
            # パス→何も処理を行わない
            pass


    print '回: '+toeic_number[0] + ' 締切年: '+toeic_apply_date_y[2] + ' 締切月: '+toeic_apply_date_m[2]+' 締切日: '+toeic_apply_date_d[2]+' 試験年: '+toeic_exam_date_y[0]+' 試験月: '+toeic_exam_date_m[0]+ ' 試験日: '+ toeic_exam_date_d[0]
    print '回: '+toeic_number[1] + ' 締切年: '+toeic_apply_date_y[5] + ' 締切月: '+toeic_apply_date_m[9]+' 締切日: '+toeic_apply_date_d[9]+' 試験年: '+toeic_exam_date_y[1]+' 試験月: '+toeic_exam_date_m[1]+ ' 試験日: '+ toeic_exam_date_d[1]
    print '回: '+toeic_number[2] + ' 締切年: '+toeic_apply_date_y[8] + ' 締切月: '+toeic_apply_date_m[16]+' 締切日: '+toeic_apply_date_d[16]+' 試験年: '+toeic_exam_date_y[2]+' 試験月: '+toeic_exam_date_m[2]+ ' 試験日: '+ toeic_exam_date_d[2]
    
    #[回番号,締切日,開催日]として格納する
    toeic_1 = [toeic_number[0], toeic_apply_date_y[2] + '-' + toeic_apply_date_m[2] + '-' + toeic_apply_date_d[2] , toeic_exam_date_y[0] + '-' + toeic_exam_date_m[0]+ '-' + toeic_exam_date_d[0]]
    toeic_2 = [toeic_number[1], toeic_apply_date_y[5] + '-' + toeic_apply_date_m[9] + '-' + toeic_apply_date_d[9] , toeic_exam_date_y[1] + '-' + toeic_exam_date_m[1]+ '-' + toeic_exam_date_d[1]]
    toeic_3 = [toeic_number[2], toeic_apply_date_y[8] + '-' + toeic_apply_date_m[16] + '-' + toeic_apply_date_d[16] , toeic_exam_date_y[2] + '-' + toeic_exam_date_m[2]+ '-' + toeic_exam_date_d[2]]

    return [toeic_1,toeic_2,toeic_3]

 
 
def get_credentials():
    """Gets valid user credentials from storage.
 
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
 
    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')
 
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials
 
def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    for t_list in toeic_scraip():
        
        # 締切日の情報
        body = {
            "summary": "【締切日】第"+t_list[0]+"回TOEICテスト",
            "start": {
                "date": t_list[1],
                "timeZone": "Asia/Tokyo",
            },
            "end": {
                "date": t_list[1],
                "timeZone": "Asia/Tokyo",
            }
        }
        
        #Calendar APIを使用して書き込み
        event = service.events().insert(calendarId='primary', body=body).execute()

        # 開催日の情報
        body = {
            "summary": "【開催日】第"+t_list[0]+"回TOEICテスト",
            "start": {
                "date": t_list[2],
                "timeZone": "Asia/Tokyo",
            },
            "end": {
                "date": t_list[2],
                "timeZone": "Asia/Tokyo",
            }
        }

        #Calendar APIを使用して書き込み
        event = service.events().insert(calendarId='primary', body=body).execute()

        


 
if __name__ == '__main__':
    main()