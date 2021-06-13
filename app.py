import os
from flask import Flask, render_template, url_for, request, flash, redirect, send_from_directory
from werkzeug.utils import secure_filename
from separation import separateMusic
import glob

base_dir = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER= "static/uploads"
SAMPLE_FOLDER= "static/samples"
OUTPUT_FOLDER= "static/sounds"
ALLOWED_EXT = { 'wav', 'aac'}

app = Flask(__name__)  
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SAMPLE_FOLDER'] = SAMPLE_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

songs = os.listdir(app.config['SAMPLE_FOLDER'])
app.add_url_rule(
    "/uploads/<name>", endpoint="download_file", build_only=True
)

mainSource ='' ## sourcefilepath

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT


# routes -------------
@app.route('/') ## home--------------------------------
def home():
    global mainSource
    mainSource=''
    delete_all()
    return render_template('index.html', songs=songs)

@app.route('/uploads/<name>') ##uploaded_file uri---------------------------
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route('/upload',methods = ["POST","GET"]) #### upload-------------------------------
def upload(): 
    if request.method =="POST":
        if 'file' not in request.files:
            flash('No file part','danger')
            return render_template('index.html', songs=songs)
        file = request.files['file']
        print("uploaded file: ",file)
        if file.filename == '':
            flash('No selected file','danger')
            return render_template('index.html', songs=songs)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('download_file', name=filename))
            source = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            global mainSource
            mainSource=''+source
            print("uploaded mainsrc:",mainSource)
            flash("Loaded...",'info')
            return render_template('index.html', source = source)
        else: 
            flash("Wrong Format",'danger')
            return render_template('index.html', songs=songs)


@app.route('/select', methods=['GET', 'POST'])  ## route for sample select
def selected():
    selectedSource = request.args.get('select-song')
    if (selectedSource==None):
        flash("Please select from the given samples or upload a wav file!",'warning')
        return render_template('index.html', songs=songs)
    print("selected song:",selectedSource)
    src=os.path.join(app.config['SAMPLE_FOLDER'],selectedSource)
    global mainSource
    mainSource =''+src
    print("selected mainsrc:",mainSource)
    flash("Loaded...",'info')
    return render_template('index.html', source = src)


@app.route('/predict', methods=['POST','GET']) ## separate -------------------------
def separateAudio():
    print("separating mainsrc:",mainSource)
    if(mainSource==''):
        print("empty----------------------------------------------")
        flash("Empty File!!!!!",'danger')
        return render_template('index.html', songs=songs)
    else:
        separateMusic(mainSource)
        audios = os.listdir(app.config['OUTPUT_FOLDER'])
        output = []
        for a in audios: output.append(app.config['OUTPUT_FOLDER']+'/'+a)
        flash('Successfull!', 'success')
        return render_template('index.html', audios=output, source = mainSource)

    

@app.route('/about') ### about page---------------------------------
def about():
    return render_template('about.html')

def delete_all():
    folder = glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], '*.wav'))
    print("folder:", folder)
    test = 'test3.wav'
    for f in folder:
        if(f == os.path.join(app.config['UPLOAD_FOLDER'], test) ):
            continue
        else: os.remove(f)


if __name__ == '__main__':
    app.run(threaded=True,port=5000) 
