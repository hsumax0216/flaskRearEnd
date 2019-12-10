from flask import Flask, request, jsonify,render_template
from flask_sqlalchemy import SQLAlchemy
from hellow import app,db,member,product,trade,Appointboard,comment#,Bidding
#app,db一定要import
import datetime
import pymysql
@app.route("/AppointedPage", methods = ['GET','POST'])#reservation.html
def AppointedPage():
	if(request.method == 'POST'):
		response = []
		t = {}
		
	if(request.method == 'GET'):
		return render_template('reservation.html')

if (__name__ == "__main__") :
    app.debug = True
    app.run()