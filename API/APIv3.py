from flask import Flask, request, jsonify

import cv2
import numpy as np

from ultralytics import YOLO
import tensorflow as tf
from tensorflow.keras.applications.resnet_v2 import ResNet50V2, preprocess_input, decode_predictions



app = Flask(__name__)
#------------------------------------------------------------------------------------------------------#
### Define model

# Load your YOLOv8 model
detect_model = YOLO('best.pt')  

# Load the pre-trained ResNet50V2 model
classify_model = tf.keras.models.load_model('resnet_ABC.keras')
class_names = ['AB','C','D']

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
    # Resize and preprocess image
    img_resized = cv2.resize(img, (224, 224))

    cv2.imwrite("saved_img.jpg", img_resized)
    img_array = np.expand_dims(img_resized, axis=0)
    img_array = preprocess_input(img_array)
    
    # Predictx
    predictions = classify_model.predict(img_array)
    # decoded_predictions = decode_predictions(predictions, top=1)[0]
    # prediction = decoded_predictions[0][1]  # Get the label of the top prediction
    class_id = np.argmax(predictions, axis = 1)
    class_name = class_names[class_id.item()]

    return jsonify({'prediction': class_name})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0") 
