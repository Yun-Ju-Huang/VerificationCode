from flask import Flask,render_template
import requests
app = Flask(__name__)

# API 的網域位址
url = 'http://35.206.206.144:8000/photo'

# 需要解決的驗證碼圖片位址
file_path = "D:\github\VerificationCode\TestImage\JNG5V.png"
file_name = file_path.split('\\')[-1]
file = open(file_path,'rb')

# file_name = "123.txt"
# file = "123"
files = {'file':(file_name, file, 'image/jpg/png')}
r = requests.post(url, files = files)


print(r.status_code)
print(r.text)


@app.route("/")
def hello():
    return "Hello, World!"

# # @app.route('/user/<name>')
# # def user(name):
# #     return render_template('home.html',name = name)

# @app.route('/home')
# def user():
#     return render_template('home.html')

# if __name__ == '__main__':
#     app.run()