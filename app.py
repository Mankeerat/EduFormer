from flask import Flask, render_template, request
from utils.translater import generate_transcript
from utils.generators import generate_summary_questions
import speech_recognition as sr


app = Flask(__name__)

record = False
transcript = ""
questions = []
summary = ""
model = "Wordnet"

@app.route('/home')
def home():
    return render_template("firstpage.html")

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
    return render_template('index.html')

@app.route('/analysis')
def ananlyze():
    return render_template('analysis.html')

@app.route('/transcript')
def translate():
    global transcript 
    transcript = generate_transcript(
        # audio
    )
    return render()

@app.route('/summary_questions')
def generateQuestions():
    global questions
    global summary
    questions, summary = generate_summary_questions(
        context = transcript,
        modelopt = model
    )
    return render()

@app.route('/changeModel', methods = ['POST'])
def changeModel():
    global model
    model = request.form['model']
    return render()

def render():
    return render_template('index.html', transcript=transcript, summary=summary, questions=questions)

if __name__ == '__main__':
    app.debug = True
    app.run()

