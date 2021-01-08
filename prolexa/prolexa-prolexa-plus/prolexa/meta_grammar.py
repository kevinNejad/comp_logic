import contractions
import os
import re

from enum import Enum

from prolexa import PACKAGE_PATH, PROLOG_PATH

#from common_sense import add_rules, fetch_standard_input
from utils import Tagger, POS, standardise_tags, remove_punctuation, lemmatise,is_plural

PROLOG_DET_REGEX = r'determiner\([a-z],X=>B,X=>H,\[\(H:-B\)\]\)(.*)'
PROLOG_DET = 'determiner(p,X=>B,X=>H,[(H:-B)]) --> [{}].\n'

# PartsOfSpeech

tagger = Tagger()

def initialise_prolexa(pl):
    #pl.consult(os.path.join(PROLOG_PATH, 'prolexa.pl'))
    pl.consult(os.path.join(PACKAGE_PATH, 'prolexa.pl'))

def update_knowledge_store(pl):
    list(pl.query('make'))

def reset_grammar():
    lines = get_prolog_grammar(PROLOG_PATH, 'prolexa_grammar.pl')
    write_new_grammar(PACKAGE_PATH, lines)

    lines = get_prolog_grammar(PROLOG_PATH, 'prolexa.pl')
    write_new_prolexa(PACKAGE_PATH, lines)

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


def escape_and_call_prolexa(pl, text):
    update_rules(tagger, text)
    #update_knowledge_store(pl)
    initialise_prolexa(pl)

    libPrefix = 'prolexa:'
    generator = pl.query(libPrefix + handle_utterance_str(text))
    return list(generator)


def handle_utterance_str(text):
    if text[0] != "'" and text[0] != '"' :
        text = f'"{text}"'

    text = text.replace('"', '\"')
    text = text.replace("'", '\"')

    return 'handle_utterance(1,{},Output)'.format(text)


def standardised_query(pl, text):
    text = remove_punctuation(text)
    text = contractions.fix(text)
    text = lemmatise(text)
    #fetch_standard_input(pl, text)
    return escape_and_call_prolexa(pl, text)


def get_tags(tagger, text):
    _, _, tags = tagger.tag(text)
    tags = standardise_tags(tags)
    print('TAGS: ', tags)
    return tags

def handle_noun(lines, i, text, tags):
    nn = POS.NOUN.value
    start = 'pred('
    end = ', '
    exists = False
    new_line = ''
    input_word = text[tags.index(nn)]
    _, input_word = is_plural(input_word)
    text[tags.index(nn)] = input_word

    for noun_idx, noun_line in enumerate(lines[i:]):
        if not(re.match(r'pred\((.*)[1],\[(.*)\]\)\.', noun_line)):
            noun_idx = noun_idx + i
            if tags:
                tags.remove(nn)
            if text:
                text.remove(input_word)
            break

        line_word = (noun_line.split(start))[1].split(end)[0]
        if input_word == line_word:
            if (re.match(r'pred\((.*)[1](.*)n\/(.*)\]\)\.', noun_line)):
                exists = True
                if tags:
                    tags.remove(nn)
                if text:
                    text.remove(input_word)
                break
            else:
                noun_idx = noun_idx + i
                insert_idx = noun_line.index(']).')
                new_line = (noun_line[:insert_idx]
                            + ',n/'
                            + input_word
                            + noun_line[insert_idx:])
                lines[noun_idx] = new_line
                exists = True
                if tags:
                    tags.remove(nn)
                if text:
                    text.remove(input_word)
                break

    if not exists:
        if new_line == '':
            new_line = 'pred(' + input_word + ', 1,[n/' + input_word + ']).\n'
        lines.insert(noun_idx, new_line)
        

    return lines

def handle_adjective(lines, i, text, tags):
    a = POS.ADJECTIVE.value
    start = 'pred('
    end = ', '
    exists = False
    new_line = ''
    input_word = text[tags.index(a)]
    _, input_word = is_plural(input_word)
    text[tags.index(a)] = input_word

    for noun_idx, noun_line in enumerate(lines[i:]):
        if not(re.match(r'pred\((.*)[1],\[(.*)\]\)\.', noun_line)):
            noun_idx = noun_idx + i
            if tags:
                tags.remove('JJ')
            if text:
                text.remove(input_word)
            break
        line_word = (noun_line.split(start))[1].split(end)[0]
        if input_word == line_word:
            if (re.match(r'pred\((.*)[1](.*)a\/(.*)\]\)\.', noun_line)):
                exists = True
                if tags:
                    tags.remove(a)
                if text:
                    text.remove(input_word)
                break
            else:
                noun_idx = noun_idx + i
                insert_idx = noun_line.index(']).')
                new_line = (noun_line[:insert_idx]
                            + ',a/'
                            + input_word
                            + noun_line[insert_idx:])
                lines[noun_idx] = new_line
                exists = True
                if tags:
                    tags.remove(a)
                if text:
                    text.remove(input_word)
                break

    if not exists:
        if new_line == '':
            new_line = 'pred(' + input_word + ', 1,[a/' + input_word + ']).\n'
        lines.insert(noun_idx, new_line)

    return lines

def handle_verb(lines, i, text, tags):
    v = POS.VERB.value
    start = 'pred('
    end = ', '
    exists = False
    new_line = ''
    input_word = text[tags.index(v)]
    _, input_word = is_plural(input_word)
    text[tags.index(v)] = input_word

    for noun_idx, noun_line in enumerate(lines[i:]):
        if not(re.match(r'pred\((.*)[1],\[(.*)\]\)\.', noun_line)):
            noun_idx = noun_idx + i
            if tags:
                tags.remove(v)
            if text:
                text.remove(input_word)
            break

        line_word = (noun_line.split(start))[1].split(end)[0]
        if input_word == line_word:
            if (re.match(r'pred\((.*)[1](.*)v\/(.*)\]\)\.', noun_line)):
                exists = True
                if tags:
                    tags.remove(v)
                if text:
                    text.remove(input_word)
                break
            else:
                noun_idx = noun_idx + i
                insert_idx = noun_line.index(']).')
                new_line = (noun_line[:insert_idx]
                            + ',v/'
                            + input_word
                            + noun_line[insert_idx:])
                lines[noun_idx] = new_line
                exists = True
                if tags:
                    tags.remove(v)
                if text:
                    text.remove(input_word)
                break

    if not exists:
        if new_line == '':
            new_line = 'pred(' + input_word + ', 1,[v/' + input_word + ']).\n'
        lines.insert(noun_idx, new_line)

    return lines

def handle_proper_noun(lines, i, text, tags):
    prop = POS.PROPNOUN.value
    start = '--> ['
    end = ']'
    exists = False
    input_word = text[tags.index(prop)]
    for det_idx, det_line in enumerate(lines[i:]):
        if not(re.match(r'proper_noun\(s(.*) -->(.*)\]\.', det_line)):
            det_idx = det_idx + i
            if tags:
                tags.remove(prop)
            if text:
                text.remove(input_word)
            break
        line_word = (det_line.split(start))[1].split(end)[0]
        if input_word == line_word:
            exists = True
            if tags:
                tags.remove(prop)
            if text:
                text.remove(input_word)
            break

    if not exists:
        new_line = 'proper_noun(s,{}) --> [{}].\n'.format(
            input_word, input_word)
        lines.insert(det_idx, new_line)

    return lines

def update_rules(tagger, text):
    tags = get_tags(tagger, text)
    text = text.lower()
    # Handle extra whitespace
    text = ' '.join(text.split()).split(' ')
    start = ''
    end = ''
    lines = get_prolog_grammar(PACKAGE_PATH, 'knowledge_store.pl')

    for idx, line in enumerate(iter(lines)):
        if not text:
            break

        pred_match = r'pred\((.*)[1],\[(.*)\]\)\.'

        if (POS.NOUN.value in tags) and re.match(pred_match, line):
            lines = handle_noun(lines, idx, text, tags)

        if (POS.ADJECTIVE.value in tags) and re.match(pred_match, line):
            lines = handle_adjective(lines, idx, text, tags)

        if (POS.VERB.value in tags) and re.match(pred_match, line):
            lines = handle_verb(lines, idx, text, tags)

        prop_match = r'proper_noun\(s(.*) -->(.*)\]\.'

        if (POS.PROPNOUN.value in tags) and re.match(prop_match, line):
            lines = handle_proper_noun(lines, idx, text, tags)

    write_new_grammar(PACKAGE_PATH, lines)
