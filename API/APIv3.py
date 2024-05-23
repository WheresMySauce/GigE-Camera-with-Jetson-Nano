from flask import Flask, request
import cv2
from ultralytics import YOLO
import numpy as np

app = Flask(__name__)
model = YOLO('yolov8n.pt')  # Load your YOLOv8 model

@app.route('/detect', methods=['POST'])
def detect():
    nparr = np.frombuffer(request.data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    results = model(img)
    res_plotted = results[0].plot() 
    _, img_encoded = cv2.imencode('.jpg', res_plotted)
    return img_encoded.tobytes()

if __name__ == '__main__':
    app.run(debug=True) 
