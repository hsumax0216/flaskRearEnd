from flask import Flask, request, jsonify,render_template
import pymysql
import sys
from .. import main
from config import Config

@main.route("/product_searching", methods = ['GET'])
def Product_searching_Info():
    connect = pymysql.connect(host = Config.DB_HOST, user = Config.DB_USER
                          , password = Config.DB_PW, db = Config.DB_DB)
    cursor = connect.cursor()
	
    productName =request.args.get('Name')
    lowerPrice =request.args.get('FirstPrice')
    higherPrice =request.args.get('LastPrice')
    productEv =request.args.get('AvgEv')
    
    if(not productName):
        productName='無'
    if(not lowerPrice):
        lowerPrice=0
    if(not higherPrice):
        higherPrice=sys.maxsize
    if(not productEv):
        productEv=0		
    #print(productName,lowerPrice,higherPrice,productEv)
    SQLIns = "SELECT * FROM product WHERE ProductName  \
		LIKE '%{0}%' AND AvgEv >={1} AND  (Price BETWEEN {2} \
		AND {3} OR BiddingPrice BETWEEN {4} AND {5}) "\
    .format(productName,productEv,lowerPrice,higherPrice,lowerPrice,higherPrice)

    try:
       # 执行sql语句
       if(cursor.execute(SQLIns)):
           data = cursor.fetchone()
           
           ans=[]
           
           while data is not None:    
             #  print(data)
             #  print()
               t = {
                   'state' : True ,
                   'ProductID' : data[0],              # state 表示 是否成功 
                   'SellerID' : data[1],
                   'ProductName' : data[2],
                   'ImageURL' : data[3],
                   'Amount' : data[4],
                   'Price' : data[5],
                   'LowestPrice' : data[6],
                   'BiddingPrice' : data[7],
                   'BiddingUnitPrice' : data[8],
                   'BiddingDeadline' : data[9],
                   'BiddingTopUserID' : data[10],
                   'Information' : data[11],
                   'Category' : data[12],
                   'AvgEv':data[13],
                   'TotalEvCount':data[14],
                   'SurfedTimes':data[15]
                   }
               ans.append(t)
               data = cursor.fetchone()
           return jsonify(ans)
       else:
           t = {
               'state' : False              # state 表示 是否成功 
               }
           return jsonify(t)
    except Exception as e:
	   # 如果发生错误则回滚
       print(e)
       connect.rollback()     
    connect.close()
    return 'product_searching...'