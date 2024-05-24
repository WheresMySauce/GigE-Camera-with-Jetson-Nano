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
detect_model = YOLO('yolov8n.pt')  

# Load the pre-trained ResNet50V2 model
classify_model = ResNet50V2(
    include_top=True,
    weights="imagenet",
    input_tensor=None,
    input_shape=None,
    pooling=None,
    classes=1000,
    classifier_activation="softmax",
)

#------------------------------------------------------------------------------------------------------#



@app.route('/detect', methods=['POST'])
def detect():
    nparr = np.frombuffer(request.data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    print(img.shape)
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
    # Resize and preprocess image
    img_resized = cv2.resize(img, (224, 224))

    cv2.imwrite("saved_img", img_resized)
    img_array = np.expand_dims(img_resized, axis=0)
    img_array = preprocess_input(img_array)
    
    # Predict
    predictions = classify_model.predict(img_array)
    decoded_predictions = decode_predictions(predictions, top=1)[0]
    prediction = decoded_predictions[0][1]  # Get the label of the top prediction

    return jsonify({'prediction': prediction})


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0") 
