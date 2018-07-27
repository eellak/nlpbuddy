from django.shortcuts import render
from django.http import JsonResponse

import spacy
from .utils import analyze_text

# load the two language models. Currently supported languages are 
# Greek, English

LANGUAGE_MODELS = {
        'Greek': spacy.load('el_core_web_sm'),
        'English': spacy.load('en_core_web_sm')
    }    


def index(request):
    'Index view'
    context = {}
    return render(request, 'nlp/index.html', context)

def about(request):
    'About view'
    context = {}
    return render(request, 'nlp/about.html', context)


def analyze(request):
    if request.method == 'POST':
#        text = request.POST.get("text", "")
        # TODO: will remove once js sends text as expected
        for key in request.POST.dict().keys():
            text = key
        # add some limit here
        text = text[:200000]
        ret = {}
        ret = analyze_text(LANGUAGE_MODELS, text)

        if not text:
            response = JsonResponse({'status':'false','message':'need some text here!'})
            response.status_code = 500
            return response

        return JsonResponse(ret)
    else:
        ret = {'methods_allowed': 'POST'}
        return JsonResponse(ret)

