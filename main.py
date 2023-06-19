from flask import Flask
import tensorflow as tf
from tensorflow.keras.models import load_model
from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import numpy as np
import cv2
import os

app = Flask(__name__)
# app.config['UPLOADED_IMAGES_DEST'] = 'media/images'
# app.config['UPLOAD_FOLDER'] = 'media'
model = load_model('MobileNetV3Small.h5')

def contrast_adjustment(img, alpha=1.2, beta=1):
    output = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
    return output

@app.route('/', methods=['GET', 'POST'])
def classify_disease():
   if request.method == 'POST':
      diseases_name = ['Acne', 'Acnetic Keratosis', 'Basal Cell Carcinoma', 'Capillaritis', 'Eczema', 'Folliculitis', 'Impetigo', 'Keloids', 'Lichen Planus', 'Orf', 'Psoriasis', 'Rosacea', 'Scabies', 'Skin Tag', 'Syphilis', 'Tuberous Sclerosis', 'Varicella', 'Vitiligo']

      try:
         file = request.files['imageFile1']
         file_name = secure_filename(file.filename)
         file.save(f'media/images/{file_name}')
      except:
         file = request.files['imageFile2']
         file_name = secure_filename(file.filename)
         file.save(f'media/images/{file_name}')

      img=cv2.imread(f'media/images/{file_name}')
      img=contrast_adjustment(img)
      resized_img=tf.image.resize(img, (224, 224))
      cv2.imwrite(os.path.join('media', 'images',file_name ), img)
      predictions=model.predict(np.expand_dims(resized_img, 0))
      idx = predictions.argmax()
      label = diseases_name[idx]
      return render_template('index.html', predictions=label, img=file_name)
   else:
      return render_template('index.html')

if __name__ == '__main__':

   app.run(host='127.0.0.1', port=5001, debug=True)