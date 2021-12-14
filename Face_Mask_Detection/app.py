# -*- coding: utf-8 -*-
"""


@author: vedashri
"""

from flask import Flask, render_template, Response,request
from werkzeug.utils import secure_filename
from camera1 import VideoCamera
from imgdect import get_img
import cv2
#from detect import pre_dect
import os
import sqlite3 as sql

app = Flask(__name__)
UPLOAD_FOLDER = '.\\imgssave'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/a')
def index():
    return render_template('Home.html')

@app.route('/image', methods=['POST','GET'])
def image():
    return render_template('image.html')

def img_gen():
    while True:
        frame=cv2.imread('./static/detectedimgs/img_3.jpg')
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame=jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
@app.route('/img_feed')
def img_feed():
    return Response(img_gen(),mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/showimage',methods= ['GET', 'POST'])    
def showimage():
    if request.method == 'POST':
        try:
            for imgs in os.listdir('./imgssave/'):
                f='./imgssave/'+imgs
                os.remove(f)
        except :
            pass
        image = request.files['myfile']
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        get_img()
        
        return render_template('imageshow.html')
    return render_template('image.html')

@app.route('/vedio')
def vedio():
    return render_template('vedio.html')



@app.route('/')
def getDB():
    global rows
    con = sql.connect('Mask_db.db')
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM Mask_Camera")

    rows = cur.fetchall();

    return render_template('vedio.html', rows = rows)
   # return rows


@app.route("/savedetails",methods = ["POST","GET"])  
def saveDetails():  
    msg = "msg"  
    if request.method == "POST":  
        try:  
            url_name = request.form["url_name"]  
            camname = request.form["camname"]  
            id = request.form["id"]
            with sql.connect('Mask_db.db') as con:  
           # con = sql.connect('Mask_db.db')
              cur = con.cursor()  
              cur.execute("INSERT INTO Mask_Camera(id,cam_url,cam_name) VALUES (?,?,?)",(id,url_name,camname))  
              con.commit()  
              msg = "Url and Camera Name successfully Added"  
            
        except:  
            con.rollback()  
            msg = "We can not add the url and camera name to the list"  
        finally:  
            return render_template("success.html",msg = msg)  
            con.close()  
    return render_template('Add_Url.html')


@app.route("/deleterecord",methods = ["POST","GET"])  
def deleterecord():  
   # id = request.form["id"]  
    with sql.connect("Mask_db.db") as con:  
        
        try: 
            con.row_factory = sql.Row 
            cur = con.cursor()  
           # cur.execute("delete from Mask_Camera where id ?",id) 
            cur.execute("SELECT * FROM Mask_Camera")

            rows = cur.fetchall();

            if request.method == 'POST': 
              
        #test = request.form.getlist('mycheckbox')
              for getid in request.form.getlist('mycheckbox'):
                  print(getid)
                  cur.execute('DELETE FROM Mask_Camera WHERE id = {0}'.format(getid)) 
                  con.commit()
            msg = "record successfully deleted" 
            
        except:  
            msg = "can't be deleted"  
        finally:  
            return render_template("delete_selector.html",rows=rows, msg=msg)  
    return render_template("delete_record.html",msg=msg,rows=rows)  
 
def ved_gen(camera):
    
    
    camera.update(0)


    while True:
        #get camera frame
        
        frame = camera.get_frame()
	
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


	

@app.route('/video_feed')
def video_feed():
    return Response(ved_gen(VideoCamera()),mimetype='multipart/x-mixed-replace; boundary=frame')


def ved(cam):
    return cam.me


@app.route('/technology')
def tech():
    return Response(ved(VideoCamera()),mimetype='multipart/x-mixed-replace; boundary=frame')






@app.route('/')
def getCamera():
    con = sql.connect('Mask_db.db')
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM Mask_Camera")

    rows = cur.fetchall();

    return render_template('vedio.html', rows = rows)


if __name__ == '__main__':
    #app.run(debug=True,port='5000')
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port) # host="0.0.0.0" instead of debug=True