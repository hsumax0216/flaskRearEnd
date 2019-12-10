from flask import Flask, request, jsonify,render_template
import pymysql

app = Flask(__name__)
app.debug = True

@app.route("/")
def home():
    return "Hello Flask"
## 註冊
@app.route("/signUp", methods=['GET', 'POST'])
def signUp():
	if(request.method == 'POST'):
		print("method POST success")
		connect = pymysql.connect(host = "127.0.0.1", user = "root"
							  , password = "admin", db = "test")
		cursor = connect.cursor()
		#print(request.headers)
		print(request.form)
		userPhone = request.form['Phone']
		userName = request.form['Name']
		userNickname = request.form['Id']
		userEmail = request.form['Email']
		userAccount = request.form['Account']
		userPassword = request.form['Password']
		#userImageURL = request.form['imageURL']
		print(userPhone)
		print(userName)
		print(userNickname)
		print(userEmail)
		print(userAccount)
		print(userPassword)
		#print(userPassword)
		# 寫入database
		#SQLIns = "INSERT INTO member(PhoneNumber, Name, NickName, Email, Account, Password, ImageURL) \
		#          VALUES ('%s', '%s',  '%s', '%s', '%s', '%s','%s')"\
		#          % (userPhone, userName, userNickname, userEmail, userAccount, userPassword, userImageURL)
		SQLIns = "INSERT INTO MEMBER (PhoneNumber, Name, NickName, Email, Account, Password, ImageURL, AvgEv, TotalEvCount) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '0', '0')"\
				  .format(userPhone, userName, userNickname, userEmail, userAccount, userPassword, userImageURL)
		print(SQLIns)
		try:
		   # 执行sql语句
		   if(cursor.execute(SQLIns)):
			   t = {
				   'state' : True,              # state 表示 是否成功 
				   }
			   # 提交到数据库执行
			   connect.commit()
			   return jsonify(t)	   
		except:
		   # 如果发生错误则回滚
		   connect.rollback()
		   print("DB rollback")
		   
		connect.close()
		return render_template('index.html')
	if(request.method == 'GET'):
		print(request)
		return render_template('registered.html')



## 登入

@app.route("/signIn", methods = ['POST'])
def signIn():
    connect = pymysql.connect(host = "127.0.0.1", user = "root"
                          , password = "admin", db = "test")
    cursor = connect.cursor()
    userAccount = request.form['account']
    userPassword = request.form['password']
    SQLIns = "SELECT * FROM MEMBER WHERE Account = '{0}' AND Password = '{1}' ".format(userAccount, userPassword)
    try:
       # 执行sql语句
       if(cursor.execute(SQLIns)):
           data = cursor.fetchone()
           t = {
               'state' : True,               # state 表示 是否成功 
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
               'state' : False               # state 表示 是否成功 
               }
           return jsonify(t)
    except:
	   # 如果发生错误则回滚
       connect.rollback()
       print("DB rollback")       
    connect.close()
    
    
    
## 修改密碼
## 前端傳 帳號, 前密碼, 新密碼
## 後端根據帳號和前密碼去尋找，要更改的會員是誰，並且改密碼
    
@app.route("/changePassword", methods = ['POST'])
def changePassword():
    connect = pymysql.connect(host = "127.0.0.1", user = "root"
                          , password = "admin", db = "test")
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
    
    
    
    
if (__name__ == "__main__") :
    app.debug = True
    app.run()
    
    