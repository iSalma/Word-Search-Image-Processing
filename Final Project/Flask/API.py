import FinalDetector
from flask import Flask
from flask import request
import base64
import cv2

app = Flask(__name__)
@app.route('/postJsonHandler', methods = ['POST'])
def postJsonHandler():
    print("POST")
    content = request.form['name']
    imgdata = base64.b64decode(content)

    toFind = request.form['word']

    with open("imageToSave.png", "wb") as fh:
        fh.write(imgdata)

    x=cv2.imread("imageToSave.png")
    y=cv2.imread("fir.png")
    sora=FinalDetector.detectWord(x, toFind)
    cv2.imwrite("detected.png",sora)


    with open("detected.png", "rb") as fin:
        str = base64.b64encode(fin.read())
    return 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=='

@app.route('/get', methods = ['GET'])
def get():
    print("ok")
    return( "GET")
app.run(host='0.0.0.0', port= 5000)
