#捨てアドレスを大量に取得する

#必要なモジュール
from bs4 import BeautifulSoup
import requests
import re

#正規表現でタグを外す(スクレイピングで余計なものまでついてきてしまってイライラするので)
p = re.compile(r"<[^>]*?>")

#メールアドレスを生成する関数
def createMail():
    payload = {
    'account_member[login]':''
    }
    s = requests.Session()
    r = s.get('http://sute.jp')
    soup = BeautifulSoup(r.text, 'html.parser')
    address = soup.find_all("input",id="account_member_login")[0].get(value)
    payload['account_member[login]'] = address
    s.post('http://sute.jp/signup',data=payload)
    return address



