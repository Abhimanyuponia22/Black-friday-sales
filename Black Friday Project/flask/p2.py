from flask import Flask, request, render_template_string
import pickle

app = Flask(__name__)

# HTML Templates
WELCOME_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to Prediction Zone</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(to right, #56ccf2, #2f80ed);
            color: #333;
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        .container {
            margin-top: 50px;
            flex: 1;
        }
        h1 {
            color: #fff;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }
        h2 {
            color: #fff;
            margin-top: 20px;
        }
        p.lead {
            background: rgba(255, 255, 255, 0.9);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            color: #333;
        }
        .btn-primary {
            background: #ff6f61;
            border: none;
            transition: background 0.3s ease;
        }
        .btn-primary:hover {
            background: #ff4a33;
        }
        footer {
            background: #333;
            color: #fff;
            padding: 20px 0;
            text-align: center;
            width: 100%;
        }
        .social-icons {
            margin-top: 10px;
        }
        .social-icons a {
            color: #fff;
            margin: 0 10px;
            font-size: 1.5em;
            transition: color 0.3s ease;
        }
        .social-icons a:hover {
            color: #ff6f61;
        }
    </style>
</head>
<body>
    <div class="container text-center my-5">
        <h1 class="display-4">Welcome to Prediction Zone</h1>
        <h2 class="mt-4">Black Friday Sales</h2>
        <p class="lead mt-4">Black Friday is an informal name for the Friday following Thanksgiving Day in the United States, celebrated on the fourth Thursday of November. The day after Thanksgiving has been regarded as the beginning of the U.S. Christmas shopping season since 1952. Although the term "Black Friday" did not become widely used until more recent decades, many stores offer highly promoted sales and open very early, such as at midnight or even on Thanksgiving itself.</p>
        <p class="lead">Our project aims to help retail stores or eCommerce businesses determine the optimal product prices based on historical sales data to maximize profits. By analyzing past data, our machine learning model can provide valuable insights for setting competitive prices during Black Friday sales.</p>
        <a class="btn btn-primary btn-lg mt-4" href="/predict-form" role="button">Start Prediction</a>
    </div>
    <footer class="footer">
        <p class="mb-0">Created by Abhimanyu</p>
        <div class="social-icons">
            <a href="https://www.facebook.com/abhimanyu.ponia.1/" target="_blank"><i class="fab fa-facebook-f"></i></a>
            <a href="https://www.twitter.com" target="_blank"><i class="fab fa-twitter"></i></a>
            <a href="https://www.linkedin.com/in/abhimanyu-ponia-952a4823a/" target="_blank"><i class="fab fa-linkedin-in"></i></a>
            <a href="https://github.com/Abhimanyuponia22" target="_blank"><i class="fab fa-github"></i></a>
        </div>
    </footer>
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.4/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    <script src="https://kit.fontawesome.com/a076d05399.js"></script>
</body>
</html>

"""

PREDICT_FORM = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prediction Form</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(to right, #56ccf2, #2f80ed);
            color: #333;
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }
        .container {
            background: rgba(255, 255, 255, 0.9);
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            margin-top: 50px;
            flex: 1;
        }
        h1 {
            color: #181717;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }
        .form-group label {
            font-weight: bold;
        }
        .btn-primary {
            background: #007bff;
            border: none;
            transition: background 0.3s ease;
        }
        .btn-primary:hover {
            background: #0056b3;
        }
        footer {
            background: #333;
            color: #fff;
            padding: 20px 0;
            text-align: center;
            width: 100%;
            margin-top: auto;
        }
        .social-icons {
            margin-top: 10px;
        }
        .social-icons a {
            color: #fff;
            margin: 0 10px;
            font-size: 1.5em;
            transition: color 0.3s ease;
        }
        .social-icons a:hover {
            color: #ff7e5f;
        }
    </style>
    <script src="https://kit.fontawesome.com/a076d05399.js" crossorigin="anonymous"></script>
</head>
<body>
    <div class="container my-5">
        <h1 class="display-4 text-center">Machine Learning Prediction Form</h1>
        <form action="/predict" method="POST">
            <div class="form-group">
                <label for="gender">Gender</label>
                <select class="form-control" name="Gender" id="gender">
                    <option value="">Select Gender</option>
                    <option value="1">Male</option>
                    <option value="0">Female</option>
                </select>
            </div>
            <div class="form-group">
                <label for="age">Age</label>
                <select class="form-control" name="Age" id="age">
                    <option value="">Select Age Range</option>
                    <option value="0">0-17</option>
                    <option value="1">18-25</option>
                    <option value="2">26-35</option>
                    <option value="3">36-45</option>
                    <option value="4">46-50</option>
                    <option value="5">51-55</option>
                    <option value="6">55+</option>
                </select>
            </div>
            <div class="form-group">
                <label for="occupation">Occupation</label>
                <input type="number" class="form-control" name="Occupation" id="occupation" min="0" max="20">
            </div>
            <div class="form-group">
                <label for="cityCategory">City Category</label>
                <select class="form-control" name="City_Category" id="cityCategory">
                    <option value="">Select City Category</option>
                    <option value="0">0</option>
                    <option value="1">1</option>
                    <option value="2">2</option>
                </select>
            </div>
            <div class="form-group">
                <label for="stayInCurrentYears">Stay in Current Years</label>
                <select class="form-control" name="stay_in_current_years" id="stayInCurrentYears">
                    <option value="">Select Years of Stay</option>
                    <option value="0">0</option>
                    <option value="1">1</option>
                    <option value="2">2</option>
                    <option value="3">3</option>
                    <option value="4">4+</option>
                </select>
            </div>
            <div class="form-group">
                <label for="martialStatus">Marital Status</label>
                <select class="form-control" name="Martial_status" id="martialStatus">
                    <option value="">Select Marital Status</option>
                    <option value="0">Unmarried</option>
                    <option value="1">Married</option>
                </select>
            </div>
            <div class="form-group">
                <label for="pc1">PC1</label>
                <input type="number" class="form-control" name="PC1" id="pc1" step="0.02" min="0" max="19">
            </div>
            <div class="form-group">
                <label for="pc2">PC2</label>
                <input type="number" class="form-control" name="PC2" id="pc2" step="0.02" min="0" max="17">
            </div>
            <div class="form-group">
                <label for="pc3">PC3</label>
                <input type="number" class="form-control" name="PC3" id="pc3" step="0.02" min="0" max="15">
            </div>
            <button type="submit" class="btn btn-primary">Predict</button>
        </form>
    </div>
    <footer class="footer bg-dark text-white text-center py-3">
        <p class="mb-0">Created by Abhimanyu</p>
        <div class="social-icons">
            <a href="https://www.facebook.com" target="_blank"><i class="fab fa-facebook-f"></i></a>
            <a href="https://www.twitter.com" target="_blank"><i class="fab fa-twitter"></i></a>
            <a href="https://www.linkedin.com" target="_blank"><i class="fab fa-linkedin-in"></i></a>
            <a href="https://www.github.com" target="_blank"><i class="fab fa-github"></i></a>
        </div>
    </footer>
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.4/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
"""

RESULT_PAGE = """
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prediction Result</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(to right, #56ccf2, #2f80ed);
            color: #333;
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }
        .container {
            background: rgba(255, 255, 255, 0.9);
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            margin-top: 50px;
            flex: 1;
        }
        h1 {
            color: #181717;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }
        .btn-primary {
            background: #007bff;
            border: none;
            transition: background 0.3s ease;
        }
        .btn-primary:hover {
            background: #0056b3;
        }
        footer {
            background: #333;
            color: #fff;
            padding: 20px 0;
            text-align: center;
            width: 100%;
            margin-top: auto;
        }
        .social-icons {
            margin-top: 10px;
        }
        .social-icons a {
            color: #fff;
            margin: 0 10px;
            font-size: 1.5em;
            transition: color 0.3s ease;
        }
        .social-icons a:hover {
            color: #ff7e5f;
        }
    </style>
    <script src="https://kit.fontawesome.com/a076d05399.js" crossorigin="anonymous"></script>
</head>
<body>
    <div class="container text-center my-5">
        <h1 class="display-4">Prediction Result</h1>
        <p class="lead">Based on your input, the prediction result is: <strong>{{ prediction }}</strong></p>
        <a class="btn btn-primary" href="/">Back to Home</a>
    </div>
    <footer class="footer bg-dark text-white text-center py-3">
        <p class="mb-0">Created by Abhimanyu</p>
        <div class="social-icons">
            <a href="https://www.facebook.com" target="_blank"><i class="fab fa-facebook-f"></i></a>
            <a href="https://www.twitter.com" target="_blank"><i class="fab fa-twitter"></i></a>
            <a href="https://www.linkedin.com" target="_blank"><i class="fab fa-linkedin-in"></i></a>
            <a href="https://www.github.com" target="_blank"><i class="fab fa-github"></i></a>
        </div>
    </footer>
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.4/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>

"""


@app.route("/")
def index():
    return render_template_string(WELCOME_PAGE)


@app.route("/predict-form")
def predict_form():
    return render_template_string(PREDICT_FORM)


@app.route("/predict", methods=["POST"])
def predict():
    Gender = int(request.form["Gender"])
    age = int(request.form["Age"])
    occupation = int(request.form["Occupation"])
    City_category = int(request.form["City_Category"])
    stay_in_cr = int(request.form["stay_in_current_years"])
    martial_status = int(request.form["Martial_status"])
    pc1 = float(request.form["PC1"])
    pc2 = float(request.form["PC2"])
    pc3 = float(request.form["PC3"])

    # Load the model from model.pkl file
    with open("my_pickles", "rb") as file:
        model = pickle.load(file)

    x = [Gender, age, occupation, City_category, stay_in_cr, martial_status, pc1, pc2, pc3]
    prediction = model.predict([x])

    return render_template_string(RESULT_PAGE, prediction=prediction[0])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4003, debug=True)
