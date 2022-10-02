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
mock_data = """Maintaining good health doesn't happen by accident. It requires work, smart lifestyle choices, and the occasional checkup and test.
A healthy diet is rich in fiber, whole grains, fresh fruits and vegetables, "good" or unsaturated fats, and omega-3 fatty acids. These dietary components turn down inflammation, which can damage tissue, joints, artery walls, and organs. Going easy on processed foods is another element of healthy eating. Sweets, foods made with highly refined grains, and sugar-sweetened beverages can cause spikes in blood sugar that can lead to early hunger. High blood sugar is linked to the development of diabetes, obesity, heart disease, and even dementia.
The Mediterranean diet meets all of the criteria for good health, and there is convincing evidence that it is effective at warding off heart attack, stroke, and premature death. The diet is rich in olive oil, fruits, vegetables, nuts and fish; low in red meats or processed meats; and includes a moderate amount of cheese and wine.
Physical activity is also necessary for good health. It can greatly reduce your risk of heart disease, stroke, type 2 diabetes, breast and colon cancer, depression, and falls. Physical activity improves sleep, endurance, and even sex. Aim for 150 minutes of moderate-intensity exercise every week, such as brisk walking. Strength training, important for balance, bone health, controlling blood sugar, and mobility, is recommended 2-3 times per week.
Finding ways to reduce stress is another strategy that can help you stay healthy, given the connection between stress and a variety of disorders. There are many ways to bust stress. Try, meditation, mindfulness, yoga, playing on weekends, and taking vacations.
Finally, establish a good relationship with a primary care physician. If something happens to your health, a physician you know —and who knows you — is in the best position to help. He or she will also recommend tests to check for hidden cancer or other conditions."""

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

@app.route('/summary', methods=['GET','POST'])
def summarize():
    # if request.method == "POST":
    global summary 
    summary = generate_summary(
        rawdocs=transcript
    )
    return render()

def render():
    return render_template('index.html', transcript=transcript, summary=summary, questions=questions)

if __name__ == '__main__':
    app.debug = True
    app.run()

