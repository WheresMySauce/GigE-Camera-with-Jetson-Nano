from flask import Flask, request, jsonify

import cv2
import numpy as np
## Image processing
from ultralytics import YOLO
from PIL import Image
from transformers import pipeline




app = Flask(__name__)
#------------------------------------------------------------------------------------------------------#
### Define model

# Load your YOLOv8 model
detect_model = YOLO('best.pt')  

# Load the pre-trained VIT model
pipe = pipeline("image-classification", model="th041/vit-weld-classify")
#------------------------------------------------------------------------------------------------------#
@app.route('/detect', methods=['POST'])
def detect():
    nparr = np.frombuffer(request.data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # print(img.shape)
    results = detect_model(img)
    res_plotted = results[0].plot() 
    _, img_encoded = cv2.imencode('.jpg', res_plotted)
    return img_encoded.tobytes()


@app.route('/classify', methods=['POST'])
def classify():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Read image file string data
    nparr = np.frombuffer(file.read(), np.uint8)
    # Convert numpy array to image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(img)

    # Predict
    results = pipe(pil_image)
    best_result = max(results, key=lambda x: x['score'])
    return jsonify({'prediction': best_result['label']})

@app.route('/weld_check', methods=['POST'])
def weld_check():
    file = request.files['file']
    nparr = np.frombuffer(file.read(), np.uint8)
    # Convert numpy array to image
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Perform edge detection
    edges = cv2.Canny(blurred, 50, 150)

    # Analyze edges
    num_edges = np.sum(edges > 0)
    print(num_edges)
    if num_edges > 5000:
        return jsonify({'weld_check': "Weld bead detected"})
    else:
        return jsonify({'weld_check': "Warning: No weld bead detected"})
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0") 
