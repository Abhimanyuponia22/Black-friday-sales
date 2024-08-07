from flask import Flask,request
import pickle
import requests
import pandas as pd
app=Flask(__name__)
@app.route("/")
def root():
    return """
    <html>
    <body>
            <h1>Welcome to my Machine Learning Application</h1>
            <p>This is a machine learning application to predict the 
            test result of a hearing test based on age and physical score.</p>
            <form action="/predict" method="POST">
                <div>
                    <label>Gender</label>
                    <input type="number" name="Gender">
                </div>
                <div>
                    <label>Age</label>
                    <input type="number" name="Age" step="0.02">
                </div>
                  <div>
                    <label>Occupation</label>
                    <input type="number" name="Occupation">
                </div>
                <div>
                    <label>City_Category</label>
                    <input type="number" name="City_Category">
                </div>
                <div>
                    <label>Stay_in_current_years</label>
                    <input type="number" name="stay_in_current_years">
                </div>
                <div>
                    <label>Martial Status</label>
                    <input type="number" name="Martial_status">
                </div>
                <div>
                    <label>PC1</label>
                    <input type="number" name="PC1" step="0.02">
                </div>
                <div>
                    <label>PC2</label>
                    <input type="number" name="PC2" step="0.02">
                </div>
                <div>
                    <label>PC3</label>
                    <input type="number" name="PC3" step="0.02">
                    
                </div>
                
                
                <div>
                    <input type="submit" value="Predict">
                </div>
            </form>
        </body>
    </html>
    """


@app.route("/predict", methods=["POST"])
def predict():
    Gender=int(request.form["Gender"])
    age = float(request.form["Age"])
    occupation=int(request.form["Occupation"])
    City_category=int(request.form["City_Category"])
    stay_in_cr=int(request.form["stay_in_current_years"])
    martial_status=int(request.form["Martial_status"])
    pc1=float(request.form["PC1"])
    pc2=float(request.form["PC2"])
    pc3=float(request.form["PC3"])
    print(Gender)
    print(age)
    print(occupation)
    print(City_category)
    print(stay_in_cr)
    print(martial_status)
    print(pc1)
    print(pc2)
    print(pc3)
    # load the model from model.pkl file
    with open("my_pickles", "rb") as file:
        model = pickle.load(file)
    x=[Gender,age,occupation,City_category,stay_in_cr,martial_status,pc1,pc2,pc3]
    prediction = model.predict([x])
    print(prediction)

    return """

    <html>
    <body>
    <h1>Prediction result is</h1>
    <p>Based on your prediction of age and physical score is we have prediction </p>
    </body>
    </html>
    """
app.run(host="0.0.0.0",port=4003,debug=True)


