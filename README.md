# Bone Age Assessment with Flask
Deployment of Bone Age Assessment with Flask as web page and API

MobileNetV2 is used and implemented with Keras for the model and trained on [bone age regression kaggle](https://www.kaggle.com/c/bone-age-regression/data) train dataset with training-validation-test ratio of 8:1:1 for 20 epochs and batch size of 128. The test MAE is around 19.32

## How to Run
1. Create new folder and then go inside that folder and clone this repository
```
    git clone https://github.com/rinogrego/Bone-Age-Assessment-Deployment-with-Flask
```
2. Install virtual environment from the terminal in the same project directory
```
    pip install virtualenv
    python -m venv VIRTUALENV_NAME
```
3. Activate the virtual environment from terminal
```
    VIRTUALENV_NAME\scripts\activate
```
4. Go to the folder of the cloned repository and then install the packages required for the application
```
    cd Bone-Age-Assessment-Deployment-with-Flask
    pip install -r requirements.txt
```
5. From the terminal, run the following command to run the application
```
    python app.py
```
6. To see the website navigate to your localhost from the browser (url: http://localhost:5000)

## API
If you want to check how to access the API and see how to structure the data to send as POST request, open test_request_api.py. You can run the following command from the terminal to see the example result which will be printed in the terminal (need to run the above instruction until step 5 first).
```
    python test_request_api.py
```
By sending POST request to the given url:
```
POST /api/assess
```
With the following json structure:
```
{
    "files": {
        "image": "Local filepath or URL to the image"
    },
    "gender": "one category between 'unknown', 'male', or 'female'"
}
```
The example json responses are:
- if gender is unknown
```
{
    'Assessment in Year (female)': '8 years, 8 months', 
    'Assessment in Year (male)': '8 years, 9 months', 
    'Bone Age Assessment (female)': '104.86 months ', 
    'Bone Age Assessment (male)': '105.43 months ', 
    'Filename': '10000.png', 
    'Filepath': 'E:/Kuliah/Semester 6/Pemodelan/Week 4/data/img/10000.png', 
    'Gender': 'unknown'
}
```
- if gender is specified
```
{
    'Assessment in Year': '8 years, 9 months',
    'Bone Age Assessment': '105.43 months ',
    'Filename': '10000.png',
    'Filepath': 'E:/Kuliah/Semester 6/Pemodelan/Week 4/data/img/10000.png',
    'Gender': 'male'
}
```
- if the structure of the json object to the image path or url is incorrect
```
{
    "error_message": "Wrong structure of the file object"
}
```
- if the path or url to the image is invalid or the image not is not found
```
{
    "error_message": "No image provided or invalid URL or Path"
}
```
- if the gender is not specified
```
{
    "error_message": "Please specify the gender"
}
```
- if the gender is not a string or is not either 'male', 'female', or 'unknown'
```
{
    "error_message": "Please specify the gender"
}
```
