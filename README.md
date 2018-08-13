# NLPBuddy - Open Source Text Analysis Tool

## About the project

NLPBuddy is a text analysis application for performing common NLP tasks through a web dashboard interface and an API. 

It leverages [Spacy](https://spacy.io) for the NLP tasks plus [Gensim's](https://github.com/RaRe-Technologies/gensim) implementation of the TextRank algorithm for text summarization. 

It supports texts in the following languages: Greek, English, German, Spanish, Portoguese, French, Italian and Dutch. Language identification is performed automatically through [langid](https://github.com/saffsd/langid.py)

Tasks include:
1. Text tokenization
2. Sentence splitting (lemmatized sentences too)
3. Part of Speech tags identification (verbs, nouns etc)
4. Named Entity Recognition (Location, Person, Organisation etc)
5. Text summarization (using TextRank algorithm, implemented by Gensim)
6. Keywords extraction
7. Language identification
8. For the Greek language, Categorization of text 

Text can either be provided or imported after specifying a url - we use library [python readability](https://github.com/buriy/python-readability) for this plus [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)

The Greek classifier is built with [FastText](https://fasttext.cc) and is trained in 20.000 articles labeled in these categories.

## Demo
A working demo can be found on [http://www.nlpbuddy.io/](http://www.nlpbuddy.io/)

## Usage
Enter text and hit 'Analyze it', 

![alt text](https://raw.githubusercontent.com/eellak/text-analysis/master/static/img/screenshot1.jpg)

## API Usage
[https://github.com/eellak/text-analysis/wiki/API-usage](https://github.com/eellak/text-analysis/wiki/API-usage)

## Installation 
Find development and deployment instructions here: https://github.com/eellak/text-analysis/wiki/Install

## License
The code is provided under the GNU AGPL v3.0 License.

