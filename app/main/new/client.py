import requests
data = {'MemberID' : 4,
		'ProductID' : [23],
		'Price' : [40000],
		'Amount' : [4]}
r = requests.post("http://127.0.0.1:5000/CheckOutPage", data = data)

print(r.text)