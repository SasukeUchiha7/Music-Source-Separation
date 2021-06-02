from flask import Flask, render_template, url_for, request



app = Flask(__name__)  




def _loadSongs():
    return 'songName'

# routes -------------

@app.route('/', methods = ["POST","GET"])
def home():
    if request.method =="POST":
        pass
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

# functions-----------------

def separateAudio():
    pass

if __name__ == '__main__':
    app.run(debug=True) 
