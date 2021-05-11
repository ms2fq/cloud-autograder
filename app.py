from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import subprocess, os
app = Flask(__name__)

@app.route('/')
def make_sure_alive():
    return "hello -- I am ALIVE!!!"

@app.route('/upload')
def upload_file():
    return render_template('welcome.html') + render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        ret = 'Results of running ' + secure_filename(f.filename) + ' on the Autograder'
        num_correct = 0
        if secure_filename(f.filename) == "add.py":
            num_correct = subprocess.call("./execute_add_py_submission.sh", shell=True)
        elif secure_filename(f.filename) == "subtract.py":
            num_correct = subprocess.call("./execute_subtract_py_submission.sh", shell=True)
        score = str(num_correct)
        res = []
        with open(secure_filename(f.filename), 'r') as fs:
            res = fs.readlines()
        process = subprocess.call(["rm", secure_filename(f.filename)])
        return render_template("results.html", fname=secure_filename(f.filename), grade=score, lines=res, length=len(res))

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0')

