from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
from hellow import member,product,trade,Surfedrecord,Appointboard,comment,Bidding

app = Flask(__name__)
app.debug = True#mysql+pymysql://root:soselab401@140.121.197.131:3306/test
#app.config['SECRET_KEY'] = 'hard to guess string'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:admin@127.0.0.1:3306/test"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True


class func():
	def __init__(self, db):
		self.db = db
	def findmember(self):
		return member.query.all()#.filter_by(Account=ac,Password=pw).all()
	def addmember(self,name,email,ac,pw,phone=None,nick=None,url=None,avgev=None,tevc=None):
		if(name is None or email is None or ac is None or pw is None):
			print('add member error')
			return 'add member error'
		temp = member(\
			PhoneNumber=phone,\
			Name=name,\
			NickName=nick,\
			Email=email,\
			Account=ac,\
			Password=pw,\
			ImageURL=url,\
			AvgEv=avgev,\
			TotalEvCount=tevc)
		try:
			db.session.add(temp)
			db.session.commit()
		except Exception as e:
			print(e)
			db.session.rollback()
		return 'add member success'
'''	def find(self,name:str,id:int=0):
		return db.session.query.all()#.filter_by(Name=name).all()
'''
@app.route("/")
def home():
	return "ggagag"

        

'''admin_member = member(\
	PhoneNumber='0912345678',\
	Name='王八',NickName='',\
	Email='00657013@mail.ntou.edu.tw',\
	Account='smilehaha154',\
	Password='a878787',\
	ImageURL='www.facebook.com'\
	)'''
db = SQLAlchemy(app)
#a=member.query.all()
print((db))
a=func(db)
print(a.addmember('王八',\
	'00657013@mail.ntou.edu.tw',\
	'smilehaha154',\
	'a878787',\
	'0912345678',\
	'',\
	'www.facebook.com'))
'''b=a.findmember()
print(b)'''
'''

	def find(ac:str,pw:str):
		return db.session.query.filter_by(Account=ac,Password=pw).all()
	def find(id:int,name:str=""):
		return db.session.query.filter_by(ID=id).all()
'''
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