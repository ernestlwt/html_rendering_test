from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np

class Classifier(object):
    def __init__(self):
        self.model = ResNet50(weights='imagenet')

    def load(self):
        img_path = 'app/elephant.jpg'
        img = image.load_img(img_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        preds = self.model.predict(x)

    def predict(self, image):
        x = preprocess_input(image)
        preds = self.model.predict(image)

        return decode_predictions(preds, top=3)[0]