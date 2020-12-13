"""
Artificially generate Saffran's data
"""
import random 
import nltk
from nltk import Nonterminal, Production

word_list = ["tiduko", "golatu", "daropi"]# "pabiku", 
syllable_list = ["pa", "bi", "ku", "ti", "du", "ko", "go", "la", "tu", "da", "ro", "pi"] #TODO

speech_stream = [] #randomly take words from word list, split into syllables (just take 2 letters each), concatenate

def generate_speech_stream(finish_prob = None, n_words =None):
    assert n_words is None or finish_prob is None, "only use n_words when the number of words is deterministic (so no finish_prob should be defined)"
    s = ""
    i = 0
    while True:
        finish = random.random() < finish_prob if n_words is None else i >= n_words
        if finish:
            return s 
        random_word = word_list[random.randint(0, len(word_list)-1)]
        syllables = [random_word[2*i:2*i+2] for i in range(len(random_word)//2)] 
        s += " " + " ".join(syllables)
        i += 1
    # shuffled_words = random.shuffle(word_list)
    # for word in shuffled_words:

# use induce pcfg to get grammar


def get_grammar():   # TODO: How to get the probabilities, from the stream above? or is the string above only to test inference
    # grammar = nltk.PCFG.fromstring(""" 
    # Sentence -> Words [1.0]
    # Words -> Word Words [0.8] | Word [0.2]
    # Word -> Syllables [1.0]
    # Syllables -> Syllable Syllables	 [0.8] | Syllable [0.2]
    # Syllable -> 'tu' [0.083]
    # Syllable -> 'pi' [0.168]
    # Syllable -> 'ro' [0.083]
    # Syllable -> 'go' [0.083]
    # Syllable -> 'la' [0.168]
    # Syllable -> 'bu' [0.083]
    # Syllable -> 'da' [0.083]
    # Syllable -> 'ko' [0.083]
    # Syllable -> 'ti' [0.083]
    # Syllable -> 'du' [0.083] 
    # """)
    words_to_word = Production(Nonterminal("Words"), [Nonterminal("Word")])
    words_to_words = Production(Nonterminal("Words"), [Nonterminal("Word"), Nonterminal("Words")])
    syllables_to_syllable = Production(Nonterminal("Syllables"), [Nonterminal("Syllable")])
    syllables_to_syllables = Production(Nonterminal("Syllables"), [Nonterminal("Syllable"), Nonterminal("Syllables")])
    productions = [
        Production(Nonterminal('Sentence'), [Nonterminal("Words")]),
        Production(Nonterminal("Word"), [Nonterminal("Syllables")]),
    ]
    word_prob = 0.2 #probability to go words -> word 
    syllable_prob = 0.2 #probability to go syllables -> syllable 
    for _ in range(10000):
        word_alone = random.random() < word_prob
        if word_alone:
            productions.append(words_to_word)
        else:
            productions.append(words_to_words)
        syllable_alone = random.random() < syllable_prob
        if syllable_alone:
            productions.append(syllables_to_syllable)
        else:
            productions.append(syllables_to_syllables)

    # productions.append(Production(Nonterminal('Sentence')))
    for iteration in range(100):
        s = generate_speech_stream(n_words=3)
        syllables = s.split()
        for i, syllable in enumerate(syllables):
            if i < len(syllables) - 1:
                lhs = Nonterminal(f"begin_{syllable}")
                rhs = [syllable]
                new_production = Production(lhs=lhs, rhs=rhs)
                productions.append(new_production)
            
        # productions.append(generate_speech_stream(n_words=5))

    S = Nonterminal("Sentence")
    grammar = nltk.induce_pcfg(S, productions)
    print(grammar)
    return grammar 
# parse speech stream on grammar
def parse_stream(grammar, s):
    parser = nltk.parse.BottomUpChartParser(grammar)
    tokens = s.split()
    for tree in parser.parse(tokens): #TODO: Find the tree with the highest probability
        tree.pretty_print()           # From the .parse() documentation: When possible this list is sorted from most likely to least likely.
        break

if __name__ == "__main__":
    s = generate_speech_stream(n_words = 3)
    grammar = get_grammar()
    parse_stream(grammar, s)