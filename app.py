import os
from flask import Flask, send_file, request, render_template, jsonify, redirect, jsonify
from werkzeug.utils import secure_filename

from tensorflow.keras.models import load_model
from tensorflow.keras.losses import MeanAbsoluteError
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import numpy as np
from PIL import Image
import base64
import io


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        
        # get the image
        file = request.files["image"]
        try:
            image = Image.open(file.stream)
        except:
            return "No Image Provided"
        image = image.resize((224, 224))
        image = image.convert('RGB')
        image = np.asarray(image) * 1.0/255
        image = np.expand_dims(image, axis=0)
        
        # to display uploaded image
        file = request.files['image']
        img = Image.open(file.stream)
        img = img.resize((224, 224))
        img = img.convert('L')   # ie. convert to grayscale
        buffer = io.BytesIO()
        img.save(buffer, 'png')
        buffer.seek(0)
        img_data = buffer.read()
        img_data = base64.b64encode(img_data).decode()
        img_html = f'data:image/png;base64,{img_data}'
        
        # get the gender
        gender_dict = {
            "male": 1,
            "female": 0,
            "unknown": -1,
        }
        try:
            gender = request.form['gender']
        except:
            return "Please Specify the Gender"
        gender = gender_dict[gender]
        gender = np.array(gender)
        gender = np.expand_dims(gender, axis=0)
        
        # load model
        model = load_model('model\PreTrained-256-256-G-64-conc-256-256_Bone-Age-MobileNetV2_bs-128_20_epochs.h5', compile=False)
        
        if gender in [0, 1]:
            # if gender is specified
            age_prediction = model.predict([image, gender])[0][0]
            
        else:
            # if gender not specified
            gender_m = np.expand_dims(1, axis=0)
            gender_f = np.expand_dims(0, axis=0)
            age_prediction_m = model.predict([image, gender_m])[0][0]
            age_prediction_f = model.predict([image, gender_f])[0][0]
            
            return render_template(
                'index.html',
                image=img_html, 
                filename="Filename: {}".format(request.files["image"].filename),
                bone_age_assessment_male='Bone Age Assessment (male): %.2f months' % float(age_prediction_m),
                bone_age_assessment_male_y='Assessment in Year: %d years, %d months' % (age_prediction_m//12, age_prediction_m%12),
                bone_age_assessment_female='Bone Age Assessment (female): %.2f months' % float(age_prediction_f),
                bone_age_assessment_female_y='Assessment in Year: %d years, %d months' % (age_prediction_f//12, age_prediction_f%12)
            )
        
        return render_template(
            'index.html', 
            image=img_html, 
            filename="Filename: {}".format(request.files["image"].filename),
            gender="Gender: {}".format(request.form["gender"]),
            bone_age_assessment='Bone Age Assessment: %.2f months ' % float(age_prediction),
            bone_age_assessment_y='Assessment in Year: %d years, %d months' % (age_prediction//12, age_prediction%12)
        )
    
    return "Can only be accessed through POST request"

if __name__ == '__main__':
    app.run(debug=True)