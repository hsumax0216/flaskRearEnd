from flask import Flask, request, jsonify, render_template
import pymysql
import datetime

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False


@app.route("/", methods = ['GET'])
def home():
    resjson = []
    t = {
            'state' : True
            }
    resjson
    json = jsonify(t)
    
    return json


## 顯示個人介面
## 前端傳ID，後端根據ID 回傳json格式的member資料    
    #http://127.0.0.1:5000/
@app.route("/personalPage", methods = ['GET','POST'])
def personalPage():
    connect = pymysql.connect(host = "127.0.0.1", user = "root"
                          , password = "admin", db = "test")
    cursor = connect.cursor()
    userID = request.form['id']
    SQLIns = "SELECT * FROM MEMBER WHERE ID = {0}".format(userID)
    try:
       # 执行sql语句
       if(cursor.execute(SQLIns)):
           data = cursor.fetchone()
           t = {
               'state' : True,              # state 表示 是否成功 
               'ID' : data[0],
               'PhoneNumber' : data[1],
               'Name' : data[2],
               'NickName' : data[3],
               'Email' : data[4],
               'Account' : data[5],
               'Password' : data[6],
               'ImageURL' : data[7]
               }
           return jsonify(t)
       else:
           t = {
               'state' : False              # state 表示 是否成功 
               }
           return jsonify(t)
    except:
	   # 如果发生错误则回滚
       connect.rollback()
       print("DB rollback")       
    connect.close()


@app.route("/personalPage/onSale", methods = ['POST'])
def onSale():
    connect = pymysql.connect(host = "127.0.0.1", user = "root"
                          , password = "admin", db = "test")
    cursor = connect.cursor()
    userID = request.form['id']
    SQLIns = "SELECT ProductName, Price, LowestPrice, BiddingPrice, BiddingUnitPrice, BiddingDeadline FROM product WHERE SellerID = {0}".format(userID)
    try:
       # 执行sql语句
       if(cursor.execute(SQLIns)):
           data = cursor.fetchall()
           resJson = []
           t = {}
           for rows in data:                   
               t  =  {                                   
                        'ProductName' : rows[0],                                                   
                        'Price' :    rows[1],
                        'LowestPrice' : rows[2],
                        'BiddingPrice' : rows[3],
                        'BiddingUnitPrice' : rows[4],
                        'BiddingDeadLine' : rows[5]                                                            
                    }       
               resJson.append(t)                                         
           return jsonify(resJson)
       else:
           t = {
               'state' : False              # state 表示 是否成功 
               }
           return jsonify(t)
    except Exception as e:
        #印出錯誤訊息
        print(e)
	   # 如果发生错误则回滚
        connect.rollback()
        print("DB rollback")       
    connect.close()  


#上架商品

@app.route("/personalPage/onSale/sale", methods = ['POST'])
def sale():
    connect = pymysql.connect(host = "127.0.0.1", user = "root"
                          , password = "admin", db = "test")
    cursor = connect.cursor()
    print(request.form)
    bidding = request.form['bidding']
    bidding = int(bidding)
    sellerID = request.form['sellerID']
    productName = request.form['productName']
    imageURL = request.form['imageURL']
    amount = request.form['amount']
    price = request.form['price']
    information = request.form['information']
    category = request.form['category']
    if(bidding):
        lowestPrice = request.form['lowestPrice']
        biddingPrice = request.form['biddingPrice']
        biddingUnitPrice = request.form['biddingUnitPrice']
        biddingDeadline = (datetime.date.today() + datetime.timedelta(days=3))

        # biddingTopUser 前端不用傳，有人下標以後才會有資料
    SQLIns = "INSERT INTO product (SellerID, ProductName, ImageURL, Amount, Price, \
LowestPrice, BiddingPrice, BiddingUnitPrice, BiddingDeadline, BiddingTopUserID, Information, Category, AvgEv, TotalEvCount) "
    if(bidding):
        SQLIns += "VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', NULL, '{9}', '{10}', '0', '0')"\
                    .format(sellerID, productName, imageURL, amount, price, lowestPrice, biddingPrice, biddingUnitPrice, biddingDeadline, information, category)
    else:
        SQLIns += "VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', NULL, NULL, NULL, NULL, NULL, '{5}', '{6}', '0', '0')"\
                    .format(sellerID, productName, imageURL, amount, price, information, category)
    print(SQLIns)
    SQLIns2 = "SELECT AUTO_INCREMENT FROM information_schema.TABLES WHERE TABLE_SCHEMA = 'test' AND TABLE_NAME = 'product'"
    cursor.execute(SQLIns2)
    data = cursor.fetchone()
    productID = data[0]
    try:
       # 执行sql语句
       if(cursor.execute(SQLIns)):
           t = {
               'state' : True,              # state 表示 是否成功                
               'productID' : productID
               }
           connect.commit()
           return jsonify(t)
       else:
           t = {
               'state' : False              # state 表示 是否成功 
               }
           return jsonify(t)
    except Exception as e:
        #印出錯誤訊息
        print(e)
	   # 如果发生错误则回滚
        connect.rollback()
        print("DB rollback")       
    connect.close()   

# 編輯商品資訊
    
@app.route("/personalPage/onSale/edit", methods = ['POST'])
def edit(): 
    connect = pymysql.connect(host = "127.0.0.1", user = "root"
                          , password = "admin", db = "test")
    cursor = connect.cursor()
    print(request.form)
    productID = request.form['id']
    information = request.form['information']
    SQLIns = "UPDATE product SET Information = '{0}' WHERE ProductID = '{1}'".format(information, productID)
    try:
       # 执行sql语句
       if(cursor.execute(SQLIns)):
           t = {
               'state' : True,              # state 表示 是否成功                
               }
           connect.commit()
           return jsonify(t)
       else:
           t = {
               'state' : False              # state 表示 是否成功 
               }
           return jsonify(t)
    except Exception as e:
        #印出錯誤訊息
        print(e)
	   # 如果发生错误则回滚
        connect.rollback()
        print("DB rollback")       
    connect.close()       
    
# 刪除商品
        
@app.route("/personalPage/onSale/delete", methods = ['POST'])
def delete(): 
    connect = pymysql.connect(host = "127.0.0.1", user = "root"
                          , password = "admin", db = "test")
    cursor = connect.cursor()
    print(request.form)
    productID = request.form['id']    
    SQLIns = "DELETE FROM product WHERE ProductID = '{0}'".format(productID)
    try:
       # 执行sql语句
       if(cursor.execute(SQLIns)):
           t = {
               'state' : True,              # state 表示 是否成功                
               }
           connect.commit()
           return jsonify(t)
       else:
           t = {
               'state' : False              # state 表示 是否成功 
               }
           return jsonify(t)
    except Exception as e:
        #印出錯誤訊息
        print(e)
	   # 如果发生错误则回滚
        connect.rollback()
        print("DB rollback")       
    connect.close()  

# 顯示交易中商品
    
@app.route("/personalPage/onTrade", methods = ['POST'])
def onTrade():           
    connect = pymysql.connect(host = "127.0.0.1", user = "root"
                          , password = "admin", db = "test")
    cursor = connect.cursor()
    print(request.form)
    userID = request.form['id']
    #, TradeAmount, TradePrice, CompletedType
    SQLIns1 = "SELECT TradeID, ProductName, TradeAmount, TradePrice FROM product, trade WHERE trade.SellerID = '{0}' AND trade.ProductID = product.ProductID AND CompletedType = 0"\
                .format(userID)
    SQLIns2 = "SELECT ProductName, TradeAmount, TradePrice FROM product, trade WHERE trade.BuyerID = '{0}' AND trade.ProductID = product.ProductID AND CompletedType = 0"\
                .format(userID)
    try:
       # 执行sql语句
       cursor.execute(SQLIns1)
       data1 = cursor.fetchall()
       resJson = []
       t = {}
       cursor.execute(SQLIns2)
       data2 = cursor.fetchall()
       if(data1 != ()):
           for rows in data1:
               t = {                       
                   'TradeID' : rows[0],
                   'ProductName' : rows[1],
                   'TradeAmount' : rows[2],
                   'TradePrice' : rows[3],                                                          
                   'Identity' : '0'         # 0 = 是賣家
                   }
               resJson.append(t)
       if(data2 != ()):
           for rows in data2:
               t = {
                   'TradeID' : rows[0],
                   'ProductName' : rows[0],
                   'TradeAmount' : rows[1],
                   'TradePrice' : rows[2],                                                          
                   'Identity' : '1'         # 1 = 是買家
                   }
               resJson.append(t)               
           return jsonify(resJson)
       if(data1 == () and data2 == ()):
           t = {
               'state' : False              # state 表示 是否成功 
               }           
           return jsonify(t)
    except Exception as e:
        #印出錯誤訊息
        print(e)
	   # 如果发生错误则回滚
        connect.rollback()
        print("DB rollback")       
    connect.close()      
    
# 交易完成
    
@app.route("/personalPage/onTrade/tradeCompleted", methods = ['POST'])
def tradeCompelete():           
    connect = pymysql.connect(host = "127.0.0.1", user = "root"
                          , password = "admin", db = "test")    
    cursor = connect.cursor()        
    print(request.form)
    tradeID = request.form['id']
    productEv = request.form['productEv']
    memberEv = request.form['memberEv']
    evText = request.form['evText']
    SQLIns1 = "SELECT SellerID, ProductID FROM trade WHERE TradeID = '{0}'".format(tradeID)
    try:
        # 执行sql语句
        cursor.execute(SQLIns1)
        data = cursor.fetchone()
        sellerID = data[0]
        productID = data[1]
        SQLIns2 = "UPDATE trade SET CompletedType = '1', BuyerEvProduct = '{0}', BuyerEvSeller = '{1}', BuyerEvText = '{2}' WHERE TradeID = '{3}'"\
                    .format(productEv, memberEv, evText, tradeID)  
        cursor.execute(SQLIns2)
        SQLIns3 = "UPDATE member SET AvgEv = ((AvgEv * TotalEvCount) + '{0}') / (TotalEvCount + 1), TotalEvCount = TotalEvCount + 1 WHERE ID = '{1}'"\
                    .format(memberEv, sellerID)                
        cursor.execute(SQLIns3)
        SQLIns4 = "UPDATE product SET AvgEv = ((AvgEv * TotalEvCount) + '{0}') / (TotalEvCount + 1), TotalEvCount = TotalEvCount + 1 WHERE ProductID = '{1}'"\
                    .format(productEv, productID)
        cursor.execute(SQLIns4)
        connect.commit()
        t = {
                'state' : True
                }
        return jsonify(t)       
    except Exception as e:
        #印出錯誤訊息
        print(e)
	   # 如果发生错误则回滚
        connect.rollback()
        print("DB rollback")       
    connect.close()

@app.route("/personalPage/tradeRecord", methods = ['POST'])
def tradeRecord():
    connect = pymysql.connect(host = "127.0.0.1", user = "root"
                          , password = "admin", db = "test")    
    cursor = connect.cursor()     
    userID = request.form['id']
    
    print(request.form)
    # 找出 交易紀錄中 所需要的資料， 條件設定為 賣家是該ID 且交易狀態是完成
    SQLIns1 = "SELECT BuyerID,  productID, TradePrice, TradeAmount, BuyerEvProduct, BuyerEvSeller, BuyerEvText FROM trade  WHERE SellerID = '{0}' AND CompletedType = '1'"\
                .format(userID)
    # 找出 交易紀錄中 所需要的資料， 條件設定為 買家是該ID 且交易狀態是完成                
    SQLIns2 = "SELECT SellerID,  productID, TradePrice, TradeAmount, BuyerEvProduct, BuyerEvSeller, BuyerEvText FROM trade  WHERE BuyerID = '{0}' AND CompletedType = '1'"\
                .format(userID)
    resJson = []
    t = {}
    try:
        #執行SQL語句
        cursor.execute(SQLIns1)
        data1 = cursor.fetchall()
        print(data1)
        cursor.execute(SQLIns2)
        data2 = cursor.fetchall()
        print(data2)
        for rows in data1:
            SQLIns3 = "SELECT NickName FROM member WHERE ID = %(userID)s"
            SQLIns4 = "SELECT ProductName FROM product WHERE ProductID = %(productID)s"
            cursor.execute(SQLIns3, {'userID' : rows[0]})        
            dataTmp1 = cursor.fetchone()
            cursor.execute(SQLIns4, {'productID' : rows[1]})
            dataTmp2 = cursor.fetchone()
            t = {
                    'Identity' : '0',        # 0 = 是賣家
                    'Name' : dataTmp1[0],                    
                    'ProductName' : dataTmp2[0],
                    'TradePrice' : rows[2],
                    'TradeAmount' : rows[3],
                    'BuyerEvProduct' : rows[4],
                    'BuyerEvSeller' : rows[5],
                    'BuyerEvText' : rows[6]
                    }
            resJson.append(t)
        for rows in data2:
            SQLIns3 = "SELECT NickName FROM member WHERE ID = %(userID)s"
            SQLIns4 = "SELECT ProductName FROM product WHERE ProductID = %(productID)s"
            cursor.execute(SQLIns3, {'userID' : rows[0]})        
            dataTmp1 = cursor.fetchone()
            cursor.execute(SQLIns4, {'productID' : rows[1]})
            dataTmp2 = cursor.fetchone()
            t = {
                    'Identity' : '1',        # 1 = 是買家
                    'Name' : dataTmp1[0],                    
                    'ProductName' : dataTmp2[0],
                    'TradePrice' : rows[2],
                    'TradeAmount' : rows[3],
                    'BuyerEvProduct' : rows[4],
                    'BuyerEvSeller' : rows[5],
                    'BuyerEvText' : rows[6]
                    }
            resJson.append(t)
        print(resJson)
        return jsonify(resJson)
    except Exception as e:
        #印出錯誤訊息
        print(e)
	   # 錯誤回滾
        connect.rollback()
        print("DB rollback")       
    connect.close()  
    
"""@app.route("/personalPage/surfedRecord", methods = ['POST'])
def surfedRecord():
    connect = pymysql.connect(host = "127.0.0.1", user = "root"
                          , password = "admin", db = "test")    
    cursor = connect.cursor()     
    userID = request.form['id']
    print(request.form)
    SQLIns = ""
    try:
        
    except Exception as e:
        #印出錯誤訊息
        print(e)
	   # 如果发生错误则回滚
        connect.rollback()
        print("DB rollback")       
    connect.close() """
       
if (__name__ == "__main__") :
    app.run()
    