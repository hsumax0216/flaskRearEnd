from flask import Flask, request, jsonify,render_template
import pymysql

app = Flask(__name__)
app.config["JSON_AS_ASCII"]=False


@app.route("/index", methods = ['GET'])
def homepage(PageState):
    connect = pymysql.connect(host = "140.121.197.131", user = "root"
                          , password = "soselab401", db = "test")
    cursor = connect.cursor()
    hottest=[]
    latest=[]
    
    SQLIns = "SELECT * FROM product ORDER BY TotalEvCount ASC"
    
    try:
   # 执行sql语句
       if(cursor.execute(SQLIns)):
           
 
           
           
           for i in range (0,7):  
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
                       'TotalEvCount':data[14]
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
    SQLIns = "SELECT * FROM product ORDER BY ProductID DESC"
    
    try:
   # 执行sql语句
       if(cursor.execute(SQLIns)):
           for i in range (0,7):  
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
                       'TotalEvCount':data[14]
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

@app.route("/product_Category/<Category>", methods = ['GET'])
def ProductCategory(Category):
    connect = pymysql.connect(host = "140.121.197.131", user = "root"
                          , password = "soselab401", db = "test")
    cursor = connect.cursor()

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
                   'TotalEvCount':data[14]
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

if (__name__ == "__main__") :
    app.run()
    
 
    
    
    