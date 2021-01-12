from flask import send_from_directory, abort, render_template, Blueprint, current_app, jsonify
from Utill import util2

app = Blueprint("app", __name__, static_folder='App_static', template_folder='App_templates')


@app.route('/predict_csv_result', methods=['GET'])
def display_result():
    try:
        util2.return_table()
        return render_template("page2.html")
    except:
        return abort(404)


@app.route('/get_table', methods=['GET'])
def display_table():
    return util2.return_table()


@app.route('/download_file', methods=['POST'])
def download_csv():
    try:
        filename = util2.return_filename()
        return send_from_directory(current_app.config['UPLOAD_PATH'], filename, mimetype="text/csv", as_attachment=True)
    except (FileNotFoundError, NameError):
        return abort(404)


@app.route('/delete_file', methods=['GET'])
def delete_file():
    util2.delete_file()
    return jsonify({'redirect': "/"})
