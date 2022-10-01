from flask import Flask, render_template, request
from utils.summarizer import generate_summary
from utils.MCQ import generate_questions
from utils.translater import generate_transcript

app = Flask(__name__)

record = False
transcript = ""
questions = []
summary = ""

@app.route('/')
def index():
    global transcript
    global questions
    global summary
    transcript = ""
    questions = []
    summary = ""
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

@app.route('/transcript', methods=['GET','POST'])
def translate():
    # if request.method == "POST":
    global transcript 
    transcript = generate_transcript(
        # audio
    )
    return render()

@app.route('/questions', methods=['GET','POST'])
def generateQuestions():
    # if request.method == "POST":
    global questions
    questions = generate_questions(
        # text
    )
    return render()


@app.route('/summary', methods=['GET','POST'])
def summarize():
    # if request.method == "POST":
    global summary 
    summary = generate_summary(
        # text
    )
    return render()

def render():
    return render_template('index.html', transcript=transcript, summary = summary, questions=questions)

if __name__ == '__main__':
    app.debug = True
    app.run()