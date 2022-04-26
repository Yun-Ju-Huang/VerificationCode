from xml.etree.ElementInclude import include
from flask import Flask, flash,render_template,request,redirect,url_for,send_file
import requests
from flask_uploads import IMAGES, UploadSet, configure_uploads
import pathlib
import os
from datetime import datetime
import time
import captcha_TwoCaptcha


#error message
message={"DB_ConnectError":"錯誤:DB_ConnectError",
"Content_Unrecognizable":"錯誤:內容無法識別",
"Authorization_Error":"錯誤:授權好像停止了，請洽宏燁資訊業務詢問",
"AuthorizationIP_Error":"錯誤:IP未授權，請洽宏燁資訊業務詢問",
"FileTypes_Error":"錯誤:檔案不符合類型",
"Content_Nnrecognizable":"錯誤:檔案無法解析",
"API_connectError":"錯誤:連線異常，請洽宏燁資訊",
"Error":"錯誤:請確認圖片內容"}

#在 Python 中獲取主目錄(例如: D:\pyhton\VerificationCode)
a=pathlib.Path(__file__).parent.absolute()  

file_types = ["png", "jpg", "jpeg"]
log_time = datetime.now().strftime('%Y%m%d')
log_name = log_time + "_log.csv"
log_path = f'{a}/Log/' + log_name
download_path = f'{a}/Picture'
response_error = ""
response_code = ""
error_Message = "NULL"



# 起首式(flask 基本起首是)
app = Flask(__name__)
# Flask 拿到上傳檔案的起首式(flask_uploads起首式)
photos = UploadSet("photos", IMAGES)
app.config["UPLOADED_PHOTOS_DEST"] = "static/img"
app.config["SECRET_KEY"] = os.urandom(24)
configure_uploads(app, photos)


# 執行上傳檔案頁面( upload.html)
@app.route('/')
def home():    
    return render_template('upload.html')  # 執行 upload.html

# 執行回傳頁面(return.html)
@app.route("/return", methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':  # 判斷若method=GET，此處用於當user點"再次上傳"時        
        return redirect(url_for("home"))  # 執行home function
    if request.method == 'POST' and request.files['photo'] != "":       # 判斷若method=POST，此處用於使用者輸入完檔案路徑或選擇完檔案
        fileName = str(request.files['photo']).replace(">", "").replace("<", "").replace("FileStorage: ", "").replace("(", "").replace(")", "").split("'")
        # 拿到上傳的檔案名稱
        fileName = str(fileName[1])
        # print(fileName)
        png = ".png" in fileName
        jpg = ".jpg" in fileName
        jpeg =".jpeg"in fileName
        if (png == False) and (jpg == False) and (jpeg == False) and fileName != "":
            flash("※請確認上傳圖片格式※")
            return redirect(url_for("home"))
        elif fileName == "":            
            flash("※請重新選擇上傳圖片※")
            return redirect(url_for("home"))
        else :
            filename = time.strftime('%Y%m%d%H%M%S', time.localtime())+request.files['photo'].filename            
            file_paths = os.path.join(download_path, filename)
            request.files['photo'].save(file_paths)
            file_path = (file_paths).replace("/", "\\")
            file_name = file_path.split('\\')[-1]      
            file = open(file_path, 'rb')
            files = {'file': (file_name, file, 'image/jpg/png')}
            r =captcha_TwoCaptcha.get_captcha(files)            
            print(r)
            answer = r
            if (answer in message.keys()) == True:
                answer = message[answer]
            return render_template('return.html', answer=answer)  # 執行 return.html
    elif request.files['photo'] == "":
        return redirect(url_for("home"))

# @app.route('/dl')
# def upload_form():
#     return render_template('Download.html')

# @app.route('/download')
# def download_file():
# 	#path = "html2pdf.pdf"
# 	#path = "info.xlsx"
# 	path = f'{a}/download/TableauDesktop-64bit-2021-4-6.exe'
# 	#path = "sample.txt"
# 	return send_file(path, as_attachment=True)
   


if __name__ == "__main__":
    #Run flask起首式 給host 與 port 
    app.run(host="0.0.0.0", port=80)




