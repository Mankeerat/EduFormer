# def generate_transcript(
#     # audio
# ):
#     # audio --model-> text 
#     text = "demo transcript"
#     return text


import speech_recognition as sr

def generate_transcript():
    r = sr.Recognizer()
    with sr.AudioFile('static/how2beatcancer.wav' ) as source:
        print('Converting audio transcripts into text ...')
        audio_text = r.listen(source)
        text = r.recognize_google(audio_text)
        return text
