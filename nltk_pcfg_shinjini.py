import nltk
from nltk import Nonterminal, nonterminals, Production, PCFG
from nltk import tokenize
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

pcfg_prods = grammar.productions()
print(len(pcfg_prods))
# print(grammar.productions())

parser = nltk.parse.BottomUpChartParser(grammar)
# sentence = "da ro pi go la tu"
sentence = "da tu go pi la"
tokens = sentence.split()

parsers = [
    ViterbiParser(grammar),
    pchart.InsideChartParser(grammar),
    pchart.RandomChartParser(grammar),
    pchart.UnsortedChartParser(grammar),
    pchart.LongestChartParser(grammar),
    pchart.InsideChartParser(grammar, beam_size=len(tokens) + 1)
]

for tree in parser.parse(tokens):
    tree.pretty_print()

# times = []
# average_p = []
# num_parses = []
# all_parses = {}
# for parser in parsers:
#     print('\ns: %s\nparser: %s\ngrammar: %s' % (sentence, parser, grammar))
#     parser.trace(3)
#     t = time.time()
#     parses = parser.parse_all(tokens)
#     times.append(time.time() - t)
#     if parses:
#         lp = len(parses)
#         p = reduce(lambda a, b: a + b.prob(), parses, 0.0)
#     else:
#         p = 0
#     average_p.append(p)
#     num_parses.append(len(parses))
#     for p in parses:
#         all_parses[p.freeze()] = 1
#
# # Print summary statistics
# print()
# print('-------------------------+------------------------------------------')
# print('   Parser           Beam | Time (secs)   # Parses   Average P(parse)')
# print('-------------------------+------------------------------------------')
# for i in range(len(parsers)):
#     print('%19s %4d |%11.4f%11d%19.14f' % (parsers[i].__class__.__name__,
#                                            getattr(parsers[0], "beam_size", 0),
#                                            times[i],
#                                            num_parses[i],
#                                            average_p[i]))
# parses = all_parses.keys()
# if parses:
#     p = reduce(lambda a, b: a + b.prob(), parses, 0) / len(parses)
# else:
#     p = 0
# print('-------------------------+------------------------------------------')
# print('%19s      |%11s%11d%19.14f' % ('(All Parses)', 'n/a', len(parses), p))
# print()
#
# for parse in parses:
#     print(parse)
