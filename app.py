import pandas as pd
from flask import Flask, jsonify, request
from functions import translate_all_languages

# app
app = Flask(__name__)

# routes
@app.route('/', methods=['POST'])



def predict():
    # get data
    data = request.get_json(force=True)
    print("data recieved")

    dataset=[]

    for i in data:
        dataset.append(data[i])
    print(dataset[0])

    from LanguageIdentifier import predict
    language= predict(dataset[0])

    data_dict={}
    data_dict= translate_all_languages(language, dataset[1], dataset[:-1])

    print(data_dict[dataset[1]])
    
    file = open("/home/jatin26/ab-inbev/output.txt", "a")
    file.write(data_dict[dataset[1]][0])
    file.close()
    # return data
    return jsonify(results= data_dict)

if __name__ == '__main__':
    app.run(port = 6000, debug=True)

