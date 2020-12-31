import pyswip
import re

def add_knowledge(tag, rels):
    grammar_2_add = []
    for rel in rels:
        text = 'human(tag) --> [mortal]' # prolog
        grammar_2_add.append(text)

    write_new_grammars(grammar_2_add)

def write_new_grammars(grammar):
    open('knowledge_store.pl', 'w') as f:
        content = f.lines()
        
        for g in grammar:
            re.match('grammar(*') ## find which line to add the grammar
            content = ' '.join(g)


        

