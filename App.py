import time
import cv2
import os
from flask import Flask, render_template, Response

app = Flask(__name__)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen():
    while(1):
        cap = cv2.VideoCapture(os.path.abspath('assets/movie.avi'))
        stop = False
        while(cap.isOpened() and stop == False):
            ret, img = cap.read()
            if ret == True:
                img = cv2.resize(img, (0,0), fx=0.5, fy=0.5) 
                frame = cv2.imencode('.jpg', img)[1].tobytes()
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                time.sleep(0.01)
            else:
                stop = True

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')
