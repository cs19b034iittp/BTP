import tensorflow as tf
from keras.preprocessing import image
import numpy as np
from tensorflow.keras.utils import load_img, img_to_array
model = tf.keras.models.load_model('model.h5')
def predict_image( image_path):
    # Load the saved model

    # Load the image to be predicted
    img = load_img(image_path, target_size=(224, 224))
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = x / 255.0

    # Make the prediction
    prediction = model.predict(x)

    # Print the result
    if prediction < 0.5:
        return "Chem"
    else:
       return "Non-chem"
