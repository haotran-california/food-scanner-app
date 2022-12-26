from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
from PIL import Image
from keras.models import load_model
import tensorflow as tf
import numpy as np
import os 

class_names = ['apple','banana','beetroot','bell pepper','cabbage','capsicum','carrot',
 'cauliflower','chilli pepper','corn','cucumber','eggplant','garlic','ginger','grapes',
 'jalepeno','kiwi','lemon','lettuce','mango','onion','orange','paprika','pear','peas',
 'pineapple','pomegranate','potato','raddish','soy beans','spinach','sweetcorn',
 'sweetpotato','tomato','turnip','watermelon']

app = Flask(__name__)
CORS(app)

@app.route("/")
def index(): 
	return "Hello world"

@app.route("/predict", methods=["POST"])
def predict():
    
    rawImage = request.files["file"]
    pil_image = Image.open(rawImage)
    pil_image.save("./images/current.jpg")
    
    imagePath = "./images/current.jpg"
    image = tf.keras.utils.load_img(imagePath, target_size=(64,64))
    rawInputArr = tf.keras.preprocessing.image.img_to_array(image)
    inputArr = np.array([rawInputArr])

    model = load_model("./model/trainedModel.h5")
    outputArray = model.predict(inputArr)
    resultIndex = np.where(outputArray[0] == max(outputArray[0]))

    prediction = class_names[resultIndex[0][0]]
    
    return jsonify(prediction) 
