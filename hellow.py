import os
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql

#basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.debug = True
#app.config['SECRET_KEY'] = 'hard to guess string'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:admin@127.0.0.1:3306/test"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)

class member(db.Model):
	_tablename_='member'
	ID = db.Column(db.Integer,nullable=False,primary_key=True,autoincrement=True)
	PhoneNumber = db.Column(db.CHAR(10))
	Name = db.Column(db.CHAR(10),nullable=False)
	NickName = db.Column(db.CHAR(20))
	Email = db.Column(db.VARCHAR(255),nullable=False)
	Account = db.Column(db.CHAR(40),nullable=False)
	Password = db.Column(db.CHAR(16),nullable=False)
	ImageURL = db.Column(db.VARCHAR(255))
	
	def __repr__(self):
		return '<member %r %r>' % (self.ID, self.Name)

class product(db.Model):
	_tablename_ = 'product'
	ProductID = db.Column(db.Integer,nullable=False,primary_key=True,autoincrement=True)
	SellerID = db.Column(db.Integer,db.ForeignKey('member.ID'))
	ProductName = db.Column(db.VARCHAR(255))
	ImageURL = db.Column(db.VARCHAR(255))
	Amount = db.Column(db.Integer,nullable=False)
	Price = db.Column(db.Integer)
	LowestPrice = db.Column(db.Integer)
	BiddingPrice = db.Column(db.Integer)
	BiddingUnitPrice = db.Column(db.Integer)
	BiddingDeadline = db.Column(db.DateTime)
	BiddingTopUserID = db.Column(db.Integer)
	Information = db.Column(db.Text(255))
	Category = db.Column(db.VARCHAR(255),nullable=False)
	
	def __repr__(self):
		return '<product %r>' % self.ProductID

class trade(db.Model):
	_tablename_ = 'trade'
	TradeID = db.Column(db.Integer,nullable=False,primary_key=True,autoincrement=True)
	SellerID = db.Column(db.Integer,db.ForeignKey('member.ID'),nullable=False,primary_key=True)
	BuyerID = db.Column(db.Integer,db.ForeignKey('member.ID'))
	ProductID = db.Column(db.Integer,db.ForeignKey('product.ProductID'))
	TradeAmount = db.Column(db.Integer)
	TradePrice = db.Column(db.Integer)
	CompletedType = db.Column(db.Boolean)
	
	
	def __repr__(self):
		return '<trade %r>' % self.TradeID		

class Surfedrecord(db.Model):
	_tablename_ = 'Surfedrecord'
	UserID = db.Column(db.Integer,db.ForeignKey('member.ID'),nullable=False,primary_key=True)
	ProductID = db.Column(db.Integer,db.ForeignKey('product.ProductID'),nullable=False,primary_key=True)
	SurfingDate = db.Column(db.DateTime,nullable=False)
	TimeToLeaveDate = db.Column(db.DateTime,nullable=False)
	
	
	def __repr__(self):
		return '<Surfedrecord %r %r>' % (self.UserID , self.ProductID)

class Appointboard(db.Model):
	_tablename_ = 'Appointboard'
	TradeID = db.Column(db.Integer,db.ForeignKey('trade.TradeID'),nullable=False,primary_key=True)
	AppointDate = db.Column(db.DateTime)
	BoughtDate = db.Column(db.DateTime,nullable=False)
	
	
	def __repr__(self):
		return '<Appointboard %r>' % self.Name

class comment(db.Model):
	_tablename_ = 'comment'
	CommentID = db.Column(db.Integer,nullable=False,primary_key=True,autoincrement=True)
	TradeID = db.Column(db.Integer,db.ForeignKey('trade.TradeID'))
	ProductID = db.Column(db.Integer,db.ForeignKey('product.ProductID'),nullable=False)
	Information = db.Column(db.Text(255))
	CommentDatetime = db.Column(db.DateTime,nullable=False)
	
	
	def __repr__(self):
		return '<comment %r>' % self.Name

class Bidding(db.Model):
	_tablename_ = 'Bidding'
	ProductID = db.Column(db.Integer,db.ForeignKey('product.ProductID'),nullable=False,primary_key=True)
	BiddingUserID = db.Column(db.Integer,db.ForeignKey('member.ID'),nullable=False,primary_key=True)
	
	
	def __repr__(self):
		return '<Bidding %r>' % self.Name