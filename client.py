from flask import Flask
from flask import jsonify, render_template, request, abort, url_for
from Page2.app import app
from Utill import util1, util2
from werkzeug.utils import secure_filename
import os

'''
It is a flask API that is use to predict whether person subscribe to
bank or not. All the main function and working present in Util module
File System of this API
Banking ML/
    | -- Client_static
    | -- Client_templates
    | -- client.py
    | -- /app
        | -- App_static
        | -- App_templates
        | -- __init__.py
        | -- app.py
app.py is basically for second page, which is use to show predicted value of 
csv
'''

client = Flask(__name__, static_folder="Client_static", template_folder="Client_templates")
client.register_blueprint(app, url_prefix="/app")
client.config['MAX_CONTENT_LENGTH'] = 1024 * 50
client.config['UPLOAD_PATH'] = r'Data/File to send'


# this function return main page of website
@client.route("/main", methods=['GET', 'POST'])
@client.route("/", methods=['GET', 'POST'])
def main_page():
    return render_template("client.html")


# this function return option for select tag in main webpage
@client.route('/get_data', methods=['GET'])
def get_data():
    response = jsonify(util1.get_data_for_page())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


# it predict data given by form
@client.route('/predict_data', methods=['POST'])
def predict_form():
    arr_from_client = request.json
    final_arr = util1.dummy_str_var(arr_from_client["data"])
    response = jsonify({'estimate_val': util1.predict_val(final_arr)})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


# it is use to predict data given in csv file
@client.route('/predict_csv', methods=['POST'])
def predict_csv():
    csv_file = request.files.get("file")
    file_name = csv_file.filename

    filename = secure_filename(file_name)
    file_ext = os.path.splitext(filename)[1]
    if file_ext not in ['.xlsx', '.csv']:
        abort(400)
    else:
        csv_file.save(os.path.join(client.config['UPLOAD_PATH'], filename))
        var = util2.get_file(file_name)
        if var is None:
            util2.df_transform()
            util2.predict_file()
            util2.save_file()
            return jsonify({'redirect': url_for("app.display_result")})
        util2.delete_file()
        return jsonify({'error': var})


if __name__ == '__main__':
    client.config['TEMPLATES_AUTO_RELOAD'] = True
    util1.load_file()
    client.run(host='0.0.0.0', port='300', debug=True)
