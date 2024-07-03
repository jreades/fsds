import pandas as pd
import os
import re
import sys
#import math # May be needed for isnan
import time
import html
import nltk
import string
import unicodedata

# Deals with Icelandic and other non-ASCII
# characters in a more straightforward way
# than a non-library based regex.
from unidecode import unidecode

DEBUG = False

###########################
# Download NLTK libraries if we haven't already
# downloaded and saved them. This _can_ be done
# while building the Docker image but could then
# leave those not using Docker high and dry.
###########################
try:
    nltk.data.load('tokenizers/punkt/english.pickle')
except LookupError as e:
    print("Unable to load punkt, downloading...")
    nltk.download('punkt')
    nltk.data.load('tokenizers/punkt/english.pickle')

try: 
    from nltk.corpus import stopwords
    stopword_list = set(stopwords.words('english'))
except LookupError as e:
    print("Unable to load stopwords, downloading...")
    nltk.download('stopwords')
    from nltk.corpus import stopwords
    stopword_list = set(stopwords.words('english'))

# Alternate tokenizer: 
#from nltk.tokenize.toktok import ToktokTokenizer
#wtok = ToktokTokenizer()
try:
    wtok = nltk.tokenize.treebank.TreebankWordTokenizer()
    nltk.pos_tag(wtok.tokenize("A test of the perceptron tagger"))
except LookupError as e:
    print("Unable to load POS tagger, downloading...")
    nltk.download('averaged_perceptron_tagger')
    wtok = nltk.tokenize.treebank.TreebankWordTokenizer()
    nltk.pos_tag(wtok.tokenize("A test of the perceptron tagger"))

try:
    from nltk.corpus import wordnet as wn 
    lm = nltk.stem.wordnet.WordNetLemmatizer()
    lm.lemmatize("ran")
except LookupError as e:
    print("Unable to load WordNet, downloading...") 
    nltk.download('omw-1.4')
    nltk.download('wordnet')
    from nltk.corpus import wordnet as wn 
    lm = nltk.stem.wordnet.WordNetLemmatizer()
    lm.lemmatize("ran")

from nltk.tokenize import sent_tokenize

print("All NLTK libraries installed...")

# How to update the stopword list... 
stopword_list.update([
#    'thesis','dissertation','chapter','chapters','research','result','results',
#    'methodology','approach','understand','understanding','demonstrate','find', 
])

from bs4 import BeautifulSoup

# Utility function for dealing with uncertain 
# encodings. This is a pretty brutal approach
# that assumes quite a lot, but seems to work 
# with the many data sets.
def decode(text:str, encd:str='latin1', decd:str='utf-8') -> str:
    """
    Attempts to resolve encoding issues in a rather 
    direct manner by encoding and decoding the string. 
    If a UnicodeDecdeError is thrown then it will return
    the original string unchanged.

    text: a string to be decoded.
    encd: the encoding scheme to use (defaults to latin1)
    decd: the decoding scheme to use (defaults to utf-8)
    """
    try:
        return text.encode(encd).decode(decd).replace('\n',' ')
    except UnicodeDecodeError as e:
        print(f"Problem decoding '{text[:45]}...'")
        return text

# POS_TAGGER_FUNCTION : TYPE 1 
def pos_tagger(nltk_tag): 
    """
    Returns the appropriate Wordnet POS tag for a set
    of specified NLTK tags (we only focus on a few of them).

    nltk_tag: a NLTK POS tag to be translated to a Wordnet tag
    """
    if nltk_tag.startswith('J'): 
        return wn.ADJ 
    elif nltk_tag.startswith('V'): 
        return wn.VERB 
    elif nltk_tag.startswith('N'): 
        return wn.NOUN 
    elif nltk_tag.startswith('R'): 
        return wn.ADV 
    else:           
        return None

# Useful example code [here](https://www.geeksforgeeks.org/python-lemmatization-approaches-with-examples/?ref=rp).
# 
# | Tag | What it Means |
# | :-- | :------------ |
# | CC | coordinating conjunction |
# | CD | cardinal digit |
# | DT | determiner |
# | EX | existential there (like: “there is” … think of it like “there exists”) |
# | FW | foreign word |
# | IN | preposition/subordinating conjunction |
# | JJ | adjective ‘big’ |
# | JJR | adjective, comparative ‘bigger’ |
# | JJS | adjective, superlative ‘biggest’ |
# | LS | list marker 1 |
# | MD | modal could, will |
# | NN | noun, singular ‘desk’ |
# | NNS | noun plural ‘desks’ |
# | NNP | proper noun, singular ‘Harrison’ |
# | NNPS | proper noun, plural ‘Americans’ |
# | PDT | predeterminer ‘all the kids’ |
# | POS | possessive ending parent‘s |
# | PRP | personal pronoun I, he, she |
# | PRP\$ | possessive pronoun my, his, hers |
# | RB | adverb very, silently, |
# | RBR | adverb, comparative better |
# | RBS | adverb, superlative best |
# | RP | particle give up |
# | TO | to go ‘to‘ the store. |
# | UH | interjection errrrrrrrm |
# | VB | verb, base form take |
# | VBD | verb, past tense took |
# | VBG | verb, gerund/present participle taking |
# | VBN | verb, past participle taken |
# | VBP | verb, sing. present, non-3d take |
# | VBZ | verb, 3rd person sing. present takes |
# | WDT | wh-determiner which |
# | WP  | wh-pronoun who, what |
# | WP\$ | possessive wh-pronoun whose |
# | WRB | wh-abverb where, when |

pos_tags = """| CC | coordinating conjunction |
| CD | cardinal digit |
| DT | determiner |
| EX | existential there |
| FW | foreign word |
| IN | preposition/subordinating conjunction |
| JJ | adjective 'big' |
| JJR | adjective, comparative |
| JJS | adjective, superlative |
| LS | list marker 1 |
| MD | modal could, will |
| NN | noun, singular |
| NNS | noun plural |
| NNP | proper noun, singular |
| NNPS | proper noun, plural |
| PDT | predeterminer |
| POS | possessive ending |
| PRP | personal pronoun |
| PRP | possessive pronoun |
| RB | adverb very, silently, |
| RBR | adverb, comparative |
| RBS | adverb, superlative |
| RP | participle |
| TO | to go 'to' |
| UH | interjection |
| VB | verb, base form |
| VBD | verb, past tense |
| VBG | verb, gerund/present participle |
| VBN | verb, past participle |
| VBP | verb, sing. present, non-3d |
| VBZ | verb, 3rd person sing. present |
| WDT | wh-determiner |
| WP  | wh-pronoun |
| WP | possessive |
| WRB | wh-abverb |"""

global pos_lkp
pos_lkp  = {}
for p in pos_tags.split("\n"):
    m = re.search(r"^\| ([A-Z\$]{2,5})\s+\| ([^\|]+)", p)
    pos_lkp[m.groups()[0]] = m.groups()[1].strip()

# https://stackoverflow.com/a/57917378/4041902
def case_lemma(word, pos):
    """
    Does lemmatisation *without* requiring the term to have
    already been converted to lowercase. This can be useful
    because it deals more effectively with acronyms, terms-of-
    art and so on. You don't usually call this directly as it's
    used by the 'lemmatise' function.

    word: the term to be lemmatised
    pos:  the part-of-speech (which influences lemmatisation)
    """
    try: 
        if word.isupper() or re.match(r"^[A-Z\.]+$", word): # Likely acronyms shouldn't title-case
            word = lm.lemmatize(word, pos=pos_tagger(pos)).upper()
            #print(f"case_lemma[upper]({word}, {pos})")
        elif word == word.title():
            word = lm.lemmatize(word, pos=pos_tagger(pos)).capitalize()
            #print(f"case_lemma[title]({word}, {pos})")
        else:
            word = lm.lemmatize(word, pos=pos_tagger(pos))
    except KeyError:
        if DEBUG: print(f"Can't process: {t[0]} / {pos_tagger(t[1])}")
        pass

    return word

# More pandas-friendly version of the lemmatisation function.
# Notice that we again assume that the text is not yet lower-case
# since this allows us to work as late as possible with the 
# cased text, thus giving more time to detect names, acronyms, etc.
def lemmatise(text:str) -> str:
    """
    Performs lemmatisation of a sentence or paragraph while trying
    to respect some fairly sophisticated pre-processing that might
    include phrase detection (e.g. Geographic_Information_Systems).

    text: a sentence or paragraph to be lemmatised.
    """
    sents  = sent_tokenize(text)
    lemmas = []
    for s in sents:

        # Word tokenizers is used to find the words  
        # and punctuation in a string 
        wordsList = wtok.tokenize(s)

        # Using a part-of-speech  
        # tagger or POS-tagger.  
        tagged = nltk.pos_tag(wordsList)

        slemmas = []

        # For each of the tagged elements...
        for t in tagged:
            # Does it look like a phrase or other special case
            # marked by a '_' linking two or more raw terms?
            if '_' in t[0]:
                ulemmas = []
                for w in nltk.pos_tag(t[0].split('_')):
                    ulemmas.append( case_lemma(w[0], w[1]) )
                slemmas.append("_".join(ulemmas))
            else:
                slemmas.append( case_lemma(t[0], t[1]) )
        lemmas.append(" ".join(slemmas))
    
    return " ".join(lemmas)

# These seem to come through surprisingly often and need to resolved
smart_quotes = set(['‘','“','”','"','"',"’","‹","›","»","«","'","'"])
sq = re.compile(f"({'|'.join(smart_quotes)})",flags=re.IGNORECASE|re.DOTALL)
def remove_quotemarks(text:str) -> str:
    """
    Removes 'smart' quotes that seem to escape from the 
    majority of punctuation removal approaches.

    text: the input text.
    """
    text = re.sub("\w’\w","'",text,flags=re.IGNORECASE|re.DOTALL) # This is for possessives
    text = sq.sub(" ",text) # Get rid of everything else
    return text

# I have replaced the KDNuggets solution with a more 
# straightforward approach that requires an external
# library. The external library appears to do a better
# job of converting non-ASCII characters to a reasonable
# ASCII equivalent (å becomes a, and ß becomes Ss...)
# Adapted from https://www.kdnuggets.com/2018/08/practitioners-guide-processing-understanding-text-2.html
areg = re.compile('([a-z]+?)\?([a-z])', flags=re.IGNORECASE|re.DOTALL)
def remove_accented_chars(text:str) -> str:
    """
    Replaces accented characters from source text using a 
    standard unicode decoding approach such that å becomes a, 
    and ß becomes Ss, and so on. 

    text: the text from which to replace accented characters.
    """
    return areg.sub(r'\1\2', unidecode(text))
    #return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')

# From https://www.kdnuggets.com/2018/08/practitioners-guide-processing-understanding-text-2.html
# From https://stackoverflow.com/questions/19790188/expanding-english-language-contractions-in-python
global CONTRACTION_MAP
CONTRACTION_MAP = { 
    "ain't": "am not",
    "aren't": "are not",
    "can't": "cannot",
    "can't've": "cannot have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he would",
    "he'd've": "he would have",
    "he'll": "he will",
    "he'll've": "he will have",
    "he's": "he is",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how'll": "how will",
    "how's": "how is",
    "I'd": "I would",
    "I'd've": "I would have",
    "I'll": "I will",
    "I'll've": "I will have",
    "I'm": "I am",
    "I've": "I have",
    "i'd": "I would",
    "i'd've": "I would have",
    "i'll": "I will",
    "i'll've": "I will have",
    "i'm": "I am",
    "i've": "I have",
    "isn't": "is not",
    "it'd": "it would",
    "it'd've": "it would have",
    "it'll": "it will",
    "it'll've": "it will have",
    "it's": "it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "o'clock": "of the clock",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd": "she had / she would",
    "she'd've": "she would have",
    "she'll": "she will",
    "she'll've": "she will have",
    "she's": "she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so is",
    "that'd": "that would",
    "that'd've": "that would have",
    "that's": "that is",
    "there'd": "there would",
    "there'd've": "there would have",
    "there's": "there is",
    "they'd": "tthey would",
    "they'd've": "they would have",
    "they'll": "they will",
    "they'll've": "they will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    "we'd": "we would",
    "we'd've": "we would have",
    "we'll": "we will",
    "we'll've": "we will have",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "hat will",
    "what'll've": "what will have",
    "what're": "what are",
    "what's": "what is",
    "what've": "what have",
    "when's": "when is",
    "when've": "when have",
    "where'd": "where did",
    "where's": "where is",
    "where've": "where have",
    "who'll": "who will",
    "who'll've": "who will have",
    "who's": "who is",
    "who've": "who have",
    "why's": "why is",
    "why've": "why have",
    "will've": "will have",
    "won't": "will not",
    "won't've": "will not have",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "y'all're": "you all are",
    "y'all've": "you all have",
    "you'd": "you would",
    "you'd've": "you would have",
    "you'll": "you will",
    "you'll've": "you will have",
    "you're": "you are",
    "you've": "you have"
}

# Remove some very common abbreviations
contracts = re.compile(r'\b[IiEe]\.?[eg]\.{0,1}\b') # Forgot the trailing \b and messed up Egyptology
def remove_contractions(text):
    """
    Replaces very common contractions (e.g., i.e., etc.) 
    with an empty space (' ')

    text: the text from which to remove contractions
    """
    return contracts.sub(' ', text)

# This captures a wide range of contractions, though 
# I don't know if we should also be capturing the 
# possessive and fixing that as well... 
def expand_contractions(text, contraction_mapping=CONTRACTION_MAP):
    """
    Uses a map of common contractions to replace 
    them with the 'written out' form such that 
    "you'll" becomes 'you will' and so forth.

    text: the input text in which to replace contractions
    contraction_mapping: a dictionary of key/value pairs (defaults to one provided in this module)
    """
    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())), 
                                      flags=re.IGNORECASE|re.DOTALL)
    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match) if contraction_mapping.get(match) else contraction_mapping.get(match.lower())                       
        expanded_contraction = first_char+expanded_contraction[1:]
        return expanded_contraction
        
    expanded_text = contractions_pattern.sub(expand_match, text)
    return expanded_text

# Late in the day we realised that the contraction expansion 
# process would address things like "it's" but *not* things 
# like "the U.K.'s". In other words, we were missing possessives
# out completely, and this would result in strange post-lemma
# outputs (e.g. "uks").
possessives = re.compile(r'(?:\'[sS])(?=[\'\s,;:])', flags=re.DOTALL|re.IGNORECASE)
def remove_possessives(text):
    """
    Attempt to deal with possessives (e.g. "the UK's policy")
    so that they aren't normalised to "uks".

    text: the text from which to remove possessives
    """
    return possessives.sub(' ', text)

# This is kind of the final step to get rid of text that might
# give the NER, lemmatiser, and WE processes fits. At this point
# the only thing left should be fairly simple word, word-boundary
# stuff.
# Adapted from https://www.kdnuggets.com/2018/08/practitioners-guide-processing-understanding-text-2.html
def remove_special_chars(text:str, remove_digits:bool=False, replace_with_spaces:bool=True) -> str:
    """
    A final pass through the text to remove 'special characters'
    that have somehow evaded earlier cleaning. After this you'd 
    only expect to have alpha-numeric (with numeric optional) 
    and the base punctuation ('.', '_', '-').

    text: the text from which to remove special characters
    remove_digits: boolean determining whether or not to remove digits (default: False)
    replace_with_spaces: boolean determining whether or not substitution is ' ' or '' (default: True)
    """
    pattern = r'[^a-zA-z0-9\s\.\_\-]' if not remove_digits else r'[^a-zA-z\s\.\_\-]'
    return re.sub(pattern, ' ' if replace_with_spaces else '', text)

# Adapted from https://www.kdnuggets.com/2018/08/practitioners-guide-processing-understanding-text-2.html
global NUMBER_MAP
NUMBER_MAP = {
    'k': 1e3,
    'm': 1e6,
    'b': 1e9,
    'bn': 1e9,
    't': 1e12,
    'tn': 1e12
}

# I'm not 100% sure this adds much to our comprehension but
# it seemed like a valuable contribution at the time... this
# will convert 125k to 125000, or 12.5b to 12500000000.
formatted_nums = re.compile(r'(\d+)\s?,\s?(?=\d{3})', flags=re.DOTALL)
def expand_numbers(text:str, number_mapping=NUMBER_MAP):
    """
    Try to turn numbers into textual forma such that 125k
    becomes 125000 and so on.

    text: the text in which to expand numbers
    number_mapping: defaults to mapping provided in this module but can be specified.
    """
    number_pattern = re.compile(r'([0-9]+(\.[0-9]+)?)\s?({})(?=\.|\s)'.format('|'.join(number_mapping.keys())), 
                                      flags=re.IGNORECASE|re.DOTALL)
    
    def expand_number_match(number):
        num    = float(number.group(1).replace('..','.'))
        suffix = number.group(len(number.groups()))
        
        exp = number_mapping.get(suffix)  if number_mapping.get(suffix)  else number_mapping.get(suffix.lower())
        return str(int(num * exp))
    
    expanded_txt = number_pattern.sub(expand_number_match, formatted_nums.sub(r'\1',text))
    return expanded_txt

# Since we don't want to force lower-case unnecessarily 
# early, we want to set this up so that it's easy to
# pass through cases as part of stopword filtering.
def remove_stopwords(text, is_lower_case=False):
    """
    Remove stopwords from text that may or may not already 
    be lower-cased.

    text: the text from which to remove stopwords
    is_lower_case: Boolean indicating whether or not the text should be treated as lower-case (default: False)
    """
    tokens = wtok.tokenize(text)
    tokens = [token.strip() for token in tokens]
    if is_lower_case:
        filtered_tokens = [token for token in tokens if token not in stopword_list]
    else:
        filtered_tokens = [token for token in tokens if token.lower() not in stopword_list]
    filtered_text = ' '.join(filtered_tokens)    
    return filtered_text

# Remove punctuation -- you could remove special chars instead
# but that is a more brutal approach that loses some of the subtlety
# that we can get it if we keep phrases for learning sentence embeddings.
pk    = re.compile(r'[\(\)\[\]\|<>\\]', flags=re.DOTALL) # Punctuation we don't want to 'keep'
hy    = re.compile(r'(?:-{2,}|–|—|\s-\s)', flags=re.DOTALL) # Hyphenation ('--' and '---')
def remove_punctuation(text:str, keep_phrases:bool=True):
    """
    Remove punctuation while trying to control for issues
    of hyphenation. Doesn't apply to '.' or ',', with hyphens
    and other dashes as special cases.

    text: the text from which to strip punctuation
    keep_phrases: Boolean indicating whether to replace punctuation with ' . ' or ' '
    """
    return pk.sub(' . ' if keep_phrases else ' ', hy.sub(', ', text))

# We are basically stripping out short 'words' here
# that either have to exceed the minimum length set
# or which aren't part of the punctuation that we're
# keeping because they are part of phrase boundaries.
punkts = re.compile(r'[,;:\-!?\.\/\\]',flags=re.IGNORECASE|re.DOTALL)
def remove_short_text(doc:str, shortest_word:int=1):
    """
    We set a minimum threshold for the length of a 'word'
    or term here so that anything which has been cleaned
    almost to oblivion can be dumped at this point. 
    """
    text = re.split('\s+',doc)
    return ' '.join([x for x in text if len(x)>shortest_word or punkts.match(x)])

# More useful in texts where there are very short lines that are likely
# to be headings or other types of 'non-content' (e.g. 'Contact Us')
def remove_short_lines(doc:str, shortest_line:int=1):
    """
    Looks for things like footers and other 'non-content'
    that might detract from processing of the text as a whole.
    """
    lines = re.split(r'[\r\n]+',doc,flags=re.DOTALL|re.M)
    rv = [l for l in lines if len(re.split(r'\s',l))>shortest_line]

# Apply BS4 filtering to remove the actual HTML tags.
# But notice below that we need to do a bit of pre-processing
# so that what comes back isn't an unreadable mess thanks to
# the simple removely of all HTML.
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
def strip_html_tags(doc:str) -> str:
    """
    Simple interface to BS4's `soup.get_text()` method. You
    might prefer to use `strip_html` since that also controls
    for the way that get_text tends to remove semantically
    important whitespace as well!
    """
    soup = BeautifulSoup(doc, "html.parser")
    return soup.get_text(separator=" ")

# Remove HTML syntax but leave whatever its content was! 
# With Beautiful Soup you need to insert whitespace 
# otherwise retrieving the HTML loses all of the word
# boundaries. It is now possible to this using:
#   soup.get_text(separator=" ")
# but that may not always do what we want compared to
# a regex.
def strip_html(doc:str):
    if re.search(r'(:?<|>)',doc):
        # bs4 strips out semantically important whitespace so we need
        # to insert an extra space after end-tags.
        doc = re.sub(r'(\/[A-Za-z]+\d?|[A-Za-z]+ \/)>','\\1> ', html.unescape(doc))
        return strip_html_tags(doc)
    else:
        return doc

# Deal with some issues that accumulate over the various
# passes with different regexes and NER tools. We first 
# need a list of all of the named entities since we need
# to ensure that these remain part of the 'word' to which
# they were attached.
entities = set(['PERSON','NORP','FAC','ORG','GPE','LOC','PRODUCT','EVENT','WORK_OF_ART','LAW',
               'LANGUAGE','DATE','TIME','PERCENT','MONEY','QUANTITY','ORDINAL','CARDINAL'])
# In some cases only part of the name or entity is recognised so we get 'sharm el-/placesheik'
err   = re.compile(f"(/(?:{'|'.join(entities)}))([^\.\s]+)", flags=re.DOTALL|re.IGNORECASE)
# Artefact of the processing: '.. _' or '..' or '.._'
pkerr = re.compile(r'\.{2,}\s?\_?', flags=re.DOTALL)
# Another possible processing artefact or possible scanning output
herr  = re.compile(r'(?:-|_)+', flags=re.DOTALL)
def fix_ner_errors(doc):
    return herr.sub('_',pkerr.sub(' . ', err.sub(r'\2\1', doc)))

preamble_re = re.compile(r'^(?:[Ss]ee )?(?:for )?(?:e\.?g\.? )?;?\s*')
# Detecting likely publications -- still need to do a little work 
# to tidy up inline citations; e.g. 'Felix Guattari (2005, 2009)' is
# currently turning into Felix Guattari Felix_Guattari_2005/REF Felix_Guattari_2009/REF
# so you're getting an extra Guattari there.
def detect_publications(d):
    # Convert back to string-form if is in list (tokenised) form
    if type(d) is list: 
        d = ' '.join([' '. join([str(elem) for elem in sublist]) for sublist in d])

    refs = []

    # These are potential publications, but could just 
    # as easily be parentheticals!
    for m in re.finditer(r'\((.+?)\)',d):
        
        #print(f"=> {m.group(1)}")
        start_pos = 1
        
        if DEBUG: print(f"0. {m.group(0)}")

        for y in re.finditer(r'\d{4}(?!s)',m.group(1)):
            
            if DEBUG: print(f"\t1. '{y.group()}' ({y.start()}->{y.end()})")

            author_txt = ""
            for r in re.split(r'(?:,\s+&?\s*|\s+&\s+)',preamble_re.sub('',m.group()[start_pos:y.start()])):
                if DEBUG: print(f"\t2. '{r}'")
                if re.search('\d{4}(?!s)',r) or len(r) < 2:
                    if DEBUG: print(f"\t3. Probably an inline author reference... '{r}'")
                    d_rng = re.split(r'(?:,&)?\s+',d[d[:m.start()].rfind('.')+1:m.start()]) # range in 'd' where likely to find author
                    #print(f"\t4. => {d_rng}")
                    for i in reversed(d_rng):
                        #print(f"\t\t- {i}")
                        if len(i) > 0:
                            if re.match(r'[A-Z]',i) or i in ['von','van','the']: #len(i) < 3 or 
                                if author_txt != '':
                                    author_txt = i + '_' + author_txt
                                else:
                                    author_txt = i
                            else:
                                break
                elif len(r.split(' ')) > 4:
                    pass
                else:
                    if author_txt != '':
                        author_txt += '_'+r
                    else:
                        author_txt = r
            if author_txt != "":
                author_txt = author_txt.replace(",",'').replace(' ','_') + '_' + y.group() + "/REF"
                if DEBUG: print(f"\t- Author txt: {author_txt}")
                refs.append(author_txt.replace('.',''))
            start_pos = y.end() + 1
    
        if m.group(0).startswith('(') and m.group(0).endswith(')'):
            d = d.replace(m.group(0), ' '.join(refs))
    return d

# This probably needs more work since it's by far the slowest 
# part of the cleaning process. That said, it's also doing the
# most complex task so perhaps no optimisation is possible. 
# What we are trying to do is find named entities of various 
# sorts and then (lightly) process them in ways that are useful
# for later. So in the case of dates we remove the 'ca.' from 
# 'ca.1750' as well as 'the' or 'an' or 'a' from 'the Neolithic'
# and so on.
#
# In writing the documentation I've also realised that it doesn't
# try to attach NER tags to unigrams (if ' ' in e.text) because
# we aren't worried about those from the standpoint of learning 
# the word embeddings, whereas we *are* worried about recognising
# that 'World War II' was an event and should be learned as such
# rather than as 'World', 'War' (and the 'II' would probably be
# lost at some point later in the processing).
prefix_re = re.compile(r'^(?:the|an|a)_', re.IGNORECASE)
suffix_re = re.compile(r'[^A-Za-z0-9]+$') # Was r'[\)_]+$'
paren_re  = re.compile(r'\s*\([^\)]+\)?$')
def detect_entities(text, spacy_model):
    # Convert back to string-form if is in list (tokenised) form
    if type(text) is list: 
        text = ' '.join([' '. join([str(elem) for elem in sublist]) for sublist in text])
    
    tic = time.perf_counter()

    # Build the model based on the document
    doc = spacy_model(text)
    
    if DEBUG: spacy.displacy.render(doc, style='ent')

    toc = time.perf_counter()
    #print(f"Model created in {toc-tic:0.2f}")

    s = dict() # Create dict of substitutions

    tic = time.perf_counter()
    # Build the dictionary of substitutions by iterating
    # over the entitites detected...
    for e in doc.ents:
        if '_' not in e.text:
            try:
                stxt = ''
                if e.label_ in ['CARDINAL']:
                    # We aren't interested in keeping cardinal values
                    stxt = ''
                elif e.label_ in ['DATE']:
                    # Deal with 'c.1580', 'ca. 1795' and 'period_of_...' 
                    se = re.sub(r'ca?\.[\_]+','',
                                    re.sub(r'(?:period)_','',e.text.replace(" ","_"))
                                )
                    # Deal with all the other things that crop up 
                    # (e.g. 'the Neolithic to the Roman period (4000 BCE - 410 CE')
                    se = suffix_re.sub('',paren_re.sub('',prefix_re.sub('', se)))
                    stxt = se + "/" + e.label_
                else:
                    se = suffix_re.sub('',paren_re.sub('',prefix_re.sub('', e.text.replace(" ","_"))))
                    stxt = se + "/" + e.label_
                
                # And save the original and the substitution into the dict
                s[e.text] = stxt.replace('-_','_')
            except TypeError:
                print(f"Error processing entity: {e}")
    
    toc = time.perf_counter()
    #print(f"Dict of substitutions created in {toc-tic:0.2f}")

    # Now make the substitutions -- I have a strong suspicion
    # that this is very, very slow. Would it be better to have
    # a map (k -> v) that is applied in a list context? E.g.
    # [map(x) for x in nltk.tokenize(str)] 
    # That would require you to store things that aren't being
    # substituted as well (which is fine since these aren't long
    # documents), but if you were concerned with large docs then
    # something like:
    # [map(x) if x in map else x for x in nltk.tokenize(str)]
    tic = time.perf_counter()
    for sk in s.keys():
        # The basic assumption built into this process is
        # that we're only really interested in words > unigrams
        # so something like 'James' won't actually be registered
        # as a person because it's not particularly important 
        # that we spot this as an 'entity' compared to something
        # like 'the Uniform Dispute Resolution Policy'. However,
        # looking back at the name of this function perhaps it 
        # needs a rename since you might reasonably *think* that
        # it will give you unigram NERs as well!
        if ' ' in sk:
            try: 
                # Here we build a custom regex for the substitution
                # but notice that we need to check the NER process
                # hasn't accidentally interpolated into the middle 
                # of something we already knew about.
                pat = r'\b(?<!_)' + sk + r'(?!_)\b'
                if DEBUG: print(f"Substitution: {sk} -> {s[sk]} with {pat}")
                rs = re.compile(pat)
                d = rs.sub(s[sk], d)
            except:
                # If the pattern doesn't compile (this happens a fair
                # few times because of special characters in the origin
                # text) then we try to substitute out likely problem
                # characters by replacing them with the '.' (any char)
                # character. The only thing doesn't deal with (which 
                # seems to crop up because of poor OCR) is the accidental
                # escape (e.g. 'W' became '\V' during OCR of thesis).
                err = sys.exc_info()
                #print(f"    Exception type: {err[1]}")
                try:
                    # Basically try to substitute out anything that might give us trouble
                    pat = r'\b(?<!_)' + re.sub(r'[\(\)<>{}\$\\\+\[\]:;&\?\^~]','.',sk) + r'(?!_)\b'
                    rs = re.compile(pat)
                    d = rs.sub(s[sk], d)
                    if DEBUG: print(f"    Adjusted regex: " + pat)
                except:
                    # At this point we're dealing with a (hopefully) small number
                    # of cases where there is weirdness like '$\sim$' that does
                    # badly when trying to manage things via regex substitution
                    # composed automatically
                    print(f"    Unable to manage substitution automatically for '{sk}'")
    
    toc = time.perf_counter()
    #print(f"Substitutions completed in {toc-tic:0.2f}")
    
    return d

# Deal with likely acronyms -- I was trying to 
# develop something quite sophisticated but there
# are so many edge cases that it's probably better 
# to just tackle the basic ones and leave the rest.
# acro = re.compile(r'\b(?<!/)([A-Z]{1,}[a-z]{0,3})\.?((?:[A-Z]{1,}[a-z]{0,3}){1,4})\.?(?![_0-9\-])',flags=re.DOTALL)
# acro = re.compile(r"""\b(?<!/) # Don't accidentally match NER tags
#                       ( (?:    # Memoise these...
#                         [A-Z]{1,}[A-Za-z0-9]{0,7}\-[A-Z0-9]{2,7} | # e.g. HadGEM2-ES
#                         [A-Z]{1,}[a-z]{0,3}\.?(?:[A-Z]{1,}[a-z]{0,3}){1,4}? | # e.g. GISci, P.hD
#                         [A-Z]{3,}[A-Z0-9]*? # Easiest case: e.g. GIS, GEM2
#                        ) )""",
#                     flags=re.X|re.DOTALL)
# The above regexes also tried to interpret MacCaffrey as a 
# complex acronym so I *then* needed a 'Scottish' regex to 
# remove that interpretation... this is the point at which 
# I largely gave up on trying to detect acronyms like 
# HadGEM2-ES.
# scot = re.compile(r'\b(Ma?c\s?[A-Za-z]+)/ACRONYM([a-z]+)', flags=re.DOTALL)
#
# We should also check/deal with 'U.K.' and 'U.S.A.'...
acro = re.compile(r"""\b(?<=\s)  # Look for a proper break before
                       ( (?:     # Memoise these options... 
                            [A-Z]{1,}[a-z]{0,1}[A-Z]{1,}[a-z]*? |  # e.g. PhD or HadGEM2 or GIS
                            [A-Z\.]{3,}                            # e.g. U.K or U.S.A.s
                          )(?:s|\'s)?
                        )
                        (?=[\s\.\)\]\;\:])""", flags=re.X|re.DOTALL)
# Since this often comes _after_ NER, we can end up with acronyms
# having been assigned as part of an ORG or LAW. For example: 
# National_Water_and_Sewerage_Corporation_NWSC/ORG 
# and we want to correct this to:
# National_Water_and_Sewerage_Corporation/ORG NWSC/ACRONYM
extras = re.compile(r"""\b(?<=\s)  
                        ([A-Za-z0-9_]+?)_([A-Z]{3,})(?:s|\'s)?/([A-Z]{,6})
                        (?=\b)""", flags=re.X|re.DOTALL) # \b replaces [\s\.\)\]\;\:]
def detect_acronyms(text:str) -> str:
    """
    Detect likely acronyms and assign a (false) NER tag so that
    they aren't learned as phrases together with the rest of the
    term. 
    
    test: the text to parse for likely acronyms
    """
    #text = re.sub(r'([A-Z])s/AC',r'\1/AC',acro.sub(r'\1/ACRONYM',text))
    # I can't think of any other way to deal with this issue
    #text = scot.sub(r'\1\2',text)
    if not text or text==None or text=='':
        return ''
    else:
        return re.sub('\.(?!\s)', '', extras.sub(r'\1/\3 \2/ACRONYM', acro.sub(r'\1/ACRONYM', text)))

multiples = re.compile(r'(?:\s*\.\s*){2,}')
translate_table = dict((ord(char), None) for char in string.punctuation if char != '.')
translate_numbers = dict((ord(char), None) for char in '1234567890') 
def normalise_document(doc:str, html_stripping=True, contraction_expansion=True,
                     accented_char_removal=True, text_lower_case=True,
                     text_lemmatization=True, special_char_removal=False,
                     punctuation_removal=True, keep_sentences=True,
                     stopword_removal=True, remove_digits=False, infer_numbers=True,
                     shortest_word=3) -> str:
    """
    Apply all of the functions above to a document using their
    default values so as to demonstrate the NLP process.

    doc: a document to clean.
    """
    if DEBUG: print(f"Input:\n\t{doc}")

    try: 
        # strip HTML
        if html_stripping:
            doc = strip_html_tags(doc)
            if DEBUG: print(f"After HTML removal:\n\t{doc}")
    
        # remove extra newlines
        doc = re.sub(r'[\r|\n|\r\n]+', ' ', doc)
    
        # remove extra whitespace
        doc = re.sub('\s+', ' ', doc)
        if DEBUG: print(f"After newline and whitespace removal:\n\t{doc}")
        
        # remove quotemarks
        doc = remove_quotemarks(doc)
        
        # remove accented characters
        if accented_char_removal:
            doc = remove_accented_chars(doc)
            if DEBUG: print(f"After accent removal:\n\t{doc}")
    
        # expand contractions    
        if contraction_expansion:
            doc = expand_contractions(doc)
            if DEBUG: print(f"After contraction expansion:\n\t{doc}")
    
        # infer numbers from abbreviations
        if infer_numbers:
            doc = expand_numbers(doc)
            if DEBUG: print(f"After number expansion:\n\t{doc}")
    
        # lemmatize text
        if text_lemmatization:
            doc = lemmatise(doc)
            if DEBUG: print(f"After lemmatisation:\n\t{doc}")
    
        # lowercase the text    
        if text_lower_case:
            doc = doc.lower()
            if DEBUG: print(f"After lower-casing:\n\t{doc}")
        
        # remove special characters and\or digits    
        if special_char_removal:
            doc = remove_special_chars(doc, remove_digits)
            if DEBUG: print(f"After special char removal:\n\t{doc}")
    
        if remove_digits:
            doc = doc.translate(translate_numbers)

        # remove stopwords
        if stopword_removal:
            doc = remove_stopwords(doc, is_lower_case=text_lower_case)
            if DEBUG: print(f"After stopword removal:\n\t{doc}")
        
        # Deal with HTML entities -- not sure
        # why these aren't picked up earlier in 
        # the HTML function...
        doc = html.unescape(doc)
        
        # remove punctuation
        if punctuation_removal:
            doc = remove_punctuation(doc, keep_sentences)
            if DEBUG: print(f"After punctuation removal:\n\t{doc}")
        
        # remove short words
        if shortest_word > 1:
            doc = remove_short_text(doc, shortest_word)
            if DEBUG: print(f"After short text removal:\n\t{doc}")
        
        # Tidy up
        doc = multiples.sub(' . ', doc).translate(translate_table)

        return doc
    except TypeError as err:
        if DEBUG:
            print(f"Problems with: {doc}")
            print(err)
            #traceback.print_exc(file=sys.stdout)
        rval = doc if doc is not None else ''
        return rval