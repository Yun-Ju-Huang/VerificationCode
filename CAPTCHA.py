from flask import Flask,render_template,request,redirect,url_for
import requests
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

# # API 的網域位址
url = 'http://35.206.206.144:8000/photo'

@app.route('/')
def home():    
    return render_template('upload.html') 

@app.route('/return', methods=['GET', 'POST'])
def retu():
    
    if request.method == 'GET':
        return redirect(url_for("home"))
    path = request.form['path']
    if path == "":
        return redirect(url_for("home"))
    else:
        file_name = path.split('\\')[-1]
        file = open(path,'rb')
        files = {'file':(file_name, file, 'image/jpg/png')}
        asn = requests.post(url, files = files)
        print(path)
        print(asn.status_code)
        print(asn.text)
        answer =asn.text
        return render_template('return.html',answer=answer)
if __name__ == '__main__':
    app.run()