from flask import Flask, render_template, request, jsonify
from flask_cors import cross_origin
from sklearn.preprocessing import StandardScaler
import os
import yaml
import joblib
import numpy as np


params_path = 'params.yaml'
webapp_root = 'webapp'

static_dir = os.path.join(webapp_root, "static")
template_dir = os.path.join(webapp_root, "templates")

app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)


def read_params(config_path):

    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


def predict(data):

    config = read_params(params_path)
    model_dir_path = config['webapp_model_dir']
    model = joblib.load(model_dir_path)
    # print(model.predict([[321.0, 111.0, 3.0, 3.5, 4.0, 8.83, 1]]))

    scaler = StandardScaler()
    data = scaler.fit_transform(data)

    prediction = model.predict(data)
    return prediction


def api_response(response):
    try:
        data = np.array([list(request.json.value())])
        response = predict(data)
        response = {'response': response}
        return response
    except Exception as e:
        print(e)
        error = {"error": "something went wrong"}
        return error


@app.route('/', methods=['GET', 'POST'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")


@app.route('/predict', methods=['GET', 'POST'])
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            if request.form:
                data = dict(request.form)
                if data['research'] == 'yes':
                    data['research'] = 1
                else:
                    data['research'] = 0
                data = data.values()
                data = [list(map(float, data))]
                print(data)
                response = predict(data)
                return render_template('result.html', response=response)
            elif request.json:
                response = api_response(request)
                return jsonify(response)

        except Exception as e:
            print(e)
            error = {"error:": "Something went wromg"}
            return render_template('404.html', error=error)
    else:
        return render_template('index.html')


port = int(os.getenv("PORT"))

if __name__ == "__main__":
    # app.run(host='127.0.0.1', port=8001, debug=True)
    #app.run(debug=True) # running the app
    app.run(host='0.0.0.0', port=port)
