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


