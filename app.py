import os
from flask import Flask, render_template, url_for, request, flash, redirect, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER= "static/uploads"
ALLOWED_EXT = { 'wav', 'aac'}

app = Flask(__name__)  
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.add_url_rule(
    "/uploads/<name>", endpoint="download_file", build_only=True
)

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT


# routes -------------
@app.route('/')
def home():
    return render_template('index.html', songs=[])

@app.route('/upload',methods = ["POST","GET"])
def upload():
    # if request.method == 'POST':
    #   f = request.files['file']
    #   f.save(secure_filename(f.filename))
    #   return 'file uploaded successfully'
    if request.method =="POST":
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('download_file', name=filename))
            source = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            return render_template('index.html', source = source)

@app.route('/about')
def about():
    return render_template('about.html')

# functions -----------------

def loadUploadFile():
    return ''''''

def separateAudio():
    pass

if __name__ == '__main__':
    app.run(debug=True) 
