import speech_recognition as sr

def generate_transcript():
    r = sr.Recognizer()
    with sr.AudioFile('static/how2beatcancer.wav' ) as source:
        audio_text = r.listen(source)
        print('Converting audio transcripts into text ...')
        text = r.recognize_google(audio_text)
        return text
