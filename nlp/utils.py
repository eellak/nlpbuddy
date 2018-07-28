from collections import defaultdict

from django.conf import settings
from gensim.summarization import summarize

ENTITIES_MAPPING = {
    'PERSON': 'person',
    'LOC': 'location',
    'GPE': 'location',
    'ORG':'organization',
}

POS_MAPPING = {
    'NOUN': 'nouns',
    'VERB': 'verbs',
    'ADJ': 'adjectives',
}

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
                analyzed_text += '<span class="tooltip" data-content="POS: {0}<br> LEMMA: {1}<br> DEP: {2}" style="color: red;" >{3} </span>'.format(token.pos_, token.lemma_, token.dep_, token.text)
            else:
                analyzed_text += '<span class="tooltip" data-content="POS: {0}<br> LEMMA: {1}<br> DEP: {2}" >{3} </span>'.format(token.pos_, token.lemma_, token.dep_, token.text)

        ret['text'] = analyzed_text

        # TODO: add classifier for the Greek language
        if language == 'el':
            ret['category'] = 'Soon_to_come'
        else:
            ret['category'] = ''

        try:
            ret['summary'] = summarize(text)
        except ValueError: # why does it break in short sentences?
            ret['summary'] = ''

        # top 10 most frequent keywords, based on tokens lemmatization
        frequency = defaultdict(int)
        for token in doc:
            if not token.is_stop and token.pos_ in ['VERB', 'ADJ', 'NOUN', 'ADV', 'AUX', 'PROPN']:
                frequency[token.lemma_] +=1
        keywords = [keyword for keyword, frequency in sorted(frequency.items(), key=lambda k_v: k_v[1], reverse=True)][:10]
        ret['keywords'] =  ', '.join(keywords)

        # Named Entities
        entities = {label:[] for key, label in ENTITIES_MAPPING.items()}
        for ent in doc.ents:                      
            mapped_entity = ENTITIES_MAPPING.get(ent.label_)
            if mapped_entity and ent.text not in entities[mapped_entity]:
                entities[mapped_entity].append(ent.text)

        # Sentences splitting
        ret['named_entities'] = entities
        ret['sentences'] = [sentence.text for sentence in doc.sents]

        # Text tokenization
        ret['text_tokenized'] = [token.text for token in doc]

        # Parts of Speech
        part_of_speech = {label:[] for key, label in POS_MAPPING.items()}

        for token in doc:
            mapped_token = POS_MAPPING.get(token.pos_)
            if mapped_token and token.text not in part_of_speech[mapped_token]:
                part_of_speech[mapped_token].append(token.text)
        ret['part_of_speech'] = part_of_speech

        return ret
