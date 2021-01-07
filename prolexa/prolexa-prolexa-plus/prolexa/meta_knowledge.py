import contractions
import os
import re
import string
import requests


from enum import Enum
from prolexa import PACKAGE_PATH, PROLOG_PATH
from utils import Tagger, POS, standardise_tags, get_complex_tag

PROLOG_DET_REGEX = r'determiner\([a-z],X=>B,X=>H,\[\(H:-B\)\]\)(.*)'
PROLOG_DET = 'determiner(p,X=>B,X=>H,[(H:-B)]) --> [{}].\n'


API_URI = 'http://api.conceptnet.io/'
EN = 'en'


class REL(Enum):
    IS_A = 'IsA'
    HAS_A = 'HasA'
    PART_OF = 'PartOF'
    USED_FOR = 'UsedFor'
    CAPABLE_OF = 'CapableOf'
    AT_LOCATION = 'AtLocation'
    CAUSES = 'Causes'
    HAS_PROPERTY = 'HasProperty'
    DESIRES = 'Desires'
    CREATED_BY = 'CreatedBy'
    CAUSES_DESIRE = 'CausesDesire'
    MADE_OF = 'MadeOf'

RELATIONS = [REL.IS_A, REL.HAS_A, REL.PART_OF, REL.USED_FOR,
        REL.CAPABLE_OF, REL.AT_LOCATION, REL.CAUSES,
        REL.HAS_PROPERTY, REL.DESIRES, REL.CREATED_BY,
        REL.CAUSES_DESIRE, REL.MADE_OF]


tagger = Tagger()

def get_prolog_grammar(path, fname):
    with open(os.path.join(path, fname), 'r') as f:
        lines = f.readlines()
    return lines

def write_new_grammar(path, lines):
    with open(os.path.join(path, 'knowledge_store.pl'), 'w') as f:
        lines = ''.join(lines)
        f.write(lines)

def write_new_prolexa(path, lines):
    with open(os.path.join(path, 'prolexa.pl'), 'w') as f:
        lines = ''.join(lines)
        l = lines.replace('consult(prolexa_engine)',
                          'consult(prolog/prolexa_engine)')
        l = l.replace('consult(prolexa_grammar)',
                      'consult(knowledge_store)')
        f.write(l)

def initialise_prolexa(pl):
    #pl.consult(os.path.join(PROLOG_PATH, 'prolexa.pl'))
    pl.consult(os.path.join(PACKAGE_PATH, 'prolexa.pl'))


def fetch_standard_input(pl, input_):
    update_knowledge(tagger, input_)
    # Get tag for each word
    # Get info for noun ones
    # 
    pass

def get_tags(tagger,text):
    _, _, tags = tagger.tag(text)
    tags = standardise_tags(tags)
    return tags

def update_knowledge(tagger, text):

    tags = get_tags(tagger, text)
    text = ' '.join(text.split()).split(' ')
    tag_text_pair = list(zip(tags, text))
    
    add_new_rules(tag_text_pair, RELATIONS)
    #print('TEXT:', text)
    #print('TAGS: ', tags)
    #print('tag_text_dict: ', tag_text_pair)

def add_new_rules(tag_text_pair, relations):
    for tag, text in tag_text_pair:
        if tag == POS.NOUN:
            add_noun_rules(input_word, relations)



def generate_rule(label, complex_tag):
    rule="stored_rule(1,[(mortal(X):-human(X))])."
    pass


def add_noun_rules(input_word, relations):
    conceptNet_knowledge = fetch_word_info(input_word, relations)
    rules = []
    predicates = []
    for rel, labels in conceptNet_knowledge.items():
        if rel == REL.IS_A:
            # Supported Phrases: Adjective, Noun, NounPhrase, VerbPhrase
            for label in labels:
                complex_tag = get_complex_tag(label)
                rule = generate_rule(label, complex_tag)
                rules.append(rule)
                #stored_rule(1,[(human(peter):-true)]).


        elif rel == REL.HAS_A:
            for label in labels:
                rule='[]'
                rules.append(rule)


def fetch_word_info(target, relations):
    data={}
    for rel in relations:
        query = 'query?start=/c/{}/{}&rel=/r/{}&limit=1000'.format(EN,target,rel)
        obj = requests.get(API_URI+query).json()
        
        # check if such a relation exist
        if len(obj['edges']) == 0:
            continue
        info = extract_info(obj)
        data[rel] = info
    return data

def extract_info(obj):
    labels = []
    for edge in obj['edges']:
        labels.append(edge['end']['label'])
        
    return labels
