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

#メールアドレスを取得する関数
def getMail(address):
    s = requests.Session()
    payload = {
    'user_session[login]':address
    }
    r = s.post('http://sute.jp/signin',data=payload)
    soup = BeautifulSoup(r.text,'html.parser')
    mails = soup.find_all("li",{"class":"messeage"})
    maillist = []
    
    for mail in mails:
        m = []
        r = s.get("http://sute.jp/mails/"+mail.get("data-id"))
        soup = BeautifulSoup(r.text,'html.parser')
        title = soup.fild_all("h2")[0].text
        hons = soup.find_all("p",{'class':''})
        hon = ""

        for data in hons:
            hon = hon + "\n" + p.sub("",str(data))
        m.append(title)
        m.append(hon[1:])
        maillist.append(m)
    return maillist

# メールアドレス作成
address = createMail()
print("メールアドレスは「" + address + "@sute.jp」です。")

# メール取得
mails = getMail(address)
print("---------以下のメールを受信---------")
for mail in mails:
    print("-----------------")
    print(mail[0]) #タイトル
    print(mail[1]) #本文
    print("-----------------")

