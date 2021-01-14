from flask import Flask
from flask import jsonify, render_template, request, abort
from Page2.app import app
from Utill import util1, util2
from werkzeug.utils import secure_filename
import os

client = Flask(__name__, static_folder="Client_static", template_folder="Client_templates")
client.register_blueprint(app, url_prefix="/app")
client.config['MAX_CONTENT_LENGTH'] = 1024 * 50
client.config['UPLOAD_PATH'] = r'Data/File to send'


@client.route("/main", methods=['GET', 'POST'])
@client.route("/", methods=['GET', 'POST'])
def main_page():
    return render_template("client.html")


@client.route('/get_data', methods=['GET'])
def get_data():
    response = jsonify(util1.get_data_for_page())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@client.route('/predict_data', methods=['POST'])
def predict_form():
    arr_from_client = request.json
    final_arr = util1.dummy_str_var(arr_from_client["data"])
    response = jsonify({'estimate_val': util1.predict_val(final_arr)})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


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
            return jsonify({'redirect': "app/predict_csv_result"})
        util2.delete_file()
        return jsonify({'error': var})


if __name__ == '__main__':
    client.config['TEMPLATES_AUTO_RELOAD'] = True
    util1.load_file()
    client.run(host='0.0.0.0', port='300')
