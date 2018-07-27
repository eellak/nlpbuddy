var fnc = {
    dom: {
        addClass: function(el, theClass) {
            if (el.classList) {
                el.classList.add(theClass);
            } else {
                el.className += ' ' + theClass;
            }
        },
        removeClass: function(el, theClass) {
            if (el.classList) {
                el.classList.remove(theClass);
            } else {
                el.className = el.className.replace(new RegExp('(^|\\b)' + theClass.split(' ').join('|') + '(\\b|$)', 'gi'), ' ');
            }
        },
        hasClass: function(el, theClass) {
            return el.className && new RegExp("(\\s|^)" + theClass + "(\\s|$)").test(el.className);
        },
        toggleClass: function(el, theClass) {
            return fnc.dom.hasClass(el, theClass) ? fnc.dom.removeClass(el, theClass) : fnc.dom.addClass(el, theClass);
        }
    }
};

/**
 * IE 5.5+, Firefox, Opera, Chrome, Safari XHR object
 *
 * @see [https://gist.github.com/Xeoncross/7663273]{@link https://gist.github.com/Xeoncross/7663273}
 * @param string url
 * @param object callback
 * @param mixed data
 * @param null x
 */
function fncAjax(url, callback, requestType, data, x) {
    try {
        x = new(this.XMLHttpRequest || ActiveXObject)('MSXML2.XMLHTTP.3.0');
        x.open( 'undefined' !== typeof requestType ? requestType : ( data ? 'POST' : 'GET' ), url, 1 );
        x.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        x.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
        x.onreadystatechange = function () {
            x.readyState > 3 && callback && callback(x);
        };
        x.send(data);
    } catch (e) {
        window.console && console.log(e);
    }
}

function TextAnalyzerEditor() {
    "use strict";

    var ins = this;

    this.elem = {
        body: document.querySelector('body'),
        analyzeBtn: document.querySelector('.analyze-it'),
        selectText: document.querySelector('.select-static-text select'),
        selectCustomTextBtn: document.querySelector('.select-custom-text button'),
        staticTextEditor: document.querySelector('textarea.static-text-textarea'),
        customTextEditor: document.querySelector('textarea.custom-text-textarea')
    };

    if (!this.elem.analyzeBtn || !this.elem.selectText || !this.elem.selectCustomTextBtn || !this.elem.staticTextEditor || !this.elem.customTextEditor) {
        console.error('Missing analyzer components, ', this.elem.analyzeBtn, this.elem.selectText, this.elem.selectCustomTextBtn, this.elem.staticTextEditor, this.elem.customTextEditor);
        return;
    }

    function displayLoader() {
        fnc.dom.addClass(ins.elem.body, 'is-loading');
    }

    function hideLoader() {
        fnc.dom.removeClass(ins.elem.body, 'is-loading');
    }

    function requestTextAnalysis(txt, callback) {

        displayLoader();

        fncAjax( '/api/analyze', function(result){
            if( 200 === result.status ){
                if( 'function' === typeof callback ){
                    callback( 'string' === typeof result.response ? JSON.parse( result.response ) : result.response );
                }
            }
            else{
                console.warn('Invalid response status', result.status);
            }
        }, 'POST', JSON.stringify( { text: txt } ) ) ;
    }

    function load_results(type, val) {
        var i, w, d;
        switch (type) {
            case 'text':
                ins.elem.boxes.resultsContent.innerHTML = val;
                break;
            case 'summary':
                ins.elem.boxes.summaryContent.innerHTML = val;
                break;
            case 'various':
                w = 'undefined' !== typeof val.language ? '<li><label>' + i18n.Languague + ':</label>' + val.language + '</li>' : '';
                w += 'undefined' !== typeof val.category ? '<li><label>' + i18n.Category + ':</label>' + val.category + '</li>' : '';
                w = '' === w ? w : '<ul>' + w + '</ul>';
                ins.elem.boxes.variousContent.innerHTML = w;
                break;
            case 'entities':
                w = '';
                if ('undefined' !== typeof val.person && val.person.length) {
                    d = '';
                    i = 0;
                    while (i < val.person.length) {
                        d += '<span>' + val.person[i] + '</span>';
                        i += 1;
                    }
                    w += '<li><label>' + i18n.Person + '</label><div class="person">' + d + '</div></li>';
                }
                if ('undefined' !== typeof val.location && val.location.length) {
                    d = '';
                    i = 0;
                    while (i < val.location.length) {
                        d += '<span>' + val.location[i] + '</span>';
                        i += 1;
                    }
                    w += '<li><label>' + i18n.Location + '</label><div class="location">' + d + '</div></li>';
                }
                if ('undefined' !== typeof val.organization && val.organization.length) {
                    d = '';
                    i = 0;
                    while (i < val.organization.length) {
                        d += '<span>' + val.organization[i] + '</span>';
                        i += 1;
                    }
                    w += '<li><label>' + i18n.Organization + '</label><div class="organization">' + d + '</div></li>';
                }

                w = '' === w ? w : '<ul>' + w + '</ul>';
                ins.elem.boxes.entitiesContent.innerHTML = w;
                break;
            case 'part_of_speech':
                w = '';
                if ('undefined' !== typeof val.verbs && val.verbs.length) {
                    d = '';
                    i = 0;
                    while (i < val.verbs.length) {
                        d += '<span>' + val.verbs[i] + '</span>';
                        i += 1;
                    }
                    w += '<li><label>' + i18n.Verbs + '</label><div class="verbs">' + d + '</div></li>';
                }
                if ('undefined' !== typeof val.adjectives && val.adjectives.length) {
                    d = '';
                    i = 0;
                    while (i < val.adjectives.length) {
                        d += '<span>' + val.adjectives[i] + '</span>';
                        i += 1;
                    }
                    w += '<li><label>' + i18n.Adjectives + '</label><div class="adjectives">' + d + '</div></li>';
                }
                if ('undefined' !== typeof val.nouns && val.nouns.length) {
                    d = '';
                    i = 0;
                    while (i < val.nouns.length) {
                        d += '<span>' + val.nouns[i] + '</span>';
                        i += 1;
                    }
                    w += '<li><label>' + i18n.Nouns + '</label><div class="nouns">' + d + '</div></li>';
                }

                w = '' === w ? w : '<ul>' + w + '</ul>';
                ins.elem.boxes.partOfSpeechContent.innerHTML = w;
                break;
            case 'keywords':
                w = '';
                i = 0;
                while (i < val.length) {
                    w += '<span>' + val[i].trim() + '</span>';
                    i += 1;
                }
                ins.elem.boxes.keywordsContent.innerHTML = w;
                break;
            case 'tokens':
                w = '';
                i = 0;
                while (i < val.length) {
                    w += '<span>' + val[i].trim() + '</span>';
                    i += 1;
                }
                ins.elem.boxes.tokensContent.innerHTML = w;
                break;
            case 'sentences':
                w = '';
                i = 0;
                while (i < val.length) {
                    w += '<li>' + val[i].trim() + '</li>';
                    i += 1;
                }
                w = '' === w ? w : '<ol>' + w + '</ol>';
                ins.elem.boxes.sentencesContent.innerHTML = w;
                break;
        }
    }

    function responseTextAnalysis(result) {
        load_results('text', result.text || '');
        load_results('various', { language: result.language, category: result.category });
        load_results('keywords', result.keywords && ( '' !== result.keywords ? result.keywords.split(',') : [] ) );
        load_results('summary', result.summary || '');
        load_results('entities', result.named_entities);
        load_results('part_of_speech', result.part_of_speech);
        load_results('tokens', result.text_tokenized || []);
        load_results('sentences', result.sentences);

        fnc.dom.addClass(ins.elem.body, 'has-results');

        if( result.text && '' !== result.text ){
            initTooltips( document.querySelector('.results-box.text-results').querySelectorAll('.tooltip') );
        }

        hideLoader();
    }

    function on_textSelect() {
        fnc.dom[ins.states.customText ? 'addClass' : 'removeClass'](ins.elem.body, 'with-custom-text-editor');
    }

    function onclick_analyzeIt() {
        var analyzeTxt = ins.elem[ins.states.customText ? 'customTextEditor' : 'staticTextEditor'].value.trim();
        if (2 < analyzeTxt.length) {
            requestTextAnalysis(analyzeTxt, responseTextAnalysis);
        }
    }

    function onselect_staticText() {
        if ('false' === this.value || (ins.states.selectedCustomText === this.value && ! ins.states.customText) ) {
            return;
        }
        ins.states.selectedCustomText = this.value;
        ins.elem.staticTextEditor.value = StaticTexts[this.value].content;
        ins.states.customText = !1;
        on_textSelect();
    }

    function onselect_customText() {
        if (!0 === ins.states.customText) {
            return;
        }
        ins.states.customText = !0;
        on_textSelect();
    }

    function onclick_toggleNav(){
        fnc.dom.toggleClass(ins.elem.body, 'vis-mobile-nav');
    }

    this.elem.toggleNav = document.querySelector('.toggle-nav');
    this.elem.staticTextWrap = document.querySelector('.select-static-text');
    this.elem.customTextWrap = document.querySelector('.select-custom-text');

    this.elem.boxes = {
        resultsContent: document.querySelector('.results-box.text-results .rb-content'),
        variousContent: document.querySelector('.results-box.various .rb-content'),
        keywordsContent: document.querySelector('.results-box.keywords .rb-content'),
        summaryContent: document.querySelector('.results-box.summary .rb-content'),
        entitiesContent: document.querySelector('.results-box.entities .rb-content'),
        partOfSpeechContent: document.querySelector('.results-box.part-of-speech .rb-content'),
        tokensContent: document.querySelector('.results-box.tokens .rb-content'),
        sentencesContent: document.querySelector('.results-box.sentences .rb-content')
    };

    this.states = {
        customText: !1,
        selectedCustomText: null
    };

    this.elem.analyzeBtn.addEventListener('click', onclick_analyzeIt);
    this.elem.selectText.addEventListener('change', onselect_staticText);
    this.elem.selectCustomTextBtn.addEventListener('click', onselect_customText);
    this.elem.toggleNav.addEventListener('click', onclick_toggleNav);

    var k, g;

    for (k in StaticTexts) {
        if (StaticTexts.hasOwnProperty(k)) {
            g = document.createElement('option');
            g.value = k;
            g.innerHTML = StaticTexts[k].title;
            this.elem.selectText.appendChild(g);
        }
    }
}

var tooltipElementInstance = null;

function TooltipElement(){
    "use strict";

    this.element = null;

    (function(ins){

        var x, ttInner, ttContent;

        ins.element = document.createElement('div');
        ins.element.setAttribute('class', 'tooltip-container');

        ttInner = document.createElement('div');
        ttInner.setAttribute('class', 'tooltip-inner');

        ttContent = document.createElement('div');
        ttContent.setAttribute('class', 'tooltip-content');

        ttInner.appendChild(ttContent);

        ins.element.appendChild(ttInner);

        ins.newContent = function(content){
            ttContent.innerHTML = content;
        };

        ins.hide = function(content){
            ttContent.innerHTML = content;
        };

    })(this);
}

function mouseenter_tooltip_trigger(ev){
    var clientRect, winWidth, tooltipContainerWidth = 200, content = this.getAttribute('data-content');
    content = content.trim() || '';
    if( '' !== content ){
        tooltipElementInstance = tooltipElementInstance || new TooltipElement();
        if( tooltipElementInstance.element ){
            tooltipElementInstance.newContent(content);
            clientRect = this.getBoundingClientRect();
            winWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;

            // console.log( clientRect, winWidth, clientRect.left, clientRect.width, tooltipContainerWidth);

            if( winWidth < ( clientRect.left + ( clientRect.width / 2 ) + ( tooltipContainerWidth / 2 ) ) ){
                fnc.dom.addClass( tooltipElementInstance.element, 'from-right' );
                fnc.dom.removeClass( tooltipElementInstance.element, 'from-left' );
            }
            else if( 0 > ( clientRect.left + ( clientRect.width / 2 ) - ( tooltipContainerWidth / 2 ) ) ){
                fnc.dom.addClass( tooltipElementInstance.element, 'from-left' );
                fnc.dom.removeClass( tooltipElementInstance.element, 'from-right' );
            }
            else{
                fnc.dom.removeClass( tooltipElementInstance.element, 'from-left' );
                fnc.dom.removeClass( tooltipElementInstance.element, 'from-right' );
            }
            this.appendChild( tooltipElementInstance.element );
        }
    }
}

function initTooltips( tt ){
    var i;
    if( tt.length ){
        i=0;
        while(i<tt.length){
            tt[i].addEventListener("mouseenter", mouseenter_tooltip_trigger);
            tt[i].addEventListener("click", mouseenter_tooltip_trigger);
            i+=1;
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    "use strict";
    new TextAnalyzerEditor();
    initTooltips( document.querySelectorAll('.tooltip') );
});
