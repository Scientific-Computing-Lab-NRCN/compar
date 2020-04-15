import json
import os
import sys

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from flask_wtf.file import FileField
from wtforms import StringField, TextAreaField, BooleanField, SelectField
from wtforms.validators import InputRequired
from flask_bootstrap import Bootstrap
import subprocess
from flask import request, jsonify, send_file, Response, session
from flask import Flask, render_template
from datetime import datetime
import hashlib
import tempfile
import getpass


app = Flask(__name__)
app.config.from_object(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
Bootstrap(app)

SOURCE_FILE_DIRECTORY = tempfile.gettempdir()


class SingleFileForm(FlaskForm):
    slurm_parameters = TextAreaField('slurm_parameters', validators=[InputRequired()])
    save_combinations = BooleanField('save_combinations')
    compiler = SelectField('compiler', choices=[('icc', 'ICC'), ('gcc', 'GCC')])
    compiler_version = StringField('compiler_version')
    compiler_flags = TextAreaField('compiler_flags')
    source_file_code = TextAreaField('source_file_code')
    upload_file = FileField('upload_file', validators=[FileAllowed(['c'], 'c file only!')])  # valiation dont work
    result_file_area = TextAreaField('result_file_area')


@app.route("/")
@app.route("/singlefile", methods=['GET', 'POST'])
def single_file():
    form = SingleFileForm(request.form)
    return render_template('single-file-mode.html', form=form)


@app.route('/multiplefiles')
def multiple_files():
    return render_template('multiple-files-mode.html')


@app.route('/makefile')
def makefile():
    return render_template('makefile-mode.html')


def save_source_file(file_path, txt):
    with open(file_path, "w") as f:
        f.write(txt)


@app.route('/something/', methods=['post'])
def something():
    form = SingleFileForm(request.form)
    print(form.validate_on_submit())
    print(form.errors)
    if form.validate_on_submit():
        # handling upload file/paste code
        if form.source_file_code.data:
            try:
                if request.files and request.files['upload_file'].filename != "":
                    # special handling for uploaded files will be here
                    print("file test: ", request.files['upload_file'].filename)
                else:
                    pass
            except Exception as e:
                pass
            finally:
                guid = getpass.getuser() + str(datetime.now())
                file_hash = hashlib.sha3_256(guid.encode()).hexdigest()
                session['source_file_path'] = os.path.join(SOURCE_FILE_DIRECTORY, file_hash)
                save_source_file(file_path=session['source_file_path'], txt=form.source_file_code.data)
        return jsonify(data={'message': 'hello {}'.format(form.slurm_parameters.data)})
    return jsonify(errors=form.errors)


@app.route('/stream_progress')
def stream():
    # TODO: add check in the BE in case compar is ruuning do nothing
    def generate():
        compar_file = r"../program.py"
        compar_file = "testt.py"
        interpreter = sys.executable
        command = [interpreter, '-u', compar_file]
        proc = subprocess.Popen(" ".join(command), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in proc.stdout:
            yield line.rstrip() + b'\n'
        # TODO - Get the source file !
    return app.response_class(generate(), mimetype='text/plain')


@app.route('/result_file', methods=['get'])
def result_file():
    result_file_path = session['source_file_path']
    result_file_code = ''
    print(session)
    with open(result_file_path) as fp:
        result_file_code = fp.read()
    return jsonify({"text": result_file_code})


@app.route('/downloadResultFile', methods=['get'])
def download_result_file():
    with open(session['source_file_path'], 'r') as fp:
        result_code = fp.read()
    return Response(
        result_code,
        mimetype="text/plain",
        headers={"Content-disposition": "attachment; filename=Compar_results.c"})


if __name__ == "__main__":
    app.debug = True
    app.run(port=4444)
