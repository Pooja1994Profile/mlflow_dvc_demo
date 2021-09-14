from flask import Flask, render_template, request, jsonify
from flask_cors import cross_origin
import os
import yaml
import joblib
import numpy as np
from prediction_service import prediction

webapp_root = 'webapp'

static_dir = os.path.join(webapp_root, "static")
template_dir = os.path.join(webapp_root, "templates")

app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)


@app.route('/', methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")


@app.route('/predict', methods=['GET', 'POST'])
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            if request.form:
                data_req = dict(request.form)
                if data_req['research'] == 'yes':
                    data_req['research'] = 1
                else:
                    data_req['research'] = 0
                response = prediction.form_response(data_req)
                return render_template('result.html', response=response)
            elif request.json:
                response = prediction.api_response(request)
                return jsonify(response)

        except Exception as e:
            print(e)
            error = {"error": e}
            return render_template("404.html", error=error)
    else:
        return render_template('index.html')


port = int(os.getenv("PORT"))

if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
    #app.run(debug=True) # running the app
    app.run(host='0.0.0.0', port=port)
