# text-analysis
## About the project

This is a text analysis application for performing common NLP tasks through a web dashboard interface and an API. 

It leverages [Spacy](https://spacy.io) for the NLP tasks plus [Gensim's](https://github.com/RaRe-Technologies/gensim) implementation of the TextRank algorithm for text summarization. 

It supports Greek and English texts, with automatic identification of language. 

Tasks include:
1. Text tokenization
2. Sentence splitting
3. Part of Speech tags identification (verbs, nouns etc)
4. Named Entity Recognition (Location, Person, Organisation etc)
5. Text summarization (using TextRang algorithm, implemented by Gensim)
6. Keywords extraction
7. Language identification
8. For the Greek language, Categorization of text in one of the following categories: 

Αθλητισμός, Ελλάδα, Επιστήμη, Κόσμος, Οικονομία, Περιβάλλον, Πολιτική, Τέχνες, Υγεία 

Classifier is built with [FastText](https://fasttext.cc) and is trained in 20.000 articles labeled in these categories.

## TODO
1. Add instructions on how to install + test environment
Tested on Ubuntu 16.04 with python 3.5
create virtual env: virtualenv -p python3.5 .
source activate: source bin/activate
clone project: https://github.com/eellak/text-analysis/
enter project dir: cd text-analysis
install requirements: pip install -r requirements.txt
run django migrations: python manage migrate
install nginx: apt-get install nginx
setup nginx + uwsgi configs: deploy/ ... . make sure to set the servername
visit url...

2. Make sure spaCy models (and GR classification model) are loaded only when necessary
3. improve summarization (currently stub)
4. add elements missing (category for greek, keywords, sentences, lemma/tags on text results. Add some nice examples for greek/english
