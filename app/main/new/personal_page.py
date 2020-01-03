from flask import Flask, request, jsonify
import pymysql
import datetime
from .. import main
from config import Config

## 顯示個人介面
## 前端傳ID，後端根據ID 回傳json格式的member資料    
    #http://127.0.0.1:5000/
@main.route("/personalPage", methods = ['GET','POST'])
def personalPage():
    
    connect = pymysql.connect(host = Config.DB_HOST, user = Config.DB_USER
                          , password = Config.DB_PW, db = Config.DB_DB)
    cursor = connect.cursor()
    if request.method == 'POST':
        userID = request.form['ID']
        SQLIns = "SELECT * FROM MEMBER WHERE ID = {0}".format(userID)
        SQLIns2 = "SELECT ProductName, Price, LowestPrice, BiddingPrice, BiddingUnitPrice, BiddingDeadline FROM product WHERE SellerID = {0}".format(userID)

       # 执行sql语句
        try:
            resJson = []
            resProduct = []
            resPersonal = {}
            t = {}
            if(cursor.execute(SQLIns)):
                data = cursor.fetchone()
                resPersonal = {
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
            else:
                resPersonal = {
                        'state' : False              # state 表示 是否成功 
                        }
            if(cursor.execute(SQLIns2)):
                data2 = cursor.fetchall()
                resJson = []
                t = {}
                for rows in data2:                   
                    t  =  {       
                            'state' : True,                            
                            'ProductName' : rows[0],                                                   
                            'Price' :    rows[1],
                            'LowestPrice' : rows[2],
                            'BiddingPrice' : rows[3],
                            'BiddingUnitPrice' : rows[4],
                            'BiddingDeadLine' : rows[5]                                                            
                            }       
                    resProduct.append(t)
                else:
                    t = {
                            'state' : False              # state 表示 是否成功 
                            }
                    resProduct.append(t)
            
            resJson.append(resProduct)
            resJson.append(resPersonal)
            return jsonify(resJson)
        except Exception as e:
            print(e)
            connect.rollback()
            print("DB rollback")       
    connect.close()
    return 'personal Page...'

# 顯示上架商品

@main.route("/personalPage/onSale", methods = ['GET','POST'])
def onSale():
    connect = pymysql.connect(host = Config.DB_HOST, user = Config.DB_USER
                          , password = Config.DB_PW, db = Config.DB_DB)
    cursor = connect.cursor()
    if request.method == 'POST':
        userID = request.form['ID']
        SQLIns = "SELECT ProductName, Price, LowestPrice, BiddingPrice, BiddingUnitPrice, BiddingDeadline FROM product WHERE SellerID = {0}".format(userID)
        try:
            # 执行sql语句
            if(cursor.execute(SQLIns)):
                data = cursor.fetchall()
                resJson = []
                t = {}
                for rows in data:                   
                    t  =  {       
                            'state' : True,                            
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
            果发生错误则回滚
            connect.rollback()
            print("DB rollback")       
    connect.close()  
    return 'personalPage onSale...'


#上架商品

@main.route("/personalPage/onSale/sale", methods = ['GET','POST'])
def sale():
    connect = pymysql.connect(host = Config.DB_HOST, user = Config.DB_USER
                          , password = Config.DB_PW, db = Config.DB_DB)
    cursor = connect.cursor()
    if request.method == 'POST':
        bidding = request.form['Bidding']
        bidding = int(bidding)
        sellerID = request.form['SellerID']
        productName = request.form['ProductName']
        imageURL = request.form['ImageURL']
        amount = request.form['Amount']
        price = request.form['Price']
        information = request.form['Information']
        category = request.form['Category']
        if(bidding):
            lowestPrice = request.form['LowestPrice']
            biddingPrice = request.form['BiddingPrice']
            biddingUnitPrice = request.form['BiddingUnitPrice']
            biddingDeadline = (datetime.date.today() + datetime.timedelta(days=3))

        # biddingTopUser 前端不用傳，有人下標以後才會有資料
        SQLIns = "INSERT INTO product (SellerID, ProductName, ImageURL, Amount, Price, \
LowestPrice, BiddingPrice, BiddingUnitPrice, BiddingDeadline, BiddingTopUserID, Information, Category, AvgEv, TotalEvCount,SurfedTimes) "
        if(bidding):
            SQLIns += "VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', NULL, '{9}', '{10}', '0', '0', '0')"\
                        .format(sellerID, productName, imageURL, amount, price, lowestPrice, biddingPrice, biddingUnitPrice, biddingDeadline, information, category)
        else:
            SQLIns += "VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', NULL, NULL, NULL, NULL, NULL, '{5}', '{6}', '0', '0', '0')"\
                        .format(sellerID, productName, imageURL, amount, price, information, category)
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
          #如果发生错误则回滚
          connect.rollback()
          print("DB rollback")       
    connect.close()   
    return 'personalPage onSale sale page...'

# 編輯商品資訊
    
@main.route("/personalPage/onSale/edit", methods = ['GET','POST'])
def edit(): 
    connect = pymysql.connect(host = Config.DB_HOST, user = Config.DB_USER
                          , password = Config.DB_PW, db = Config.DB_DB)
    cursor = connect.cursor()
    
    if request.method == 'POST':
        productID = request.form['ID']
        information = request.form['Information']
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
    return 'personalPage onSale sale edit...'
    
# 刪除商品
        
@main.route("/personalPage/onSale/delete", methods = ['GET','POST'])
def delete(): 
    connect = pymysql.connect(host = Config.DB_HOST, user = Config.DB_USER
                          , password = Config.DB_PW, db = Config.DB_DB)
    cursor = connect.cursor()
    if request.method == 'POST':
        productID = request.form['ID']    
        SQLIns = "DELETE FROM product WHERE ProductID = '{0}'".format(productID)
        SQLIns2 = "DELETE FROM comment WHERE ProductID = '{0}'".format(productID)
        try:
            # 执行sql语句
            if(cursor.execute(SQLIns2) | cursor.execute(SQLIns)):
                t = {
                        'state' : True               # state 表示 是否成功                
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
    return 'personalPage onSale sale delete...'

# 顯示交易中商品
    
@main.route("/personalPage/onTrade", methods = ['GET','POST'])
def onTrade():           
    connect = pymysql.connect(host = Config.DB_HOST, user = Config.DB_USER
                          , password = Config.DB_PW, db = Config.DB_DB)
    cursor = connect.cursor()
    if request.method == 'POST':        
        userID = request.form['ID']
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
                           'state' : True,                        
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
                           'state' : True, 
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
    return 'personalPage onTrade...'
    
# 交易完成
    
@main.route("/personalPage/onTrade/tradeCompleted", methods = ['GET','POST'])
def tradeCompelete():           
    connect = pymysql.connect(host = Config.DB_HOST, user = Config.DB_USER
                          , password = Config.DB_PW, db = Config.DB_DB)
    cursor = connect.cursor()        
    if request.method == 'POST':
        tradeID = request.form['ID']
        productEv = request.form['ProductEv']
        memberEv = request.form['MemberEv']
        evText = request.form['EvText']
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
    return 'personalPage onTrade tradeCompleted...'

#交易紀錄

@main.route("/personalPage/tradeRecord", methods = ['GET','POST'])
def tradeRecord():
    connect = pymysql.connect(host = Config.DB_HOST, user = Config.DB_USER
                          , password = Config.DB_PW, db = Config.DB_DB)   
    cursor = connect.cursor()     
    if request.method == 'POST':
        userID = request.form['ID']
    
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
                        'state' : True, 
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
                        'state' : True, 
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
    return 'personalPage tradeRecord...'

# 瀏覽紀錄    
    
@main.route("/personalPage/surfedRecord", methods = ['GET','POST'])
def surfedRecord():
    connect = pymysql.connect(host = Config.DB_HOST, user = Config.DB_USER
                          , password = Config.DB_PW, db = Config.DB_DB)
    cursor = connect.cursor()
    if request.method == 'POST':     
        userID = request.form['ID']        
        SQLIns = "SELECT * FROM surfedrecord WHERE UserID = '{0}'".format(userID)
        resJson = []
        t = {}
        try:
            if(cursor.execute(SQLIns)):
                data = cursor.fetchall()
                
                for rows in data:
                    print(rows)
                    t = {
                            'state' : True,
                            'ProductName' : rows[2],
                            'ImageURL' : rows[3],
                            'Price' : rows[4],
                            'LowestPrice' : rows[5],
                            'BiddingPrice' : rows[6],
                            'BiddingUnitPrice' : rows[7],
                            'BiddingDeadline' : rows[8],
                            'SurfingDate' : rows[9]
                            }
                    resJson.append(t)
                return jsonify(resJson)    
            else:
                t = {
                        'state' : False
                        }
                return jsonify(t)
            
        except Exception as e:
        #印出錯誤訊息
            print(e)
	   # 如果发生错误则回滚
            connect.rollback()
            print("DB rollback")       
    connect.close() 
    return 'personalPage surfedRecord...'
    
# 顯示預約版
    
@main.route("/personalPage/reservation" , methods = ['GET','POST'])
def reservation():
    connect = pymysql.connect(host = Config.DB_HOST, user = Config.DB_USER
                          , password = Config.DB_PW, db = Config.DB_DB)
    cursor = connect.cursor()     
    if request.method == 'POST':
        userID = request.form['ID']
        print(request.form)
        SQLIns = "SELECT * FROM appointboard WHERE SellerID = '{0}' OR BuyerID = '{0}'".format(userID) 
        
        resJson = []
        t = {}
        t1 = {}
        c = []
        try :
            if(cursor.execute(SQLIns)):
                data = cursor.fetchall()
                print(data)            
                for rows in data:
                    SQLIns2 = "SELECT Information, CommenterID FROM comment WHERE TradeID = '{0}'".format(rows[0])
                    cursor.execute(SQLIns2)
                    dataComment = cursor.fetchall()
                    SQLIns3 = "SELECT NickName FROM member WHERE ID = '{0}'".format(rows[1])
                    cursor.execute(SQLIns3)
                    dataSellerNickName = cursor.fetchone()
                    SQLIns4 = "SELECT NickName FROM member WHERE ID = '{0}'".format(rows[2])
                    cursor.execute(SQLIns4)
                    dataBuyerNickName = cursor.fetchone()
                    SQLIns5 = "SELECT ProductName, ImageURL FROM product WHERE ProductID = '{0}'".format(rows[3])
                    cursor.execute(SQLIns5)
                    dataProduct = cursor.fetchone()   
                    t = {
                            'state' : True,
							'TradeID' : rows[0],			# this 
                            'AppointDate' : rows[4],
                            'BoughtDate' : rows[5],
                            'SellerName' : dataSellerNickName[0],
                            'BuyerName' : dataBuyerNickName[0],
                            'ProductName' : dataProduct[0],
                            'ProductImg' : dataProduct[1]
                            }
                    for info in dataComment:
                        SQLIns6 = "SELECT NickName, ImageURL FROM member WHERE ID = '{0}'".format(info[1])
                        cursor.execute(SQLIns6)
                        dataCommenter = cursor.fetchall()
                        t1 = {
                                'Comment' : info[0],
                                'CommenterName' : dataCommenter[0][0],
                                'CommenterImageURL': dataCommenter[0][1]
                            }      
                        c.append(t1)
                    resJson.append(t)
                    resJson.append(c)
            return jsonify(resJson)       
        except Exception as e:
        #印出錯誤訊息
            print(e)
	   # 如果发生错误则回滚
            connect.rollback()
            print("DB rollback")            
    connect.close() 
    return 'personalPage reservation...'
    
#預約留言    
    
@main.route("/personalPage/reservation/comment" , methods = ['GET','POST'])
def reservationComment():   
    connect = pymysql.connect(host = Config.DB_HOST, user = Config.DB_USER
                          , password = Config.DB_PW, db = Config.DB_DB)
    cursor = connect.cursor()
    if request.method == 'POST':
        userID = request.form['ID']
        tradeID = request.form['TradeID']
        productID = request.form['ProductID']
        information = request.form['Information']
        SQLIns = "INSERT INTO comment(TradeID, ProductID, Information, CommentDateTime, CommenterID) VALUES('{0}', '{1}', '{2}', '{3}', '{4}')".format(tradeID, productID, information, datetime.date.today(),userID)
        try :
            if(cursor.execute(SQLIns)):
                t = {
                        'state' : True
                        }
                connect.commit()
            else:
                t = {
                        'state' : False
                    }
            return jsonify(t)
        except Exception as e:
        #印出錯誤訊息
            print(e)
	   # 如果发生错误则回滚
            connect.rollback()
            print("DB rollback")            
    connect.close()  
    return 'personalPage reservation comment...'