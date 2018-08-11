import os
import tempfile
from subprocess import check_output
from collections import defaultdict

from django.conf import settings
from spacy import displacy
from gensim.summarization import summarize
import pandas as pd
import operator
import re



fasttext_path = '/opt/demo-app/fastText/fasttext'

# uncomment for debugging purporses
import logging
fmt = getattr(settings, 'LOG_FORMAT', None)
lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)
logging.basicConfig(format=fmt, level=lvl)


MODEL_MAPPING = {
    'el': '/opt/demo-app/demo/el_classiffier.bin'
}

ENTITIES_MAPPING = {
    'PERSON': 'person',
    'LOC': 'location',
    'GPE': 'location',
    'ORG': 'organization',
}

POS_MAPPING = {
    'NOUN': 'nouns',
    'VERB': 'verbs',
    'ADJ': 'adjectives',
}


def load_greek_lexicon():
    indexes = {}
    df = pd.read_csv(
        'datasets/sentiment_analysis/greek_sentiment_lexicon.tsv', sep='\t')
    df = df.fillna('N/A')
    for index, row in df.iterrows():
        df.at[index, "Term"] = row["Term"].split(' ')[0]
        indexes[df.at[index, "Term"]] = index
    subj_scores = {
        'OBJ': 0,
        'SUBJ-': 0.5,
        'SUBJ+': 1,
    }

    emotion_scores = {
        'N/A': 0,
        '1.0': 0.2,
        '2.0': 0.4,
        '3.0': 0.6,
        '4.0': 0.8,
        '5.0': 1,
    }

    polarity_scores = {
        'N/A': 0,
        'BOTH': 0,
        'NEG': -1,
        'POS': 1
    }
    return df, subj_scores, emotion_scores, polarity_scores, indexes


df, subj_scores, emotion_scores, polarity_scores, indexes = load_greek_lexicon()


def analyze_text(text):
    ret = {}
    # language identification
    language = settings.LANG_ID.classify(text)[0]
    lang = settings.LANGUAGE_MODELS[language]
    ret = {}
    doc = lang(text)
    ret['language'] = settings.LANGUAGE_MAPPING[language]
    # analyzed text containing lemmas, pos and dep. Entities are coloured
    analyzed_text = ''
    for token in doc:
        if token.ent_type_:
            analyzed_text += '<span class="tooltip" data-content="POS: {0}<br> LEMMA: {1}<br> DEP: {2}" style="color: red;" >{3} </span>'.format(
                token.pos_, token.lemma_, token.dep_, token.text)
        else:
            analyzed_text += '<span class="tooltip" data-content="POS: {0}<br> LEMMA: {1}<br> DEP: {2}" >{3} </span>'.format(
                token.pos_, token.lemma_, token.dep_, token.text)

    ret['text'] = analyzed_text

    # Text category. Only valid for Greek text for now
    if language == 'el':
        ret.update(sentiment_analysis(doc))
        try:
            ret['category'] = predict_category(text, language)
        except Exception:
            pass

    try:
        ret['summary'] = summarize(text)
    except ValueError:  # why does it break in short sentences?
        ret['summary'] = ''

    # top 10 most frequent keywords, based on tokens lemmatization
    frequency = defaultdict(int)
    lexical_attrs = {
        'urls': [],
        'emails': [],
        'nums': [],
    }
    for token in doc:
        if (token.like_url):
            lexical_attrs['urls'].append(token.text)
        if (token.like_email):
            lexical_attrs['emails'].append(token.text)
        if (token.like_num or token.is_digit):
            lexical_attrs['nums'].append(token.text)
        if not token.is_stop and token.pos_ in ['VERB', 'ADJ', 'NOUN', 'ADV', 'AUX', 'PROPN']:
            frequency[token.lemma_] += 1
    keywords = [keyword for keyword, frequency in sorted(
        frequency.items(), key=lambda k_v: k_v[1], reverse=True)][:10]
    ret['keywords'] = ', '.join(keywords)

    # Named Entities
    entities = {label: [] for key, label in ENTITIES_MAPPING.items()}
    for ent in doc.ents:
        # noticed that these are found some times
        if ent.text.strip() not in ['\n', '', ' ', '.', ',', '-', '–', '_']:
            mapped_entity = ENTITIES_MAPPING.get(ent.label_)
            if mapped_entity and ent.text not in entities[mapped_entity]:
                entities[mapped_entity].append(ent.text)
    ret['named_entities'] = entities

    # Sentences splitting
    ret['sentences'] = [sentence.text for sentence in doc.sents]

    # Lemmatized sentences splitting
    ret['lemmatized_sentences'] = [sentence.lemma_ for sentence in doc.sents]

    # Text tokenization
    ret['text_tokenized'] = [token.text for token in doc]

    # Parts of Speech
    part_of_speech = {label: [] for key, label in POS_MAPPING.items()}

    for token in doc:
        mapped_token = POS_MAPPING.get(token.pos_)
        if mapped_token and token.text not in part_of_speech[mapped_token]:
            part_of_speech[mapped_token].append(token.text)
    ret['part_of_speech'] = part_of_speech
    ret['lexical_attrs'] = lexical_attrs
    ret['noun_chunks'] = [re.sub(r'[^\w\s]', '', x.text) for x in doc.noun_chunks]
    return ret


def predict_category(text, language):
    "Loads FastText models and predicts category"
    text = text.lower().replace('\n', ' ')
    # fastText expects a file here
    fp = tempfile.NamedTemporaryFile(delete=False)
    fp.write(str.encode(text))
    fp.close()

    model = MODEL_MAPPING[language]
    cmd = [fasttext_path, 'predict', model, fp.name]
    result = check_output(cmd).decode("utf-8")
    category = result.split('__label__')[1]

    # remove file
    try:
        os.remove(fp.name)
    except Exception:
        pass

    return category


def visualize_text(text):
    language = settings.LANG_ID.classify(text)[0]
    lang = settings.LANGUAGE_MODELS[language]
    doc = lang(text)
    return displacy.parse_deps(doc)


def sentiment_analysis(doc):

    subjectivity_score = 0
    anger_score = 0
    disgust_score = 0
    fear_score = 0
    happiness_score = 0
    sadness_score = 0
    surprise_score = 0
    matched_tokens = 0
    for token in doc:
        lemmatized_token = token.lemma_
        if (lemmatized_token in indexes):
            indx = indexes[lemmatized_token]
            pos_flag = False
            for col in ["POS1", "POS2", "POS3", "POS4"]:
                if (token.pos_ == df.at[indx, col]):
                    pos_flag = True
                    break
            if (pos_flag):
                match_col_index = [int(s) for s in col if s.isdigit()][0]
                subjectivity_score += subj_scores[df.at[indx,
                                                        'Subjectivity' + str(match_col_index)]]
                anger_score += emotion_scores[str(
                    df.at[indx, 'Anger' + str(match_col_index)])]
                disgust_score += emotion_scores[str(
                    df.at[indx, 'Disgust' + str(match_col_index)])]
                fear_score += emotion_scores[str(
                    df.at[indx, 'Fear' + str(match_col_index)])]
                happiness_score += emotion_scores[str(
                    df.at[indx, 'Happiness' + str(match_col_index)])]
                sadness_score += emotion_scores[str(
                    df.at[indx, 'Sadness' + str(match_col_index)])]
                surprise_score += emotion_scores[str(
                    df.at[indx, 'Surprise' + str(match_col_index)])]
                matched_tokens += 1
    try:
        subjectivity_score = subjectivity_score / matched_tokens * 100
        emotions = {'anger': anger_score, 'disgust': disgust_score, 'fear': fear_score,
                    'happiness': happiness_score, 'sadness': sadness_score, 'surprise': surprise_score}
        emotion_name = max(emotions.items(), key=operator.itemgetter(1))[0]
        emotion_score = emotions[emotion_name] * 100 / matched_tokens
        ret = {'subjectivity': round(subjectivity_score, 2),
               'emotion_name': emotion_name, 'emotion_score': round(emotion_score, 2)}
        # logging.debug(subjectivity_score)
        return ret
    except ZeroDivisionError:
        return {}
    except Exception:
        return {}
