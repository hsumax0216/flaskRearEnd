from flask import render_template, session, redirect, url_for, current_app,request, jsonify
from flask_sqlalchemy import SQLAlchemy
import pymysql
import sys
import datetime
from .. import db
from ..models import member, product, trade, Surfedrecord, Appointboard, comment, Bidding
#from ..email import send_email
from . import main
#from .forms import NameForm

'''
@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            if current_app.config['FLASKY_ADMIN']:
                send_email(current_app.config['FLASKY_ADMIN'], 'New User',
                           'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('.index'))
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False))
'''


@main.route("/index", methods = ['GET'])
def homepage():
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

@main.route("/product_Category/<Category>", methods = ['GET'])
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

@main.route("/signUp", methods = ['GET'])
def signUp():

    connect = pymysql.connect(host = "140.121.197.131", user = "root"
                          , password = "soselab401", db = "test")
    cursor = connect.cursor()

   # GET 格式
    userPhone = request.args.get("Phone")           #手機
    userName = request.args.get("Name")             #姓名
    userNickname = request.args.get("Id")           #暱稱
    userEmail = request.args.get("Email")           #信箱
    userAccount = request.args.get("Account")       #帳號
    userPassword = request.args.get("Password")     #密碼

     # 寫入database
    SQLIns = "INSERT INTO MEMBER (PhoneNumber, Name, NickName, Email, Account, Password, ImageURL, AvgEv, TotalEvCount) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', NULL, '0', '0')"\
                  .format(userPhone, userName, userNickname, userEmail, userAccount, userPassword)
    try:
       # 执行sql语句
       if(cursor.execute(SQLIns)):
           t = {
                   'state' : True              # state 表示 是否成功
                   }
           # 提交到数据库执行
           connect.commit()
           return jsonify(t)
       else:
           t = {
                   'state' : False              # state 表示 是否成功
                   }
           # 提交到数据库执行
           connect.commit()
           return jsonify(t)
    except Exception as e:
    #印出錯誤訊息
        print(e)
	# 錯誤回滾
        connect.rollback()
        print("DB rollback")
    connect.close()

## 登入

@main.route("/signIn", methods = ['GET','POST'])
def signIn():
    connect = pymysql.connect(host = "140.121.197.131", user = "root"
                          , password = "soselab401", db = "test")
    cursor = connect.cursor()
    if request.method == 'POST':
    # POST 格式
        userAccount = request.form['account']   # 登入帳號
        userPassword = request.form['password'] # 登入密碼


        SQLIns = "SELECT * FROM MEMBER WHERE Account = '{0}' AND Password = '{1}' ".format(userAccount, userPassword)
        try:
       # 執行sql语句
           if(cursor.execute(SQLIns)):
               data = cursor.fetchone()
               t = {
                       'state' : True,              # state 表示 是否成功
                       'ID' : data[0],              # 回傳登入者的userID
                       'PhoneNumber' : data[1],     # 回傳登入者的手機
                       'Name' : data[2],            # 回傳登入者姓名
                       'NickName' : data[3],        # 回傳登入者暱稱
                       'Email' : data[4],           # 回傳登入者信箱
                       'Account' : data[5],         # 回傳登入者帳號
                       'Password' : data[6],        # 回傳登入者密碼
                       'ImageURL' : data[7]         # 回傳登入者圖片
                       }
               return jsonify(t)
           else:
               t = {
                       'state' : False               # state 表示 是否成功
                       }
               return jsonify(t)
        except Exception as e:
        #印出錯誤訊息
            print(e)
	   # 錯誤回滾
            connect.rollback()
            print("DB rollback")
    connect.close()
    return 'signIn Page...'


## 顯示個人介面
## 前端傳ID，後端根據ID 回傳json格式的member資料
    #http://127.0.0.1:5000/
@main.route("/personalPage", methods = ['POST'])
def personalPage():
    connect = pymysql.connect(host = "140.121.197.131", user = "root"
                          , password = "soselab401", db = "test")
    cursor = connect.cursor()
    userID = request.form['ID']
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
    return 'personal Page...'

# 顯示上架商品

@main.route("/personalPage/onSale", methods = ['POST'])
def onSale():
    connect = pymysql.connect(host = "140.121.197.131", user = "root"
                          , password = "soselab401", db = "test")
    cursor = connect.cursor()
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
	   # 如果发生错误则回滚
        connect.rollback()
        print("DB rollback")
    connect.close()
    return 'personalPage onSale...'


#上架商品

@main.route("/personalPage/onSale/sale", methods = ['POST'])
def sale():
    connect = pymysql.connect(host = "140.121.197.131", user = "root"
                          , password = "soselab401", db = "test")
    cursor = connect.cursor()
    print(request.form)
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
	LowestPrice, BiddingPrice, BiddingUnitPrice, BiddingDeadline, BiddingTopUserID, Information, Category, AvgEv, TotalEvCount) "
    if(bidding):
        SQLIns += "VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', NULL, '{9}', '{10}', '0', '0')"\
                    .format(sellerID, productName, imageURL, amount, price, lowestPrice, biddingPrice, biddingUnitPrice, biddingDeadline, information, category)
    else:
        SQLIns += "VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', NULL, NULL, NULL, NULL, NULL, '{5}', '{6}', '0', '0')"\
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
	   # 如果发生错误则回滚
        connect.rollback()
        print("DB rollback")
    connect.close()
    return 'personalPage onSale sale page...'

# 編輯商品資訊

@main.route("/personalPage/onSale/edit", methods = ['POST'])
def edit():
    connect = pymysql.connect(host = "140.121.197.131", user = "root"
                          , password = "soselab401", db = "test")
    cursor = connect.cursor()
    print(request.form)
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

@main.route("/personalPage/onSale/delete", methods = ['POST'])
def delete():
    connect = pymysql.connect(host = "140.121.197.131", user = "root"
                          , password = "soselab401", db = "test")
    cursor = connect.cursor()
    print(request.form)
    productID = request.form['ID']
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
    return 'personalPage onSale sale delete...'


# 顯示交易中商品

@main.route("/personalPage/onTrade", methods = ['POST'])
def onTrade():
    connect = pymysql.connect(host = "140.121.197.131", user = "root"
                          , password = "soselab401", db = "test")
    cursor = connect.cursor()
    print(request.form)
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

@main.route("/personalPage/onTrade/tradeCompleted", methods = ['POST'])
def tradeCompelete():
    connect = pymysql.connect(host = "140.121.197.131", user = "root"
                          , password = "soselab401", db = "test")
    cursor = connect.cursor()
    print(request.form)
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

@main.route("/personalPage/tradeRecord", methods = ['POST'])
def tradeRecord():
    connect = pymysql.connect(host = "140.121.197.131", user = "root"
                          , password = "soselab401", db = "test")
    cursor = connect.cursor()
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

@main.route("/personalPage/surfedRecord", methods = ['POST'])
def surfedRecord():
    connect = pymysql.connect(host = "140.121.197.131", user = "root"
                          , password = "soselab401", db = "test")
    cursor = connect.cursor()
    userID = request.form['ID']
    print(request.form)
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

@main.route("/personalPage/reservation" , methods = ['POST'])
def reservation():
    connect = pymysql.connect(host = "140.121.197.131", user = "root"
                          , password = "soselab401", db = "test")    #soselab401
    cursor = connect.cursor()
    userID = request.form['ID']
    print(request.form)
    SQLIns = "SELECT * FROM appointboard WHERE SellerID = '{0}' OR BuyerID = '{0}'".format(userID)

    resJson = []
    t = {}
    try :
        if(cursor.execute(SQLIns)):
            data = cursor.fetchall()
            print(data)
            for rows in data:
                SQLIns2 = "SELECT Information FROM comment WHERE TradeID =  %(tID)s"
                cursor.execute(SQLIns2, {'tID' : rows[0]})
                dataComment = cursor.fetchall()

                SQLIns3 = "SELECT NickName FROM member WHERE ID = %(sID)s"
                cursor.execute(SQLIns3, {'sID' : rows[1]})
                dataSellerNickName = cursor.fetchone()

                SQLIns4 = "SELECT NickName FROM member WHERE ID = %(bID)s"
                cursor.execute(SQLIns4, {'bID' : rows[2]})
                dataBuyerNickName = cursor.fetchone()

                SQLIns5 = "SELECT ProductName, ImageURL FROM product WHERE ProductID = %(pID)s"
                cursor.execute(SQLIns5, {'pID' : rows[3]} )
                dataProduct = cursor.fetchone()

                print(rows)
                t = {
                        'state' : True,
                        'AppointDate' : rows[4],
                        'BoughtDate' : rows[5],
                        'Comment' : dataComment,
                        'SellerName' : dataSellerNickName[0],
                        'BuyerName' : dataBuyerNickName[0],
                        'ProductName' : dataProduct[0],
                        'ProductImg' : dataProduct[1]
                        }
                resJson.append(t)
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

@main.route("/personalPage/reservation/comment" , methods = ['POST'])
def reservationComment():
    connect = pymysql.connect(host = "140.121.197.131", user = "root"
                          , password = "soselab401", db = "test")    #soselab401
    cursor = connect.cursor()
    tradeID = request.form['TradeID']
    productID = request.form['ProductID']
    information = request.form['Information']
    SQLIns = "INSERT INTO comment(TradeID, ProductID, Information, CommentDateTime) VALUES('{0}', '{1}', '{2}', '{3}')".format(tradeID, productID, information, datetime.date.today())
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

@main.route("/CheckOutPage", methods = ['GET','POST'])#CheckOutPage為暫定url
def CheckOutPage():#dict={'key':'value'}#list=[value]#value=every type
	if(request.method == 'POST'):
		member_id = request.form['member_id']
		Productform = request.form.getlist('product')
		Amountform = request.form.getlist('Amount')
		Priceform = request.form.getlist('price')
		boughtItem = dict(zip(Productform,Amountform))						#商品與數量字典
		itemPrice = dict(zip(Productform,Priceform))						#商品與總價字典
		buyer = member.query.filter_by(ID = member_id).first()				#買家sql
		#state = 1 表示 無錯誤
		t={'state':1}														#回傳JSON字典
		errorProduct = []													#發生商品錯誤list
		errorSeller = []													#發生賣家錯誤list
		if(buyer is None):
			t['state']=0
			t['inform']='buyer memberID: '+str(member_id)+' didn\'t exist.'
			return jsonify(t)
		for i in boughtItem:
			prID = i														#商品ID
			Product = product.query.filter_by(ProductID = prID).first()		#商品sql
			amount = int(boughtItem[i])										#購買數量
			Cprice = int(itemPrice[i])										#購買總價
			#
			#商品總數 >= 購買商品數量#購買總數 > 0
			if(Product is not None \
				and (Product.Amount) >= (amount) \
				and (amount) > 0):
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
						#提交DB
						db.session.commit()
						db.session.refresh(Trade,['TradeID'])
						tradeidtemp = Trade.TradeID
						print('Trade.TradeID:'+str(tradeidtemp))
						Appboard = Appointboard(
							TradeID = tradeidtemp,\
							SellerID = seller.ID,\
							BuyerID = buyer.ID,\
							ProductID = Product.ProductID,\
							BoughtDate = datetime.datetime.now()
							)
						db.session.add(Appboard)
						db.session.commit()
					except Exception as e:
						print(e)
						#state = 0表示 出現錯誤
						t['state'] = 0
						t['inform'] = 'DB was rollback.'
						db.session.rollback()
				else:
					t['state'] = 0
					errorSeller.append(int(Product.SellerID))
					t['inform_seller'] = "SellerID:  "+str(Product.SellerID)+\
						"  is error.(by same person or exist)"
			else:
				t['state'] = 0
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

@main.route("/product_searching", methods = ['GET'])
def ProductSearch():
    connect = pymysql.connect(host = "140.121.197.131", user = "root"
                          , password = "soselab401", db = "test")
    cursor = connect.cursor()
    productName =request.args.get('name','無')
    lowerPrice =request.args.get('firstPrice',0)
    higherPrice =request.args.get('lastPrice',sys.maxsize)
    productEv =request.args.get('商品星級',0)

    SQLIns = "SELECT * FROM product WHERE ProductName  LIKE '%{0}%' AND AvgEv >={1} AND  (Price BETWEEN {2} AND {3} OR BiddingPrice BETWEEN {4} AND {5}) "\
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
    return 'product_searching...'

@main.route("/product_information/<ProductID>", methods = ['GET'])
def ProductInfo(ProductID):
    connect = pymysql.connect(host = "140.121.197.131", user = "root"
                          , password = "soselab401", db = "test")
    cursor = connect.cursor()

    SQLIns = "SELECT * FROM product WHERE ProductID = {0}".format(ProductID)
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
    return 'product_information ProductID={}...'.format(ProductID)