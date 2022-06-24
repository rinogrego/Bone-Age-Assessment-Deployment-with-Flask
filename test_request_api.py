import requests

url = 'http://localhost:5000/api/assess'
data = {
    "files": {
        # FILEPATH
        # "image": "E:/Kuliah/Semester 6/Pemodelan/Week 4/data/img/10000.png",
        "image": "https://storage.googleapis.com/kagglesdsdata/competitions/17699/846976/images/10000.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=databundle-worker-v2%40kaggle-161607.iam.gserviceaccount.com%2F20220624%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20220624T101700Z&X-Goog-Expires=345599&X-Goog-SignedHeaders=host&X-Goog-Signature=9d2da6eb67d9dfefe812b8b198ea380241fc22b1bb9757ecd03f687dd14fbc0eea179b90e538aca9b7481c0c341e9fbd5cf159860d89a6cb13d4f5c1bc37308c7f5dab2f646536da6f95fec39bdcdae6b6143c53d843495363a9186068afb700037da2b37abaedcd27680dc449c738d36d0fc360e0cacc687c39695e5d7e3f15935fdcf9b0cf0c71f46754c0f31a2a4a1e0924859532ea0b5aba5b86d1d6fb9fced7e0e900503a3f49e491badbdfb4191d1668e9989579dc438aad575370d49cfe34852fb69a33fb915305c363b80726cc6be0ecdb8fbd9c10f66e268d7f2c745e2aebed23921fbd83f5a2f3e4f1a226024ebe5829ee5d4b15fd4493efa8638e"
    },
    # GENDER OPTION: unknown/male/female. Unknown data will give results of each gender.
    "gender": "unknown"
}
r = requests.post(url, json=data)

print(r.json())