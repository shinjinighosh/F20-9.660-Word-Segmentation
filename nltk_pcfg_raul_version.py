import nltk
from nltk import Nonterminal, nonterminals, Production, PCFG, induce_pcfg
from nltk import tokenize
from nltk.corpus import treebank 
from nltk.parse import pchart
from nltk.parse import ViterbiParser
import sys
import time
from functools import reduce

grammar = PCFG.fromstring("""
Sentence -> Words [1.0]
Words -> Word Words [0.8] | Word [0.2]
Word -> Syllables [1.0]
Syllables -> Syllable Syllables	 [0.8] | Syllable [0.2]
Syllable -> 'tu' [0.083]
Syllable -> 'pi' [0.168]
Syllable -> 'ro' [0.083]
Syllable -> 'go' [0.083]
Syllable -> 'la' [0.168]
Syllable -> 'bu' [0.083]
Syllable -> 'da' [0.083]
Syllable -> 'ku' [0.083]
Syllable -> 'ti' [0.083]
Syllable -> 'do' [0.083]
""")

S = Nonterminal('S')
productions = []
for item in treebank.fileids()[:2]:
  for tree in treebank.parsed_sents(item):
    # perform optional tree transformations, e.g.:
    tree.collapse_unary(collapsePOS = False)# Remove branches A-B-C into A-B+C
    tree.chomsky_normal_form(horzMarkov = 2)# Remove A->(B,C,D) into A->B,C+D->D
    productions += tree.productions()

grammar = induce_pcfg(S, productions)
print(grammar)

pcfg_prods = grammar.productions()
print(len(pcfg_prods))
# print(grammar.productions())

parser = nltk.parse.BottomUpChartParser(grammar)
sentence = "da ro pi go la tu"
tokens = sentence.split()

parsers = [
    ViterbiParser(grammar),
    # pchart.InsideChartParser(grammar),
    pchart.RandomChartParser(grammar),
    # pchart.UnsortedChartParser(grammar),
    # pchart.LongestChartParser(grammar),
    # pchart.InsideChartParser(grammar, beam_size=len(tokens) + 1)
]
# tree = parser.parse(tokens)[0]
# tree.pretty_print()

# for tree in parsers[1].parse(tokens):
#     tree.pretty_print()
#     break