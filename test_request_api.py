import requests

url = 'http://localhost:5000/api/assess'
data = {
    "files": {
        # FILEPATH
        "image": "E:/Kuliah/Semester 6/Pemodelan/Week 4/data/img/10000.png"
    },
    "gender": "unknown"
}
r = requests.post(url, json=data)

print(r.json())