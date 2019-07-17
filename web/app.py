#app

from flask import Flask, request
import pandas as pd
import pickle
import sklearn
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
    
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        df = pd.DataFrame.from_records(request.json, index=[0])
        cylinders = pd.DataFrame([[0, 0, 0,0,0,0,0,0]], columns = ['10 cylinders', '12 cylinders', '3 cylinders','4 cylinders', '5 cylinders', '6 cylinders', '8 cylinders', 'other'])
        oMax = 10000000
        oMin = 0
        aMax = 103
        aMin = 0
        
        ageN = (df['age']) * 1/(aMax-aMin)
        odometerN = (df['odometer']) * (1/oMax-oMin)
        cyl = df['cylinders'].values[0]
        for i in cylinders.columns:
            if i == cyl:
                cylinders[i][0] = 1
                      
        data = pd.concat((odometerN, ageN, cylinders), axis=1)   
        pred = car_pricing_model.predict(data)
        pred = pd.Series(pred, name='Predicted_Price')
        pred = pd.concat((df['odometer'], df['age'], df['cylinders'], pred), axis=1)
   
        return(str(pred))   

@app.before_first_request
def load_model():
    global car_pricing_model
    with open('car_pricing_model', 'rb') as handle:
        car_pricing_model = (pickle.load(handle))


@app.route('/get_example/<some_input>', methods=['GET'])
def get_example(some_input):
    if request.method == 'GET':
        return('You supplied the following input: ' +str(some_input))