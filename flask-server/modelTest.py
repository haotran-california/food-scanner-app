from keras.models import load_model
import numpy as np
import tensorflow as tf

class_names = ['apple',
 'banana',
 'beetroot',
 'bell pepper',
 'cabbage',
 'capsicum',
 'carrot',
 'cauliflower',
 'chilli pepper',
 'corn',
 'cucumber',
 'eggplant',
 'garlic',
 'ginger',
 'grapes',
 'jalepeno',
 'kiwi',
 'lemon',
 'lettuce',
 'mango',
 'onion',
 'orange',
 'paprika',
 'pear',
 'peas',
 'pineapple',
 'pomegranate',
 'potato',
 'raddish',
 'soy beans',
 'spinach',
 'sweetcorn',
 'sweetpotato',
 'tomato',
 'turnip',
 'watermelon']

imgPath = "./images/banana.jpg"
bananaImage = tf.keras.preprocessing.image.load_img(imgPath, target_size=(64, 64))
input_arr = tf.keras.preprocessing.image.img_to_array(bananaImage)
input_arr = np.array([input_arr])

model = load_model("./model/trainedModel.h5")
output = model.predict(input_arr)
result_index = np.where(output[0] == max(output[0]))

prediction = class_names[result_index[0][0]]
print(prediction)



