from heapq import nlargest
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation

text = """Much of an executive’s workday is spent asking others for information—requesting status updates from a team leader, for example, or questioning a counterpart in a tense negotiation. Yet unlike professionals such as litigators, journalists, and doctors, who are taught how to ask questions as an essential part of their training, few executives think of questioning as a skill that can be honed—or consider how their own answers to questions could make conversations more productive.

That’s a missed opportunity. Questioning is a uniquely powerful tool for unlocking value in organizations: It spurs learning and the exchange of ideas, it fuels innovation and performance improvement, it builds rapport and trust among team members. And it can mitigate business risk by uncovering unforeseen pitfalls and hazards.

For some people, questioning comes easily. Their natural inquisitiveness, emotional intelligence, and ability to read people put the ideal question on the tip of their tongue. But most of us don’t ask enough questions, nor do we pose our inquiries in an optimal way.

The good news is that by asking questions, we naturally improve our emotional intelligence, which in turn makes us better questioners—a virtuous cycle. In this article, we draw on insights from behavioral science research to explore how the way we frame questions and choose to answer our counterparts can influence the outcome of conversations. We offer guidance for choosing the best type, tone, sequence, and framing of questions and for deciding what and how much information to share to reap the most benefit from our interactions, not just for ourselves but for our organizations."""

def  summarizer(rawdocs):
    stopwords = list(STOP_WORDS)

    nlp = spacy.load('en_core_web_trf')
    doc = nlp(rawdocs)
    tokens = [token.text for token in doc]
    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text] += 1


    max_freq = max(word_freq.values())

    for word in word_freq.keys():
        word_freq[word] = word_freq[word]/max_freq

    sent_tokens = [sent for sent in doc.sents]

    sent_scores = {}

    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]
                else:
                    sent_scores[sent] += word_freq[word.text]

    select_len = int(len(sent_tokens) * 0.3)

    summary = nlargest(select_len, sent_scores, key = sent_scores.get)


    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)

    return summary, doc, len(rawdocs.solit(' ')), len(summary.split(' '))
    


