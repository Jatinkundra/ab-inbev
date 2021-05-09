import pandas as pd
from flask import Flask, jsonify, request
import pickle

# load model
# model = pickle.load(open('model.pkl','rb'))

# app
app = Flask(__name__)

# routes
@app.route('/', methods=['POST'])



def predict():
    # get data
    data = request.get_json(force=True)

    dataset=[]

    for i in x:
        dataset.append(x[i])
    # convert data into dataframe
    # data.update((x, [y]) for x, y in data.items())
    # data_df = pd.DataFrame.from_dict(data)

    # predictions
    # result = model.predict(data_df)

    # send back to browser 
    
    # output = {'results': int(result[0])}

    data= dataset.to_dict()

    # return data
    return jsonify(results= data)

if __name__ == '__main__':
    app.run(port = 5000, debug=True)

