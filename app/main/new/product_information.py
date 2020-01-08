from flask import Flask, request, jsonify,render_template
import pymysql
import datetime
from .. import main
from config import Config

#商品資料及留言資料
@main.route("/product_information", methods = ['GET'])
def ProductInfo():
    connect = pymysql.connect(host = Config.DB_HOST, user = Config.DB_USER
                          , password = Config.DB_PW, db = Config.DB_DB)
    cursor = connect.cursor()
    cursor2= connect.cursor()
    ProductID =request.args.get('ProductID')
    if(not ProductID):
        t = {
               'state' : False              # state 表示 是否成功 
            }
        return jsonify(t)
    
    
          
    SQLIns = "SELECT * FROM product WHERE ProductID = {0}".format(ProductID)
    
    ans=[]
    com=[]
    try:
       # 商品資料
       if(cursor.execute(SQLIns)):
                     
           data = cursor.fetchone()
           
           while data is not None:
               SQLIns2 = "SELECT NickName,ImageURL FROM member WHERE ID = {0}".format(data[1])
               cursor2.execute(SQLIns2)
               data2=cursor2.fetchone()
               if (data2 is not None):
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
                       'TotalEvCount':data[14],
                       'SurfedTimes':data[15],
                       'SellerNickName':data2[0],
                       'SellerImageURL':data2[1]
                       }
                   ans.append(t)
               data = cursor.fetchone()
       else:
           t = {
               'state' : False              # state 表示 是否成功                
               }
           return jsonify(t)
       
        #留言
        
       SQLIns ="SELECT * FROM comment WHERE ProductID  = {0}  AND TradeID IS NULL"\
       .format(ProductID)       
       
       
       if(cursor.execute(SQLIns)):
           data = cursor.fetchone()         
           while data is not None:    
               SQLIns2 = "SELECT NickName,ImageURL FROM member WHERE ID = {0}".format(data[5])               
               cursor2.execute(SQLIns2)    
               data2=cursor2.fetchone()
               if (data2 is not None):
                   t = {
                       'state' : True ,
                       'UserID' : data[5],              
                       'Information' : data[3],
                       'NickName':data2[0],
                       'ImageURL':data2[1]
                       }
                   com.append(t)
               data = cursor.fetchone()
       else:
           t = {
               'state' : False              # state 表示 是否成功                
               }
           com.append(t)          
        
        
       return jsonify(ans,com)
    except Exception as e:
	   # 如果发生错误则回滚
       print(e)
       connect.rollback()     
    connect.close()
    return 'product_information ProductID={}...'.format(ProductID)

#留言
@main.route("/product_comment", methods = ['GET','POST'])
def Productcomment():
    connect = pymysql.connect(host = Config.DB_HOST, user = Config.DB_USER
                          , password = Config.DB_PW, db = Config.DB_DB)
    cursor = connect.cursor()    
    
    if request.method == 'POST':

        ProductID =request.form.get('ProductID')
        UserID =request.form.get('UserID')
        Information = request.form.get('Information')
        if(not ProductID):
            t = {
                   'state' : False              # state 表示 是否成功 
                }
            return jsonify(t)
        if(not UserID):
            t = {
                   'state' : False              # state 表示 是否成功 
                }
            return jsonify(t)
        if(not Information):
            t = {
                   'state' : False              # state 表示 是否成功 
                }
            return jsonify(t)
              
        SQLIns = "SELECT * FROM product WHERE ProductID = {0}".format(ProductID)
        # 嘗試得到商品資料
        if(cursor.execute(SQLIns)):
            print("SQL success")
        else:
            t = {
                    'state' : False
                }
            return jsonify(t)
        data = cursor.fetchone()       
        if(data is None):
           t = {
               'state' : False              # state 表示 是否成功                
               }
           return jsonify(t)
       #確認有商品資料
        SQLIns ="INSERT INTO comment(TradeID, ProductID, Information, CommentDateTime,UserID) VALUES(NULL,{0},'{1}', '{2}', '{3}')".format( ProductID, Information, datetime.date.today(),UserID)
        #print("BBBBBBBBBBBBB")
        try:
            #print("AAAAAAAAAAAA")
            if(cursor.execute(SQLIns)):
                t = {
                        'state' : True
                        }
                #print("RRRRRRR")
                connect.commit()
            else:
                t = {
                        'state' : False
                    }
            return jsonify(t)
            
        except Exception as e:
    	   # 如果发生错误则回滚
           print(e)
           connect.rollback()     
    connect.close()
    return 'product_information'



#瀏覽紀錄
@main.route("/product_surfing_record", methods = ['GET','POST'])
def add_surfing_record():
    connect = pymysql.connect(host = Config.DB_HOST, user = Config.DB_USER
                          , password = Config.DB_PW, db = Config.DB_DB)
    cursor = connect.cursor()
    if request.method == 'POST':
        ProductID =request.form.get('ProductID')
        UserID =request.form.get('UserID')
        if(not ProductID):
            t = {
                   'state' : False              # state 表示 是否成功 
                }
            return jsonify(t)
        SQLIns ="UPDATE product\
                 SET SurfedTimes=SurfedTimes+1\
                 WHERE ProductID = {0}".format(ProductID)
        try:
            cursor.execute(SQLIns)
        except Exception as e:
	   # 如果发生错误则回滚
               print(e)
               connect.rollback()
        connect.commit()
        
        SQLIns = "SELECT *FROM surfedrecord WHERE UserID = {0} AND ProductID = {1}  ".format(UserID,ProductID)
        
        if(not UserID):
            
            return "visitor"
        
        else:
            try:
               # 商品資料
               if(not cursor.execute(SQLIns)):         #要是沒資料則進入  代表無此瀏覽資料
                   SQLIns = "SELECT * FROM product WHERE ProductID = {0}".format(ProductID)
                   if(cursor.execute(SQLIns)):         #有商品但無瀏覽資料
                       
                       data = cursor.fetchone()
                       if(data):
                           ProductName= data[2]
                           if(ProductName==None):
                               ProductName='NULL'
                               
                           ImageURL= data[3]
                           if(ImageURL==None):
                               ImageURL='NULL'
                               
                           Price= data[5]
                           if(Price=='None'):
                               Price='NULL'
                               
                           LowestPrice= data[6]
                           if(LowestPrice==None):
                               LowestPrice='NULL'
                               
                           BiddingPrice= data[7]
                           if(BiddingPrice==None):
                               BiddingPrice='NULL'
                               
                           BiddingUnitPrice= data[8]
                           if(BiddingUnitPrice==None):
                               BiddingUnitPrice='NULL'                                                          
                               
                           timenow=datetime.datetime.today().replace(microsecond=0)
                           dtime=datetime.datetime.today().replace(microsecond=0)+datetime.timedelta(days=20)
                           
                           BiddingDeadline= data[9]
                           if(BiddingDeadline==None):
                               BiddingDeadline='NULL'
                               SQLIns = "INSERT INTO surfedrecord (UserID, ProductID, ProductName,ImageURL,Price,LowestPrice,BiddingPrice,BiddingUnitPrice,BiddingDeadline,SurfingDate,TimeToLeaveDate)\
                                     VALUES ({0},{1},'{2}','{3}',{4},{5},{6},{7},{8},'{9}','{10}');".format(UserID,ProductID,ProductName,ImageURL,Price,LowestPrice,BiddingPrice,BiddingUnitPrice,BiddingDeadline,\
                                     timenow,dtime)
                           else:
                               SQLIns = "INSERT INTO surfedrecord (UserID, ProductID, ProductName,ImageURL,Price,LowestPrice,BiddingPrice,BiddingUnitPrice,BiddingDeadline,SurfingDate,TimeToLeaveDate)\
                                     VALUES ({0},{1},'{2}','{3}',{4},{5},{6},{7},'{8}','{9}','{10}');".format(UserID,ProductID,ProductName,ImageURL,Price,LowestPrice,BiddingPrice,BiddingUnitPrice,BiddingDeadline,\
                                     timenow,dtime)
                           
                           
                           #print(SQLIns)
                           if(not cursor.execute(SQLIns)):
                                print("failed C")
                                t = {
                                        'state' : False              # state 表示 是否成功 
                                    }
                           
                                return jsonify(t)
                           else:
                               connect.commit()
                               return "successfully insert surfing record"
                       else:
                           print("failed A")
                           t = {
                               'state' : False              # state 表示 是否成功 
                               }
                           
                           return jsonify(t)
                   else:                                    #表示無此商品
                       print("failed B")
                       t = {
                           'state' : False              # state 表示 是否成功 
                           }
                       return jsonify(t)
               else:                                   #有資料 則做更新
                   SQLIns = "SELECT * FROM product WHERE ProductID = {0}".format(ProductID)
                   
                   if(cursor.execute(SQLIns)):         
                       data = cursor.fetchone()
                       if(data):
                           
                                                      
                           ProductName= data[2]
                           if(ProductName==None):
                               ProductName='NULL'
                               
                           ImageURL= data[3]
                           if(ImageURL==None):
                               ImageURL='NULL'
                               
                           Price= data[5]
                           if(Price=='None'):
                               Price='NULL'
                               
                           LowestPrice= data[6]
                           if(LowestPrice==None):
                               LowestPrice='NULL'
                               
                           BiddingPrice= data[7]
                           if(BiddingPrice==None):
                               BiddingPrice='NULL'
                               
                           BiddingUnitPrice= data[8]
                           if(BiddingUnitPrice==None):
                               BiddingUnitPrice='NULL'
                               
                           BiddingDeadline= data[9]
                           if(BiddingDeadline==None):
                               BiddingDeadline='NULL'
                               SQLIns = "UPDATE surfedrecord\
                                    SET ProductName='{2}',ImageURL='{3}',Price={4},LowestPrice={5},BiddingPrice={6},BiddingUnitPrice={7},BiddingDeadline={8},SurfingDate='{9}',TimeToLeaveDate='{10}'\
                                    WHERE UserID={0} AND ProductID={1};".format(UserID,ProductID,ProductName,ImageURL,Price,LowestPrice,BiddingPrice,BiddingUnitPrice,BiddingDeadline,\
                                    datetime.datetime.today().replace(microsecond=0),datetime.datetime.today().replace(microsecond=0)+datetime.timedelta(days=20))
                           else:
                               SQLIns = "UPDATE surfedrecord\
                                    SET ProductName='{2}',ImageURL='{3}',Price={4},LowestPrice={5},BiddingPrice={6},BiddingUnitPrice={7},BiddingDeadline='{8}',SurfingDate='{9}',TimeToLeaveDate='{10}'\
                                    WHERE UserID={0} AND ProductID={1};".format(UserID,ProductID,ProductName,ImageURL,Price,LowestPrice,BiddingPrice,BiddingUnitPrice,BiddingDeadline,\
                                    datetime.datetime.today().replace(microsecond=0),datetime.datetime.today().replace(microsecond=0)+datetime.timedelta(days=20))
                           
                           
                           if(not cursor.execute(SQLIns)):
                                t = {
                                        'state' : False              # state 表示 是否成功 
                                    }
                           
                                return jsonify(t)
                       else:
                           t = {
                               'state' : False              # state 表示 是否成功 
                               }
                           
                           return jsonify(t)
                   else:                                    #表示無此商品
                       t = {
                           'state' : False              # state 表示 是否成功 
                           }
                       return jsonify(t)
                  
               
                           
                
                
               connect.commit() 
               return "surf data added."
            except Exception as e:
	   # 如果发生错误则回滚
               print(e)
               connect.rollback()     
    connect.close()
    return 'product_information'



    