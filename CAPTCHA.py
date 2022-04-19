from flask import Flask,render_template,request,redirect,url_for
import requests
from flask_uploads import IMAGES, UploadSet, configure_uploads
import pathlib
import shutil
import os
# # API 的網域位址
url = 'http://35.206.206.144:8000/photo'


# 起首式(flask 基本起首是)
app = Flask(__name__)
# Flask 拿到上傳檔案的起首式(flask_uploads起首式)
photos = UploadSet("photos", IMAGES)
app.config["UPLOADED_PHOTOS_DEST"] = "static/img"
app.config["SECRET_KEY"] = os.urandom(24)
configure_uploads(app, photos)

#在 Python 中獲取主目錄(D:\pyhton\VerificationCode)
a=pathlib.Path(__file__).parent.absolute()  


#執行上傳檔案頁面
@app.route('/')
def home():
    shutil.rmtree(f'{a}/static/img/')#刪除img中的檔案
    os.mkdir(f'{a}/static/img/')   #建立img資料夾        
    return render_template('upload.html') 

@app.route("/return", methods=['GET', 'POST'])
def upload():
    if request.method == 'GET': 
        shutil.rmtree(f'{a}/static/img/')#刪除img中的檔案
        os.mkdir(f'{a}/static/img/')   #建立img資料夾    
        return redirect(url_for("home"))    
    if request.method == 'POST'  and 'photo' in request.files and request.form['path'] != "":      
        fileName = str(request.files['photo']).replace(">", "").replace("<","").replace("FileStorage: ","").replace("(", "").replace(")","").split("'")
        fileName = str(fileName[1])        
        # print(fileName)
        if fileName == "":
            path = request.form['path']
            # print(path)            
            file_name = path.split('\\')[-1]
            file = open(path,'rb')
            files = {'file':(file_name, file, 'image/jpg/png')}
            asn = requests.post(url, files = files)
            # print(path)
            print(asn.status_code)
            print(asn.text)
            answer =asn.text
            return render_template('return.html',answer=answer)
        else:
            photos.save(request.files['photo'])
          
            file_path = (f'{a}/static/img/{fileName}').replace("\\","/")
            file_name = file_path.split('/')[-1]
            # print(file_name)
            file = open(file_path,'rb')
            files = {'file':(file_name, file, 'image/jpg/png')}
            r = requests.post(url, files = files)
            print(r.status_code)
            print(r.text)            
            answer = r.text
            return render_template('return.html',answer=answer)
    elif request.form['path'] == "":
        return redirect(url_for("home"))  
    
    



# 
if __name__ == '__main__':
    app.run(debug="True")