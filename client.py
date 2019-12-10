import requests
data = {'member_id' : 2,
		'product' : [23],
		'price' : [40000],
		'Amount' : [4]}
r = requests.post("http://127.0.0.1:5000/CheckOutPage", data = data)

print(r.text)