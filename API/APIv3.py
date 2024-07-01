from flask import Flask, request, jsonify

import cv2
import numpy as np
import base64
## Image processing
from ultralytics import YOLO
from PIL import Image
from transformers import pipeline
## LLM
import os
from langchain_community.vectorstores import FAISS
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

## Define LLMs model
os.environ["NVIDIA_API_KEY"] = "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"
vector_db_path = "langchain/vectorstores/db_faiss"
embedder = NVIDIAEmbeddings(model="NV-Embed-QA")
vectorstore = FAISS.load_local(vector_db_path, embedder, allow_dangerous_deserialization=True)
retriever = vectorstore.as_retriever()
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Answer solely based on the following context:\n<Documents>\n{context}\n</Documents>Just go straight to the point, don't mention about the documents. Don't make up an answer if you don't know. Try to summarize the idea into one paragraph",
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

detect_model = YOLO('API/yolov8_hlabel400.pt')  
class_definition = {
    "A":"Perfect weld bead with small or no surface defects.",
    "B":"The weld bead has been disrupted by appearing of several surface defectsthan class A.",
    "C":"Weld bead created but the welding line has been disrupted continuously by appearing of more surface defects than class B.",
    "D":"Not creating a weld or burn through."
}
app = Flask(__name__)
#------------------------------------------------------------------------------------------------------#
### Define model
# Load your YOLOv8 model

class_dict = detect_model.names
print(class_dict)
# Load the pre-trained VIT model

pipe = pipeline("image-classification", model="th041/vit-weldclassifyv2")
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
        question = f"What is Corrective Action for {', '.join(unique_cls[:-1])}, and {unique_cls[-1]}?"
        response = chain.invoke(question)
    elif len(unique_cls) == 1:
        question = f"What is Corrective Action for {unique_cls[0]}?"
        response = chain.invoke(question)
    else:
        response = "No defect detected!!!"
    res_plotted = results[0].plot(conf=False, line_width=2) 
    _, img_encoded = cv2.imencode('.jpg', res_plotted)
    img_base64 = base64.b64encode(img_encoded).decode('utf-8')
    print(response)
    return jsonify({'advice': response, 'image': img_base64})


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
    final_result = best_result['label']
    output = f"{final_result} - {class_definition[final_result]}"
    return jsonify({'prediction': output})

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
    if num_edges > 7700 and num_edges<8700:
        return jsonify({'weld_check': "Warning: No weld bead detected"})
    else:
        return jsonify({'weld_check': "Weld bead detected"})
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0") 
