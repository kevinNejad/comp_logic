import re
from flair.data import Sentence
from flair.models import SequenceTagger

import os


import spacy
import textacy

try:
    nlp_spacy = spacy.load("en_core_web_sm")
except:
    print('spacy models and data have not been downloaded!')
    print('Downloading ...')
    os.system('python -m spacy download en_core_web_sm')
    nlp = spacy.load("en_core_web_sm")

from enum import Enum



# https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
class POS(Enum):
    DETERMINER = 'DT'
    ADVERB = 'RB'
    PROPNOUN = 'NNP'
    PROPNOUN_2 = 'PROPN'
    NOUN = 'NN'
    VERB = 'VB'
    ADJECTIVE = 'JJ'
    PREPOSITION = 'IN'
    COORD = 'CC'
    CARDINAL = 'CD'
    EXISTENTIAL = 'EX'
    FOREIGN = 'FW'
    LISTITEM = 'LS'
    MODAL = 'MD'
    PREDET = 'PDT'
    POSSESS = 'POS'
    PRONOUN = 'PRP'
    POSSPRONOUN = 'PRP$'
    PARTICLE = 'RP'
    SYMBOL = 'SYM'
    TO = 'TO'
    INTERJECTION = 'UH'
    WHDET = 'WDT'
    WHPRONOUN = 'WP'
    WHADVERB = 'WRB'

class CHUNK(Enum):
    NN='NN' # Noun
    VB='VB' # Verb

    NP='NP' # Noun Phrase
    VP='VP' # Verb Phrase

    CNP='CNP' # Custom/Complex Noun Phrase
    CVP='CVP' # Custom/Complex Verb Phrase

class Tagger():
    def __init__(self):
        self.tagger = SequenceTagger.load('pos')

    def tag(self, text):
        sentence = Sentence(text)

        # predict POS tags
        self.tagger.predict(sentence)
        tagged_sent = sentence.to_tagged_string()
        tags = re.findall(re.escape('<') + '(.*?)' + re.escape('>'),
                          tagged_sent)

        return tagged_sent, sentence.to_plain_string(), tags



# for queries, not knowledge loading
def standardise_tags(tags):
    std = []
    for tag in tags:
        if POS.DETERMINER.value in tag:
            std.append( POS.DETERMINER.value)
        elif POS.VERB.value in tag:
            std.append( POS.VERB.value)
        elif POS.ADVERB.value in tag:
            std.append( POS.ADVERB.value)
        elif POS.ADJECTIVE.value in tag:
            std.append( POS.ADJECTIVE.value)
        elif POS.NOUN.value in tag and tag != POS.PROPNOUN.value:
            std.append( POS.NOUN.value)
        else:
            std.append(tag)
    return std

def get_complex_tag(label):
    # Grammar patterns regex
    NN_pattern=[{'POS':"DET","OP":"?"},{'POS':"NOUN"}]
    #NN_pattern = r'(<DET>?<NOUN>)'
    #VB_pattern = r''

    CNP_pattern=[
            {"POS":"DET","OP":"?"},{"POS":"ADJ","OP":"?"},{"POS":"NOUN","OP":"$"},
            {"POS":"ADP","OP":"?"},{"POS":"DET","OP":"?"},{"POS":"ADJ","OP":"?"},
            {"POS":"NOUN","OP":"?"}]
    #CNP_pattern = r'(<DET>?<ADJ>?<NOUN><ADP>?<DET>?<ADJ>?<NOUN>?)'
    #CVP_patttern = r''

    spacy_doc = textacy.make_spacy_doc((text),
                                        lang='en_core_web_sm')

    noun_reg_check = extract_pos_regex(spacy_doc, NN_pattern)
    verb_reg_check = None

    CNP_reg_check = extract_pos_regex(spacy_doc, CNP_pattern)
    CVP_reg_check = extract_pos_regex(spacy_doc, CVP_pattern)

    # Return the patter that the label follows *EXACTLY*
    text_tag = exact_match({"NN": noun_reg_check, "VB": verb_reg_check,"CNP":CNP_reg_check,
        "CVP": CVP_reg_check}, text)

def exact_match(match_dict, text):
    for chunk, matches in match_dict.items():
        if len(matches) > 0: # at least one  match was found
            if matches[0].text.strip()==text.strip():
                return (chunk, text)

        return (None, None)

def extract_pos_regex(text_doc ,pattern):
    matches_ = list(textacy.extract.matches(nlp_t, verb_pattern))
    matches_
    seen_se = set()
    filtered_matches = []
    for match in sorted(matches_, key=len, reverse=True):
        s, e = match.start, match.end
        if any(s >= ms and e <= me for ms, me in seen_se):
            continue
        else:
            seen_se.add((s, e))
            filtered_matches.append(match)
    return sorted(filtered_matches, key=lambda m: m.start)
