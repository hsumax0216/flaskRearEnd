from flask import Flask, request, jsonify
import pymysql
import requests
from .. import main
from config import Config
import json
import random
import smtplib
from email.mime.text import MIMEText
from email.header import Header
code_list = [] 
for i in range(10): # 0-9數字
    code_list.append(str(i))
for i in range(65, 91): # 對應從“A”到“Z”的ASCII碼
    code_list.append(chr(i))
mail_host="mail.ntou.edu.tw"  #设置服务器
mail_user="00657002"    #用户名
mail_pass="H125156743"   #口令 

## 註冊

@main.route("/signUp", methods = ['GET', 'POST'])
def signUp():

    connect = pymysql.connect(host = Config.DB_HOST, user = Config.DB_USER
                          , password = Config.DB_PW, db = Config.DB_DB)
    cursor = connect.cursor()

    if request.method == 'POST':
        userPhone = request.form['Phone']               #手機
        userName = request.form['Name']                 #姓名
        userNickname = request.form['NickName']         #暱稱
        userEmail = request.form['Email']           #信箱
        userAccount = request.form['Account']       #帳號
        userPassword = request.form['Password']     #密碼  
        GRR = request.form['g-recaptcha-response']
        """postData = {
                'secret' : '6LdhqswUAAAAAHV6Bgd6fCtncxole_mXTps5cC0D',
                'response' : GRR
                }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', postData)
        j = json.loads(r.text)"""

        if(not userPhone or not userName or not userNickname or not userEmail or not userAccount or not userPassword ):#or j['success'] == False):
            t = {   
                    'state' : False                
                    }
            return jsonify(t)
        if(True):#j['success'] == True):
            userEmail = userEmail + '@mail.ntou.edu.tw'
            #寄信
            myslice = random.sample(code_list, 6) # 從list中隨機獲取6個元素，作為一個片斷返回
            verification_code = ''.join(myslice) # list to string
            mail_msg = """
<p>
<br>
感謝您註冊海大拍賣系統<br><br><br>
----------------------------
<br><br>
您的暱稱為: {0}
<br>
您註冊的帳號為: {1}
<br>
您註冊的密碼為: {2}
<br><br>
----------------------------
<br><br>
您的註冊信箱認證碼為 {3}
<br><br>
""".format(userNickname, userAccount, userPassword, verification_code)
            sender = '00657002@mail.ntou.edu.tw'
            receivers = [userEmail]
            message = MIMEText(mail_msg, 'html', 'utf-8')
            message['From'] = Header(sender, 'utf-8')
            message['To'] =  Header(receivers[0], 'utf-8')
            
            subject = '感謝您註冊海大拍賣系統'
            message['Subject'] = Header(subject, 'utf-8')
         
         
        
        
            # 寫入database
             
            SQLIns = "INSERT INTO MEMBER (PhoneNumber, Name, NickName, Email, Account, Password, ImageURL, AvgEv, TotalEvCount, VerificationCode, VerificationStatus) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', NULL, '0', '0', '{6}', '0')"\
                          .format(userPhone, userName, userNickname, userEmail, userAccount, userPassword, verification_code)                
            SQLIns2 = "SELECT * FROM member WHERE Account = '{0}'".format(userAccount)
            
            try:
                cursor.execute(SQLIns2)
                data = cursor.fetchone()
                print(data)
                if(data != None):
                    t = {
                            'state' : False
                            }
                    return jsonify(t)
                    
                else:    
                    if(cursor.execute(SQLIns)):
                        try:
                            smtpObj = smtplib.SMTP() 
                            smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
                            smtpObj.login(mail_user,mail_pass)  
                            smtpObj.sendmail(sender, receivers, message.as_string())
                            print ("Success")
                        except smtplib.SMTPException:
                            print ("False")
                        t = {
                                'state' : True,              # state 表示 是否成功 
                                'Account' : userAccount
                                }
                        # 提交到数据库执行
                        connect.commit()
                        return jsonify(t)
                    else:
                        t = {
                                'state' : False              # state 表示 是否成功 
                                }
                        # 提交到数据库执行
                        return jsonify(t)		   
            except Exception as e:
            #印出錯誤訊息
                print(e)
        	# 錯誤回滾
                connect.rollback()
                print("DB rollback")    
    connect.close() 
    return 'signUp Page...'

## 登入

@main.route("/signIn", methods = ['GET','POST'])
def signIn():
    connect = pymysql.connect(host = Config.DB_HOST, user = Config.DB_USER
                          , password = Config.DB_PW, db = Config.DB_DB)
    cursor = connect.cursor()
    if request.method == 'POST': 
    # POST 格式
        userAccount = request.form['Account']   # 登入帳號
        userPassword = request.form['Password'] # 登入密碼
    
    
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
    

## 信箱認證

@main.route("/verification", methods = ['GET','POST'])
def verification():
    connect = pymysql.connect(host = Config.DB_HOST, user = Config.DB_USER
                          , password = Config.DB_PW, db = Config.DB_DB)
    cursor = connect.cursor()
    if request.method == 'POST':
        userID = request.form['Account']
        verificationCode = request.form['VerificationCode']
        SQLIns = "UPDATE member SET VerificationStatus = '1' WHERE Account = '{0}' and VerificationCode = '{1}'"\
                .format(userID, verificationCode)
        try:
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
    return 'verification Page..'
        
    
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