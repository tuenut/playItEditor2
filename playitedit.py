from flask import Flask, jsonify, request, abort, send_from_directory, render_template
from flask_cors import CORS
from logging import DEBUG

from os.path import basename, abspath
from backend.logger import make_logger
from backend.serializer import PlayItProject

app = Flask(__name__, static_folder='frontend/build/static', template_folder='frontend/build')
CORS(app)


@app.route('/')
def index():
    """Serve react SPA"""
    return render_template('index.html')

@app.route('/open')
def open_project():
    file_path = request.args.get('file')

    if file_path is None:
        abort(401)

    plt_proj = PlayItProject()

    try:
        plt_proj.load_project(abspath(file_path))
    except FileNotFoundError:
        abort(404)

    return jsonify(plt_proj.json())


if __name__ == '__main__':
    logger = make_logger(DEBUG)
    logger.log(DEBUG, '%s is started.' % basename(__file__))

    app.run(debug=True)

# todo: must run rest-api local server. flask?
# todo: rest-api need for open files, get json structure, receive json and save files.
# todo: I.e. that's interface between react in electron and backend.serializer.PlayItProject in python
