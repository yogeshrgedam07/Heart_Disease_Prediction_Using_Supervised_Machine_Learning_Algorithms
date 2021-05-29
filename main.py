from flask import  Flask, render_template, request
from database import loginCheck, signupCheck
import numpy as np
import pandas as pd
import joblib


app = Flask(__name__)

#---------------------------------------------Homepage------------------------------------------------------------------


@app.route('/')
def index():
    return render_template('index.html')

#---------------------------------------------Disease Prediction Model--------------------------------------------------

def getParameters():
    parameters = []
    parameters.append(request.form['age'])
    parameters.append(request.form['sex'])
    parameters.append(request.form['cp'])
    parameters.append(request.form['trestbps'])
    parameters.append(request.form['chol'])
    parameters.append(request.form['fbs'])
    parameters.append(request.form['restecg'])
    parameters.append(request.form['thalach'])
    parameters.append(request.form['exang'])
    parameters.append(request.form['oldpeak'])
    parameters.append(request.form['slope'])
    parameters.append(request.form['ca'])
    parameters.append(request.form['thal'])
    return parameters

@app.route('/predict',methods=['POST'])
def predict():
    #load Models
    model = open('modelsvc.pkl','rb')
    model2 = open('modeldt.pkl', 'rb')
    model3 = open('model1.pkl', 'rb')
    model4 = open('modelkn.pkl', 'rb')
    model5 = open('modelnb.pkl', 'rb')

    #Set Classifier
    clfr = joblib.load(model)
    clfr2 = joblib.load(model2)
    clfr3 = joblib.load(model3)
    clfr4 = joblib.load(model4)
    clfr5 = joblib.load(model5)


    if request.method == 'POST':
        #input Parameters
        parameters = getParameters()
        inputFeature = np.asarray(parameters).reshape(1,-1)


        prediction1 = int(clfr.predict(inputFeature))
        my_prediction2 = clfr2.predict(inputFeature)
        my_prediction3 = clfr3.predict(inputFeature)
        my_prediction4 = clfr4.predict(inputFeature)
        my_prediction5 = clfr5.predict(inputFeature)




        prediction2 = int(my_prediction2[0])
        prediction3 = int(my_prediction3[0])
        prediction4 = int(my_prediction4[0])
        prediction5 = int(my_prediction5[0])


        predictans = [prediction1,prediction2,prediction3,prediction4, prediction5]

        yes  = 0
        no = 0
        if int(predictans[0]) == 1:
            mess = 1
            yes = yes  + 1
        else:
            mess = 0
            no = no +1
    #----------------------------------#
        if int(predictans[1]) == 1:
            mess1 = 1
            yes = yes + 1
        else:
            mess1 = 0
            no = no + 1
    #----------------------------------#

        if int(predictans[2]) == 1:
            mess2 = 1
            yes = yes + 1
        else:
            mess2 = 0
            no = no + 1
    #----------------------------------#

        if int(predictans[3]) == 1:
            mess3 = 1
            yes = yes + 1
        else:
            mess3 = 0
            no = no + 1
    #----------------------------------#

        if int(predictans[4]) == 1:
            mess4 = 1
            yes = yes + 1
        else:
            mess4 = 0
            no = no + 1
    # ----------------------------------#

        return render_template('chart.html', mess = mess, mess1 = mess1, mess2 = mess2, mess3 = mess3, mess4 = mess4,yes = (yes * 20), no= (no * 20) , predictans = predictans)

#-----------------------------------------Check Login-------------------------------------------------------------------


@app.route('/checkLogin', methods=['POST', 'GET'])
def checkLogin():
    if request.method == 'POST':
        user = request.form.get('uname')
        passw = request.form.get('upass')

        if loginCheck(user, passw) == True:
            message = 'Welcome'
            return render_template('userhome.html', message = message, name = user)

        else:
            message = 'Login Failed'
            return render_template('status.html', message = message, name = user)

#--------------------------------------------New Registration-----------------------------------------------------------


@app.route('/signupReg', methods=['POST', 'GET'])
def signupReg():
    if request.method == 'POST':
        user = request.form.get('uname1')
        pass1 = request.form.get('upass1')
        pass2 = request.form.get('upass2')

        if pass1 != pass2:
            message = 'Password Does not match'
            return render_template('status.html', message = message, name = user)
        else:
            if signupCheck(user, pass1) == True:
                message = 'Signup Successful'
            else:
                message = 'Signup Failed'
            return render_template('status.html', message=message, name = user)



#----------------------------------------------Run Project--------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug = True)