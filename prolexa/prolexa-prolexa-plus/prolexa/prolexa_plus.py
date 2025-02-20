#! /usr/bin/env python

import os

from cmd import Cmd
from pyswip import Prolog

# import warnings
# warnings.filterwarnings("ignore")

import prolexa.meta_grammar as meta
import prolexa.common_sense as cs
pl = Prolog()

class ProlexaPlus(Cmd):
    intro = 'Hello! I\'m ProlexaPlus! Tell me anything, ask me anything.'
    prompt = '> '
    file = None

    def default(self, input_):
        first_answer = meta.standardised_query(pl, input_)[0]['Output']
        message = cs.standardised_query(pl, input_)
        print(first_answer)
        print(message)

def prolexa_plus_repl():
    meta.reset_grammar()
    meta.initialise_prolexa(pl)
    ProlexaPlus().cmdloop()

if __name__ == '__main__':
    prolexa_plus_repl()
