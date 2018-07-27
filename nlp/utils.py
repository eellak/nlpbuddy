from gensim.summarization import summarize

ENTITIES_MAPPING = {
    'PERSON': 'person',
    'LOC': 'location',
    'GPE': 'location',
    'ORG':'organization',
    }


def analyze_text(models, text):
        # TODO: find language
        # language = models['
        lang = models['Greek']
        ret = {}
        doc = lang(text)
        ret['language'] = 'Greek'

        
        ret['text'] = '''
         <span title="POS: DET, LEMMA: Ο">Ο</span> <span style="color:red" title="POS: NOUN, LEMMA: Θησέας">Θησέας</span> <span title="POS: VERB, LEMMA: σκοτώνω">σκότωσε</span> <span title="POS: DET, LEMMA: Ο">το</span> <span style="color:red" title="POS: NOUN, LEMMA: Μινώταυρος">Μινώταυρο</span>
         '''
        ret['category'] = 'Athletics'

        ret['summary'] = summarize(text)
        ret['keywords'] =  'σπαθι, δεντρο, χερι'
        # Named Entities
        entities = {label:[] for key, label in ENTITIES_MAPPING.items()}
        for ent in doc.ents:                      
            mapped_entity = ENTITIES_MAPPING.get(ent.label_)
            if mapped_entity and ent.text not in entities[mapped_entity]:
                entities[mapped_entity].append(ent.text)

        ret['named_entities'] = entities
        ret['sentences'] = ['sentence1 goes here', 'sentence xxx goes here']
        ret['text_tokenized'] = [token.text for token in doc]

        ret['part_of_speech'] = {
                           'verbs': ['σκότωσε', 'κολύμπησε'],
                           'adjectives': ['καλός', 'φοβερός'],
                           'nouns': ['πρόβατο', 'κεράσι']
                          }
        return ret
