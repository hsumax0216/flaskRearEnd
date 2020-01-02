from flask import Flask, request, jsonify,render_template
import pymysql
from .. import main
from config import Config

@main.route("/index", methods = ['GET'])
def homepage():
    connect = pymysql.connect(host = Config.DB_HOST, user = Config.DB_USER
                          , password = Config.DB_PW, db = Config.DB_DB)
    cursor = connect.cursor()
    hottest=[]
    latest=[]
    
    SQLIns = "SELECT * FROM product ORDER BY SurfedTimes DESC"              #熱門商品，舉出8樣，游瀏覽次數高到低排序
    
    try:
   # 执行sql语句
       if(cursor.execute(SQLIns)):
           
 
           
           
           for i in range (0,7):                                            #不到8樣會輸出僅有項目
               data = cursor.fetchone()
               if(data is not None):
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
                   hottest.append(t)
                   
       else:
           t = {
               'state' : False              # state 表示 是否成功 
               }
           return jsonify(t)
    except Exception as e:
    	   # 如果发生错误则回滚
           print(e)
           connect.rollback()     
    SQLIns = "SELECT * FROM product ORDER BY ProductID DESC"                         #最新商品，由商品ID大排到小
    
    try:
   # 执行sql语句
       if(cursor.execute(SQLIns)):
           for i in range (0,7):                                                       #不到8樣會輸出僅有項目  
               data = cursor.fetchone()
               if(data is not None):
                   print(data)
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
                   latest.append(t)
       else:
           t = {
               'state' : False              # state 表示 是否成功 
               }
           return jsonify(t)
    except Exception as e:
    	   # 如果发生错误则回滚
           print(e)
           connect.rollback() 
    return jsonify(hottest,latest)
    connect.close()

@main.route("/product_Category", methods = ['GET'])
def ProductCategory():
    connect = pymysql.connect(host = Config.DB_HOST, user = Config.DB_USER
                          , password = Config.DB_PW, db = Config.DB_DB)
    cursor = connect.cursor()
    Category =request.args.get('Category')
    if(not Category):
        t = {
               'state' : False              # state 表示 是否成功 
            }
        return jsonify(t)
    
    SQLIns = "SELECT * FROM product WHERE Category = '{0}'".format(Category)
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
