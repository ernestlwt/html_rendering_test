from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np

class Classifier(object):
    def __init__(self):
        self.model = ResNet50(weights='imagenet')

    def predict(self, image):
        x = preprocess_input(image)
        preds = self.model.predict(image)

        return decode_predictions(preds, top=3)[0]