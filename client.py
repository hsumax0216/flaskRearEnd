import requests

user_info = {'ID' : '0001',
             'phone' : '0979576113',
             'name': '魏宏勝',
             'nickname': 'konoha',
             'e-mail': 'koka19871988@gmail.com',
             'account': '00657002',
             'password': '1234',
             'imageURL' : 'https://i.imgur.com/mPPFjO5.jpg'}
r = requests.post("http://127.0.0.1:5000/signUp", data = user_info)

print(r.text)