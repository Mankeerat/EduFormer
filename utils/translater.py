# def generate_transcript(
#     # audio
# ):
#     # audio --model-> text 
#     text = "demo transcript"
#     return text


import speech_recognition as sr

def generate_transcript():
    r = sr.Recognizer()
    with sr.AudioFile('static/how2beatcancer.mp3' ) as source:
        audio_text = r.listen(source)
        text = r.recognize_google(audio_text)
        print('Converting audio transcripts into text ...')
        print(text)
        return text
