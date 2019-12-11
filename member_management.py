from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

## 註冊

@app.route("/signUp", methods = ['GET'])
def signUp():

    connect = pymysql.connect(host = "140.121.197.131", user = "root"
                          , password = "soselab401", db = "test")
    cursor = connect.cursor()

   # GET 格式
    userPhone = request.args.get("Phone")           #手機
    userName = request.args.get("Name")             #姓名
    userNickname = request.args.get("NickName")           #暱稱
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

@app.route("/signIn", methods = ['GET','POST'])
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
    
    
## 修改密碼
## 前端傳 帳號, 前密碼, 新密碼
## 後端根據帳號和前密碼去尋找，要更改的會員是誰，並且改密碼
"""
@app.route("/changePassword", methods = ['GET','POST'])
def changePassword():
    connect = pymysql.connect(host = "140.121.197.131", "port = 3306", user = "root"
                          , password = "soselab401", db = "test")
    cursor = connect.cursor()
    userAccount = request.form['account']
    userOldPassword = request.form['oldPassword']
    userNewPassword = request.form['newPassword']
    print(userNewPassword)
    SQLIns = "UPDATE MEMBER SET Password = '{0}' WHERE Account = '{1}' AND Password = '{2}' "\
            .format(userNewPassword, userAccount, userOldPassword)
    try:
        # 执行sql语句
       if(cursor.execute(SQLIns)):
           t = {
               'state' : True           # state 表示 是否成功 
               }
           connect.commit()
           return jsonify(t)
       else:
           t = {
               'state' : False          # state 表示 是否成功 
               }
           return jsonify(t)
    except:
	   # 如果发生错误则回滚
       connect.rollback()
       print("DB rollback")       
    connect.close()       
    
"""
    
    
if (__name__ == "__main__") :
    app.run()
    
    