from flask import Flask,render_template,request,redirect,url_for
import requests
from flask_uploads import IMAGES, UploadSet, configure_uploads
import pathlib
import shutil
import os
# # API 的網域位址
url = 'http://35.206.206.144:8000/photo'
#error message
message={"DB_ConnectError":"錯誤:DB_ConnectError",
"Content_Unrecognizable":"錯誤:內容無法識別",
"Authorization_Error":"錯誤:授權好像停止了，請洽宏燁資訊業務詢問",
"AuthorizationIP_Error":"錯誤:IP未授權，請洽宏燁資訊業務詢問",
"FileTypes_Error":"錯誤:檔案不符合類型",
"Content_Nnrecognizable":"錯誤:檔案無法解析",
"API_connectError":"錯誤:連線異常，請洽宏燁資訊"}




# 起首式(flask 基本起首是)
app = Flask(__name__)
# Flask 拿到上傳檔案的起首式(flask_uploads起首式)
photos = UploadSet("photos", IMAGES)
app.config["UPLOADED_PHOTOS_DEST"] = "static/img"
app.config["SECRET_KEY"] = os.urandom(24)
configure_uploads(app, photos)

#在 Python 中獲取主目錄(D:\pyhton\VerificationCode)
a=pathlib.Path(__file__).parent.absolute()  


#執行上傳檔案頁面( upload.html)
@app.route('/')
def home():
    #刪除img中的檔案
    shutil.rmtree(f'{a}/static/img/')
    #建立img資料夾     
    os.mkdir(f'{a}/static/img/')           
    return render_template('upload.html')   # 執行 upload.html

@app.route("/return", methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':     #判斷若method=GET，此處用於當user點"再次上傳"時
        #刪除img中的檔案
        shutil.rmtree(f'{a}/static/img/')
        #建立img資料夾
        os.mkdir(f'{a}/static/img/')       
        return redirect(url_for("home"))    # 執行home function

    if request.method == 'POST'  and 'photo' in request.files and request.form['path'] != "":      #判斷若method=POST，此處用於使用者輸入完檔案路徑或選擇完檔案
        
        fileName = str(request.files['photo']).replace(">", "").replace("<","").replace("FileStorage: ","").replace("(", "").replace(")","").split("'")
        # 拿到上傳的檔案名稱
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
            if (answer in message.keys()) == True:
                answer = message[answer]
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
            if (answer in message.keys()) == True:
                answer = message[answer]
            return render_template('return.html',answer=answer)
    elif request.form['path'] == "":
        return redirect(url_for("home"))  
    
    


 
if __name__ == '__main__':
    app.run()