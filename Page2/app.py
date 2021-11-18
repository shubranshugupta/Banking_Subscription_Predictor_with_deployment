from flask import send_from_directory, abort, render_template, Blueprint, current_app, jsonify, url_for
from Utill import util2

app = Blueprint("app", __name__, static_folder='App_static', template_folder='App_templates')


# this function return base html page
@app.route('/get_base_html', methods=['GET'])
def display_result():
    return render_template("page2.html")


# this function return predicted csv in html table format
@app.route('/get_table', methods=['GET'])
def display_table():
    return util2.return_table()


# it is use to send file that is used to downloaded
@app.route('/download_file', methods=['POST'])
def download_csv():
    try:
        filename = util2.return_filename()
        return send_from_directory(current_app.config['UPLOAD_PATH'], filename, mimetype="text/csv", as_attachment=True)
    except (FileNotFoundError, NameError):
        return abort(404)


# it is use to delete unwanted file from Data folder
@app.route('/delete_file', methods=['GET'])
def delete_file():
    util2.delete_file()
    return jsonify({'redirect': url_for("main_page")})
