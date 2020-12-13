"""
Artificially generate Saffran's data
"""
import random 
import nltk 

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
    grammar = nltk.PCFG.fromstring(""" 
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
    Syllable -> 'ko' [0.083]
    Syllable -> 'ti' [0.083]
    Syllable -> 'du' [0.083] 
    """)
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