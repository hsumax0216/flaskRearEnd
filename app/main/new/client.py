import requests
r = requests.get("http://127.0.0.1:5000/product_information?ProductID=27")

print(r.text)
'''
data = {'MemberID' : 21}
r = requests.post("http://127.0.0.1:5000/biddingInfo", data = data)

print(r.text)
'''
'''
data = {'MemberID' : 21,
		'ProductID' : 56,
		'Price' : 1510,
		'Amount' : 1}
r = requests.post("http://127.0.0.1:5000/biddingDownPage", data = data)

print(r.text)
'''
'''
data = {'MemberID' : 4,
		'ProductID' : [23],
		'Price' : [40000],
		'Amount' : [4]}
r = requests.post("http://127.0.0.1:5000/CheckOutPage", data = data)
'''
'''
import datetime
from datetime import timedelta
def strTodatetime(datestr, format):
	t = datetime.datetime.strptime(datestr, format)
	delta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
	return delta


tenMinDatetime = strTodatetime("00:10:00","%H:%M:%S")
print(tenMinDatetime)
print(type(tenMinDatetime))
nowtime = datetime.datetime.now()
print(nowtime)
print(type(nowtime))
temp = nowtime - tenMinDatetime
print(temp)
print(type(temp))
'''
