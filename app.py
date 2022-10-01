from flask import Flask, render_template, request
import summarizer, MCQ, translater

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['GET','POST'])
def summarize(text):
    if METHOD == "POST":
        summarized_text = summarizer(text)
        return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run()