from flask import Flask, request
import pymysql

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello Flask"

@app.route("/signUp", methods = ['POST'])
def signUp():
    connect = pymysql.connect("localhost","root","admin","TESTDB" )
    cursor = connect.cursor()
    print(request.headers)
    print(request.form)
    userID = request.form['ID']
    userPhone = request.form['phone']
    userName = request.form['name']
    userNickname = request.form['nickname']
    userEmail = request.form['e-mail']
    userAccount = request.form['account']
    userPassword = request.form['password']
    userImageURL = request.form['imageURL']
    # 寫入database
    SQLIns = "INSERT INTO member (ID, PhoneNumber, Name, Nickname, Email, Account, Password, ImageURL) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}')"\
              .format(userID, userPhone, userName, userNickname, userEmail, userAccount, userPassword, userImageURL)
    print(SQLIns)
    #connect.commit()
    #
	#
	#"INSERT INTO MEMBER(ID, PhoneNumber, Name, \
    #          Nickname, Email, Account, Password, ImageURL) \
    #          VALUES ('%s', '%s', '%s',  '%s', '%s', '%s',  '%s','%s')"\
    #          % (userID, userPhone, userName, userNickname, userEmail, userAccount, userPassword, userImageURL)
    try:
       # 执行sql语句
       print(cursor.execute(SQLIns))
	   # 提交到数据库执行
       connect.commit()
    except:
	   # 如果发生错误则回滚
       connect.rollback()
       print("DB rollback")
	   
    connect.close()
    return "Successfully SignUp!"






if (__name__ == "__main__") :
    app.run()
    
    