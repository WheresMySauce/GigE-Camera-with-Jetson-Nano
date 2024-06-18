from flask import Flask, request, jsonify

import cv2
import numpy as np
## Image processing
from ultralytics import YOLO
from PIL import Image
from transformers import pipeline
## LLM
import os
from langchain.vectorstores import FAISS
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

## Define LLMs model
os.environ["NVIDIA_API_KEY"] = "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"
vector_db_path = "vectorstores/db_faiss"
embedder = NVIDIAEmbeddings(model="NV-Embed-QA")
vectorstore = FAISS.load_local(vector_db_path, embedder, allow_dangerous_deserialization=True)
retriever = vectorstore.as_retriever()
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Answer solely based on the following context:\n<Documents>\n{context}\n</Documents>Just go straight to the point, don't mention about the documents. Don't make up an answer if you don't know",
        ),
        ("user", "{question}"),
    ]
)
model = ChatNVIDIA(model="meta/llama3-70b-instruct", temperature=0.1)
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)


app = Flask(__name__)
#------------------------------------------------------------------------------------------------------#
### Define model
# Load your YOLOv8 model
detect_model = YOLO('best.pt')  
class_dict = detect_model.names
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
    cls_name = []
    for c in results[0].boxes.cls:
        cls_name.append(class_dict[int(c)])
    unique_cls = list(set(cls_name))
    if len(unique_cls) > 1:
        question = f"What is the corrective action for {', '.join(unique_cls[:-1])}, and {unique_cls[-1]}?"
    else:
        question = f"What is the corrective action for {unique_cls[0]}?"
    response = chain.invoke(question)
    res_plotted = results[0].plot() 
    _, img_encoded = cv2.imencode('.jpg', res_plotted)
    return img_encoded.tobytes(), jsonify({'advice': response})


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
