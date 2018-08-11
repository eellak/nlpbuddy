all:
	python3 -m spacy download en
	python3 -m spacy download es
	python3 -m spacy download de
	python3 -m spacy download it
	python3 -m spacy download fr
	python3 -m spacy download nl
	python3 -m spacy download pt
	pip3 install -r requirements.txt
