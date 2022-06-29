from flask import Flask, request, render_template, jsonify
import requests
import os

from tensorflow.keras.models import load_model

import numpy as np
from PIL import Image
import base64
import io


app = Flask(__name__)

gender_dict = {
    "male": 1,
    "female": 0,
    "unknown": -1,
}


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/assess', methods=['GET', 'POST'])
def assess():
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
                bone_age_assessment_male_y='Assessment in Year (male): %d years, %d months' % (age_prediction_m//12, age_prediction_m%12),
                bone_age_assessment_female='Bone Age Assessment (female): %.2f months' % float(age_prediction_f),
                bone_age_assessment_female_y='Assessment in Year (female): %d years, %d months' % (age_prediction_f//12, age_prediction_f%12)
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


@app.route("/api/assess", methods=["GET", "POST"])
def assess_api():
    # get the POST data
    r = request.get_json(force=True)
    
    # get image
    try:
        file_path_or_url = r['files']['image']
    except KeyError:
        return jsonify({"error_message": "Wrong structure of the file object"})
    
    if os.path.isfile(file_path_or_url):
        image = Image.open(file_path_or_url)
    else:
        try:
            file_path_or_url = requests.get(file_path_or_url)
            image = Image.open(io.BytesIO(file_path_or_url.content))
        except:
            return jsonify({"error_message": "No image provided or invalid URL or Path"})
        
    image = image.resize((224, 224))
    image = image.convert('RGB')
    image = np.asarray(image) * 1.0/255
    image = np.expand_dims(image, axis=0)
    
    # load model
    model = load_model('model\PreTrained-256-256-G-64-conc-256-256_Bone-Age-MobileNetV2_bs-128_20_epochs.h5', compile=False)
    
    # get the gender info
    try:
        gender = r['gender']
    except:
        return jsonify({"error_message": "Please specify the gender"})
    if type(gender) != str or gender.lower() not in list(gender_dict.keys()):
        return jsonify({"error_message": "Please provide a proper gender data"})
    gender = gender_dict[gender]
    gender = np.array(gender)
    gender = np.expand_dims(gender, axis=0)
    
    if gender in [0, 1]:
        # if gender is specified
        age_prediction = model.predict([image, gender])[0][0]
        
        results = {
            "Filename": r['files']['image'].split('/')[-1],
            "Filepath": r['files']['image'],
            "Gender": f"{r['gender']}",
            "Bone Age Assessment": '%.2f months ' % float(age_prediction),
            "Assessment in Year": '%d years, %d months' % (age_prediction//12, age_prediction%12)
        }
        
        return jsonify(results)
    
    else:
        # return jsonify({"error_message": "Please provided gender information"})
        gender_m = np.expand_dims(1, axis=0)
        gender_f = np.expand_dims(0, axis=0)
        age_prediction_m = model.predict([image, gender_m])[0][0]
        age_prediction_f = model.predict([image, gender_f])[0][0]
        
        results = {
            "Filename": r['files']['image'].split('/')[-1],
            "Filepath": r['files']['image'],
            "Gender": f"{r['gender']}",
            "Bone Age Assessment (male)": '%.2f months ' % float(age_prediction_m),
            "Assessment in Year (male)": '%d years, %d months' % (age_prediction_m//12, age_prediction_m%12),
            "Bone Age Assessment (female)": '%.2f months ' % float(age_prediction_f),
            "Assessment in Year (female)": '%d years, %d months' % (age_prediction_f//12, age_prediction_f%12),
        }
        
        return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)