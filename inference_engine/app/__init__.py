from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json

from app.config import Config
from app.classifier import Classifier
from PIL import Image
import numpy as np
import io
import cv2
import base64

# fixed cudnn cant find conv function 
# seems to be an RTX gpu issue
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    CORS(app)

    classifier = Classifier()

    def predict(request_data):
        image_pil = Image.open(request_data)
        image_np = np.array(image_pil)
        image = cv2.resize(image_np, (224,224))
        image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
        image = np.expand_dims(image, axis=0)
        preds = classifier.predict(image)
        data = []

        for pred in preds:
            data.append({
                "prediction": pred[1],
                "probability": json.dumps(pred[2].astype(float))
            })

        return data

    def get_base64_image(image_file):
        img_str = str(base64.b64encode(image_file.read()))
        img_str = img_str.replace('b\'','', 1)
        img_str = img_str.replace('\'', '')
        return img_str


    @app.route('/')
    def index():
        return "Hello World!"

    @app.route('/load')
    def load_model():
        classifier.load()
        return "loaded", 200

    @app.route('/predict_result', methods=['POST'])
    def predict_result():

        image_file = request.files["image"]
        predictions = predict(image_file)

        return jsonify(predictions), 200

    @app.route('/predict_html', methods=['POST'])
    def predict_html():
        image_file = request.files["image"]
        image_str = get_base64_image(image_file)
        predictions = predict(image_file)

        return render_template('results.html', predictions=predictions, image=image_str)

    return app
