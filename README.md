## How to Run the App
pip3 install -r requirements.txt
python3 app.py

please uncomment this line "# nltk.download('stopwords')" in MCQ.py before running
Delete /nltk_data/corpora/stopwords/hinglish if there's related error

## Project
This project takes advantage of two major areas of computing, Audio Digital Signal Processing and Natural Language Processing techniques. 
Firstly, we have a problem with all class recordings weather be it a lecture, a group discussion, need to pass around mics to every student etc. This can be eliminated by using an array of mics and beamforming. Beamforming is a digital signal processing technique in where we can capture sounds from specific ‘soiund zones’ and ignore it in others while recording on a an array of microphones. 
In this project we used the Delay and Sum beamformer. Sound comes from a source, reaching the n number of microphones in the array at different times. Thus by eliminating this delay in our combined soundtrack, and summing it up, we receive the sound coming from that source in this flower lobe pattern with the main lobe focussing on the source of the sound and eliminating other sounds.
 This eliminates the need to hear through a mic and in a recording would allow us to listen to sound from multiple areas ignoring the noise making it the perfect first audio setup for the nlp pipeline. This high quality, low SNR sound would work better with the already existing nlp summarization techniques and also better help us label the sound sources as well. 

This sound data is then pipelined into a sound to text model (google API) generating a transcript of the clear sound recording above through the beamformer. One can also use youtube videos/wav files to input the file or type in the text transcription to make use of the summarization and question generation part of the system. As known for summarizing long documents, the transformer approach ‘T5’ using attention which had quadratic space and time complexity making the system very slow depending on the amount of input text, ex. 
In a 1 hour lecture, the text would be very large making the system very slow with using the transformer method. Thus we have leveraged an algorithm ‘HEPOS’, published last year, which allows us to do all the computing in real time, making the system very user friendly. 

In addition to leveraging google api, T5 transformer and the HEPOS algorithm, for aiding students know if the prof mentioned that something could be an exam or if something is important, getting to know the context of the text is very important. We have then used nlp semantic analysis and semantic comparison techniques. 
We compare our text ‘using similar techniques as the quora duplicate question challenge’ to a book/ past recording or lectures/ past review notes to pin point the crucial questions and topics one has to know and generate our summary based of the results from these analysis. We have found that we can summarize the normal text to 30% of its size and retain all the important information in the summary. The summary is then pipelined into the next step which deals with Q&A generation. 

## Webpage
The main webpage is built with Flask. It integrates transcription, summary, and question generation. 
To use the app, first choose to upload an audio file or record the audio in live.
Then click on the "Convert the Text" to translate the audio file to texts, after which you are able to "Generate Summary and Questions".
Two models can be used for Question Generation -- Wordnet and Sense2Vec, generated questions would be hidden first and could be revealed using the "Show/Hide Answers" button.

## Important Note and Future work
Beamformer and file upload are not completely integrated at current stage


## Screenshots
![Features]https://github.com/Mankeerat/EduFormer/blob/main/static/features.png(?raw=true)
![Pipeline]https://github.com/Mankeerat/EduFormer/blob/main/static/pipeline.png(?raw=true)
![App]https://github.com/Mankeerat/EduFormer/blob/main/static/App_screenshot.png(?raw=true)

## VIDEO:
https://youtu.be/nIUoRQCT6so