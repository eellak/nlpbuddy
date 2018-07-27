from gensim.summarization import summarize
from django.conf import settings

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

        language = settings.LANG_ID.classify(text)[0]
        lang = settings.LANGUAGE_MODELS[language]
        ret = {}
        doc = lang(text)
        ret['language'] = settings.LANGUAGE_MAPPING[language]

        
        ret['text'] = '''
         <span title="POS: DET, LEMMA: Ο">Ο</span> <span style="color:red" title="POS: NOUN, LEMMA: Θησέας">Θησέας</span> <span title="POS: VERB, LEMMA: σκοτώνω">σκότωσε</span> <span title="POS: DET, LEMMA: Ο">το</span> <span style="color:red" title="POS: NOUN, LEMMA: Μινώταυρος">Μινώταυρο</span>
         '''
        if language == 'el':
            ret['category'] = 'Soon_to_come'
        else:
            ret['category'] = ''

        try:
            ret['summary'] = summarize(text)
        except ValueError: # why does it break?
            ret['summary'] = ''
        ret['keywords'] =  'σπαθι, δεντρο, χερι'
        
        # Named Entities
        entities = {label:[] for key, label in ENTITIES_MAPPING.items()}
        for ent in doc.ents:                      
            mapped_entity = ENTITIES_MAPPING.get(ent.label_)
            if mapped_entity and ent.text not in entities[mapped_entity]:
                entities[mapped_entity].append(ent.text)

        ret['named_entities'] = entities
#        ret['sentences'] = ['sentence1 goes here', 'sentence xxx goes here']
        ret['sentences'] = [sentence.text for sentence in doc.sents]

        # TEXT TOKENIZATION
        ret['text_tokenized'] = [token.text for token in doc]

        # Parts of Speech
        part_of_speech = {label:[] for key, label in POS_MAPPING.items()}

        for token in doc:
            mapped_token = POS_MAPPING.get(token.pos_)
            if mapped_token and token.text not in part_of_speech[mapped_token]:
                part_of_speech[mapped_token].append(token.text)
        ret['part_of_speech'] = part_of_speech

        return ret
