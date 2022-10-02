from flask import Flask, render_template, request
from utils.summarizer import generate_summary
from utils.MCQ import generate_questions
from utils.translater import generate_transcript
import speech_recognition as sr
# from utils.model import summarizer

app = Flask(__name__)

record = False
transcript = ""
questions = []
summary = ""

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

@app.route('/summary')
def summarize():
    global summary 
    summary = generate_summary(
        rawdocs=transcript
    )
    return render()

@app.route('/questions')
def generateQuestions():
    global questions
    questions = generate_questions(
        context = transcript
    )
    return render()

def render():
    return render_template('index.html', transcript=transcript, summary=summary, questions=questions)

if __name__ == '__main__':
    app.debug = True
    app.run()

