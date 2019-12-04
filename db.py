from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
from hellow import member,product,trade,Surfedrecord,Appointboard,comment,Bidding

app = Flask(__name__)
app.debug = True
#app.config['SECRET_KEY'] = 'hard to guess string'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:admin@127.0.0.1:3306/test"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)

@app.route("/")
def home():
	return "ggagag"
'''
admin_member = member(\
	PhoneNumber='0912345678',\
	Name='王八',NickName='',\
	Email='00657013@mail.ntou.edu.tw',\
	Account='smilehaha154',\
	Password='a878787',\
	ImageURL='www.facebook.com'\
	)'''
a=member.query.all()
print(a)

'''
try:
	db.session.add(admin_member)
	db.session.commit()
except Exception as e:
	print(e)
	db.session.rollback()
'''


#if __name__=="__main__":
#	app.run()