from flask import Flask, render_template, request
from summarizer import summarize
from MCQ import MCQ
from translater import translate

app = Flask(__name__)
record = False

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/record', methods=['GET','POST'])
def record():
    record != record
    # if (record==True){

    # }else{

    # }
    return render_template('index.html')

@app.route('/analysis')
def ananlyze():
    # analysis = sommething
    return render_template('analysis.html')

@app.route('/translate', methods=['GET','POST'])
def translate():
    if request.method == "POST":
        print("debug endpoint/n")
        transcript = translate()
        return render_template('index.html')

@app.route('/generateQuestions', methods=['GET','POST'])
def generateQuestions():
    if request.method == "POST":
        print("debug endpoint/n")
        questions = MCQ()
        return render_template('index.html')


@app.route('/summarize', methods=['GET','POST'])
def summarize():
    if request.method == "POST":
        print("debug endpoint/n")
        summary = summarize()
        return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run()