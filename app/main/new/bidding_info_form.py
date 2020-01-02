from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from ... import db
from .. import main
from ...models import member, product,Bidding
import datetime
from datetime import timedelta
import pymysql
@main.route("/biddingDownPage", methods = ['GET','POST'])
def biddingDownPage():#dict={'key':'value'}#list=[value]#value=every type
	if(request.method == 'POST'):
		nowtime = datetime.datetime.now()
		tenMinDatetime = strTotimedelta("00:10:00","%H:%M:%S")
		#print(tenMinDatetime)
		#print(type(tenMinDatetime))
		mbID  = request.form['MemberID']
		prID = request.form['ProductID']
		amount = int(request.form['Amount'])
		price = int(request.form['Price'])
		buyer = member.query.filter_by(ID = mbID).first()
		#state = 1 表示 無錯誤
		t={'state':True}
		if(buyer is None):
			t['state']=False
			print('buyer memberID: '+str(mbID)+' didn\'t exist.')
			return jsonify(t)
		Product = product.query.filter_by(ProductID = prID).first()
		if(Product is not None \
			and (Product.Amount) >= (amount) \
			and (amount) > 0 \
			and (Product.BiddingUnitPrice is not None)):
			bid = Bidding.query.filter_by(ProductID = prID,BiddingUserID = mbID).first()
			if(Product.BiddingPrice < price):
			#product.BiddingPrice is current highist price
				#print((Product.BiddingDeadline - tenMinDatetime))
				#print(type(Product.BiddingDeadline - tenMinDatetime))
				#print(nowtime)
				#print(type(nowtime))
				if(((Product.BiddingDeadline - tenMinDatetime) < nowtime \
					and Product.BiddingDeadline > nowtime \
					and bid is not None) \
					or (Product.BiddingDeadline - tenMinDatetime) > nowtime):
					#ready for bidding
					Product.BiddingPrice = price
					Product.BiddingTopUserID = buyer.ID
					if(bid is None):
						bid = Bidding(
								ProductID = Product.ProductID,
								BiddingUserID = buyer.ID
								)						
					try:
						db.session.add(bid)
						#提交DB
						db.session.commit()
					except Exception as e:
						print(e)
						#state = 0表示 出現錯誤
						t['state'] = False
						print('DB was rollback.')
						db.session.rollback()
				else:
				#in 10 mins and didnt bid before
					t['state'] = False
					print('didnt bid before')
			else:
			#price is lower than last bidding consumer
				t['state'] = False
				print('price is lower than last bidding consumer')
		else:
			t['state'] = False
			print('product \'if\' layer is fail')
		#回傳JSON字典
		if(Product.BiddingDeadline > nowtime):
			t['biddingtime'] = 2
			print('in time')
		elif(Product.BiddingDeadline < nowtime):
			t['biddingtime'] = 0
			print('out of the bidding time')
		elif((Product.BiddingDeadline - tenMinDatetime) < nowtime):
			t['biddingtime'] = 1
			print('in 10 mins')	
		return jsonify(t)
	if(request.method == 'GET'):
		return 'biddingDownPage...'

@main.route("/biddingInfo", methods = ['GET','POST'])
def BiddingInfo():
	if(request.method == 'POST'):
		nowtime = datetime.datetime.now()
		mbID  = request.form['MemberID']
		buyer = member.query.filter_by(ID = mbID).first()
		#state = 1 表示 無錯誤
		t={'state':True}
		if(buyer is None):
			t['state']=False
			print('buyer memberID: '+str(mbID)+' didn\'t exist.')
			return jsonify(t)
		bid = Bidding.query.filter_by(BiddingUserID = mbID).all()
		try:
			ans = []
			for bd in bid:
				PD = product.query.filter_by(ProductID = bd.ProductID).first()
				temp = {					
				# state 表示 是否成功
				#IsGEthanLowestPrice #is greater or equal than LowestPrice
				'state' : True ,\
				'OverBidTime' : (PD.BiddingDeadline < nowtime),\
				'IsTheBiddingTopUserID' : (PD.BiddingTopUserID == int(mbID)),\
				'IsGEthanLowestPrice' : (PD.BiddingPrice >= PD.LowestPrice),\
				'ProductID' : PD.ProductID,\
				'SellerID' : PD.SellerID,\
				'ProductName' : PD.ProductName,\
				'ImageURL' : PD.ImageURL,\
				'Amount' : PD.Amount,\
				'Price' : PD.Price,\
				'LowestPrice' : PD.LowestPrice,\
				'BiddingPrice' : PD.BiddingPrice,\
				'BiddingUnitPrice' : PD.BiddingUnitPrice,\
				'BiddingDeadline' : PD.BiddingDeadline,\
				'BiddingTopUserID' : PD.BiddingTopUserID,\
				'Information' : PD.Information,\
				'Category' : PD.Category,\
				'AvgEv' : PD.AvgEv,\
				'TotalEvCount' : PD.TotalEvCount,\
				'SurfedTimes' : PD.SurfedTimes
				}
				ans.append(temp)
			return jsonify(ans)
		except Exception as e:
			print(e)
			#state = 0表示 出現錯誤
			t['state'] = False
			print('PD was error.')
		print('no data')
		return jsonify(t)
	if(request.method == 'GET'):
		return 'biddingInfoPage...'

def strTotimedelta(datestr, format):
	t = datetime.datetime.strptime(datestr, format)
	delta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
	return delta