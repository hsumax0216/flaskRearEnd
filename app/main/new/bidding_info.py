from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from ... import db
from .. import main
from ...models import member, product,Bidding
import datetime
import pymysql

@main.route("/bidding_info", methods = ['GET','POST'])
def Bidding_Info():
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
				PD = product.query.filter_by(ProductID = bd.ProductID)
				temp = {					
				# state 表示 是否成功
				'state' : True ,\
				'OverBidTime' : (PD.BiddingDeadline < nowtime),\
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
				'TotalEvCount' : PD.TotalEvCount
				}
				ans.append(temp)
			return jsonify(ans)
		except Exception as e:
			print(e)
			#state = 0表示 出現錯誤
			t['state'] = False
			print('PD was error.')
		
		
	if(request.method == 'GET'):
		return 'biddingInfoPage...'