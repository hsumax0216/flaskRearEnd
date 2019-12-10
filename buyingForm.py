from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from hellow import app,db,member,product,trade,Appointboard#,Bidding
import datetime
import pymysql
#app,db一定要import
#app = Flask(__name__)
#app.debug = True
#app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:admin@127.0.0.1:3306/test"
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
#db = SQLAlchemy(app)
@app.route("/CheckOutPage", methods = ['GET','POST'])#checkOutPage為暫定url
def CheckOutPage():#dict={'key':'value'}#list=[value]#value=every type
	if(request.method == 'POST'):
		member_id = request.form['member_id']
		Productform = request.form.getlist('product')
		Amountform = request.form.getlist('Amount')
		Priceform = request.form.getlist('price')
		boughtItem = dict(zip(Productform,Amountform))						#商品與數量字典
		itemPrice = dict(zip(Productform,Priceform))						#商品與總價字典
		buyer = member.query.filter_by(ID = member_id).first()				#買家sql
		t={'status':1}														#回傳JSON字典
		errorProduct = []													#發生商品錯誤list
		errorSeller = []													#發生賣家錯誤list
		if(buyer is None):
			t['status']=0
			t['inform']='buyer memberID: '+str(member_id)+' didn\'t exist.'
			return jsonify(t)
		for i in boughtItem:
			'''需增加:
			#購買後扣除原來商品的數量(update)
			#買家無法買自己的東西(雖然應該在"直接購買"或"加入購物車"時就應該阻止)
			#無法買數量為0的東西(同上)
			#only buy the items that amount*unit price == current price
			#XXX區別(不用區分，因為還有直購競標並存的狀況)競標商品與普通商品(還是結標時自動
			#	將競標商品在資料庫自動做結帳動作?no,被動式結帳)
			#biddingPrice is init bidding price
			記得提醒學姊gnxxx在競標中的狀態列須新增"得標"進行購買鍵，進行競標物品的購買流程
			'''
			prID = i														#商品ID
			Product = product.query.filter_by(ProductID = prID).first()		#商品sql
			amount = int(boughtItem[i])										#購買數量
			Cprice = int(itemPrice[i])										#購買總價
			#
			#商品總數 >= 購買商品數量#購買總數 > 0
			if(Product is not None \
				and (Product.Amount) >= (amount) \
				and (amount) > 0):
				#Uprice = Product.Price			
				#if((Product.BiddingPrice is not None and  Cprice >= Product.BiddingPrice)or \
				#	(Product.BiddingPrice is None and Cprice == (amount*Uprice))):
				productAmount = Product.Amount								#商品總數
				productAmount -= (amount)									#減去購買商品數
				seller = member.query.filter_by(ID = Product.SellerID).first()#賣家sql
				if(seller is not None and seller.ID is not buyer.ID):		#賣家不能同時是買家
					#UPDATE商品總數
					Product.Amount = "{}".format(productAmount)
					#宣告新的交易
					Trade = trade(
							SellerID = seller.ID,\
							BuyerID = buyer.ID,\
							ProductID = Product.ProductID,\
							TradeAmount = amount,\
							TradePrice = Cprice,\
							CompletedType = False
							)
					print("before TRY")
					try:
						db.session.add(Trade)
						#print(type([Trade,Product]))#type list
						#提交DB
						db.session.commit()					
						db.session.refresh(Trade,['TradeID'])#
						tradeidtemp = Trade.TradeID
						print('Trade.TradeID:'+str(tradeidtemp))	
						Appboard = Appointboard(
							TradeID = tradeidtemp,\
							BoughtDate = datetime.datetime.now()#.strftime("%Y-%m-%d %H:%M:%S")
							)					
						db.session.add(Appboard)
						db.session.commit()	
					except Exception as e:
						print(e)
						t['status'] = 0
						t['inform'] = 'DB was rollback.'
						db.session.rollback()
				else:
					t['status'] = 0
					errorSeller.append(int(Product.SellerID))
					t['inform_seller'] = "SellerID:  "+str(Product.SellerID)+\
						"  is error.(by same person or exist)"
				#else:
				#	t['status'] = 0
				#	errorProduct.append(int(prID))
			else:
				t['status'] = 0
				errorProduct.append(int(prID))
		
		if(len(errorProduct) != 0):
			t['ProductID'] = errorProduct
			err = "ProductID: "
			for cou in  errorProduct:
				err+=(" "+str(cou))
			err+="  is error.(by amount or exist)"
			t['inform_product'] = err
		if(len(errorSeller) != 0):
			t['SellerID'] = errorSeller
		return jsonify(t)
	if(request.method == 'GET'):
		return 'CheckOutPage.html...'
'''
client:
import requests
data = {'member_id' : 2,
		'product' : [23],
		'price' : [40000],
		'Amount' : [4]}
r = requests.post("http://127.0.0.1:5000/CheckOutPage", data = data)

print(r.text)
'''
'''
{"status":1}

{"ProductID":[23],"inform_product":"ProductID:  23  is error.(by amount or exist)","status":0}

{"ProductID":[24,2,27,29],"SellerID":[1],"inform_product":"ProductID:  24 2 27 29  is error.
(by amount or exist)","inform_seller":"SellerID:  1  is error.(by same person or exist)","status":0}
'''