class Lexicon:
    """
    Represents either an 1-gram, 2-gram, 3-gram
    """
    def __init__(self):
        self.words_freq = dict() #words -> frequency
    def size(self):
        """
        Represents number of unique i-th grams 
        In the paper it's N_i
        """
        return len(self.words_freq) 
    def frequency(self, w):
        if w not in self.words_freq:
            return 0 
        return self.words_freq[w] 
    def sumFrequencies(self):
        """
        Represent the number of words (counting repetition) seen so far
        In the paper it's S_i
        """
        return sum(val for val in self.words_freq.values())
    def update_word(self, word):
        if word not in self.words_freq:
            self.words_freq[word] = 0
        self.words_freq[word]+=1
        return 

all_phonemes_divided = {
    "V": ["I", "E", "&", "A", "a", "O", "U", "6", "i", "e", "9", "Q", "u", "o", "7", "3", "R", "#", "%", "*", "(", ")", "L", "~", "M"], # vowels
    "C": ["p", "b", "m", "t", "d", "n", "k", "g", "N", "f", "v", "T", "D", "s", "z", "S", "Z", "h", "c", "G", "l", "r", "y", "w", "W"]  # consonants
}
all_phonemes = all_phonemes_divided["V"] + all_phonemes_divided["C"] 

class Phonemes:
    def __init__(self):
        self.map = {phoneme: 1 for phoneme in all_phonemes} #initially uniform
    def relativeFrequency(self, phoneme):
        assert phoneme in self.map, f"{phoneme} is not a valid phoneme!"
        return self.map[phoneme]/ sum(val for val in self.map.values())
    def update_phoneme(self, phoneme):
        assert phoneme in self.map, f"{phoneme} is not a valid phoneme!"
        self.map[phoneme]+=1
        # print(self.map)