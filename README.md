## how to run the app
pip3 install -r requirements.txt
python3 app.py

please uncomment this line # nltk.download('stopwords') in MCQ.py
delete /nltk_data/corpora/stopwords/hinglish if there's related error

## milestones
ML: 
I. Translate Audio to Text ✅
II. Summarize Text ✅
III. Generate Questions from Text ✅
IV. Text Similarity 

SWE:
I. Skeleton of website ✅
II. Route functionalities correctly ✅
III. Beautify website ✅
IV. Connect to models
V. Upload Audio Files
VI. Pdf API

## Presentation
NLP challenge

## after adding requirements
pip freeze > requirements.txt    
pip3 freeze > requirements.txt   

git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch s2v_old/vectors' \
  --prune-empty --tag-name-filter cat -- --all

f88321d
  git rebase -i