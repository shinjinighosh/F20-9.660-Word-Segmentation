from math import log
from helper_classes import Lexicon, Phonemes


class Segmentation:
    def __init__(self):
        self.lexicon = Lexicon()
        self.phonemes = Phonemes()
        pass

    def start(self, utterances):
        for utterance in utterances:
            bestScore, bestUtterance = self.evalUtterance(utterance)
            print(f"\nFor #{utterance}#, the segmentation is #{bestUtterance}# with a score of {bestScore} \n")
            # print(self.lexicon.words_freq)
        print("Finished going through the corpus!")

    def evalUtterance(self, u):
        self.store = dict()
        bestScore, bestUtterance = self._evalUtterance(u)
        self.store.clear()
        self.update_lexicon(bestUtterance)
        self.update_phonemes(bestUtterance)
        return bestScore, bestUtterance

    def _evalUtterance(self, u):
        if len(u) > 3:
            return float('inf'), u
        if u in self.store:
            return self.store[u]
        print("evaluating for :", u)
        # print()
        # if len(u) == 0:
        #     return float('inf'), ""
        n = len(u) - 1
        print(n)
        bestSegPoint = n
        bestScore = self.evalWord(u)
        print(f"initial best score: {bestScore}")
        bestUtterance = u
        for i in range(n):  # finding the segmenttion with smallest score
            subUtterance = u[:i + 1]
            word = u[i + 1:]
            prev_score, prev_subUtterance = self._evalUtterance(subUtterance)
            score = prev_score + self.evalWord(word)
            print(f"Trying {subUtterance}//{word}")
            print(score)
            if score < bestScore:
                # print("UAU")
                bestScore = score
                bestSegPoint = i
                bestUtterance = prev_subUtterance + "#" + word  # inserting word boundary
        # new_utterance = 
        self.store[u] = bestScore, bestUtterance
        # print(self.store)
        return bestScore, bestUtterance

    # def _evalUtterance(self, u):
    #     n = len(u) - 1
    #     bestCost = [0 for _ in range(n+1)]
    #     previousBoundary = [None for _ in range(n+1)]
    #     for i in range(n-1):
    #         bestCost[i] = self.evalWord(u[:i+1])
    #         previousBoundary[i]-=1
    #         for j in range()

    def evalWord(self, w):
        # return 0
        score = 0
        if self.lexicon.frequency(w) == 0:  # unseen
            if self.lexicon.size() + self.lexicon.sumFrequencies() == 0:  # first utterance
                print("empty")
                return float('inf')
            escape = self.lexicon.size() / (self.lexicon.size() + self.lexicon.sumFrequencies())
            P_0 = self.phonemes.relativeFrequency("#")
            score = -log(escape) - log(P_0 / (1 - P_0))
            for i in range(len(w)):
                if w[i] != " ":
                    score -= log(self.phonemes.relativeFrequency(w[i]))
        else:  # already seen
            P_w = self.lexicon.frequency(w) / (self.lexicon.size() + self.lexicon.sumFrequencies())
            score = -log(P_w)
        return score

    def update_lexicon(self, new_utterance):
        all_words = new_utterance.split("#")
        for word in all_words:
            self.lexicon.update_word(word)
        return

    def update_phonemes(self, new_utterance):
        for char in new_utterance:
            if char != " ":
                self.phonemes.update_phoneme(char)
    # def insertWordBoundary(self, u, bestSegPoint):


if __name__ == "__main__":
    seg = Segmentation()
    utterances = [
        "yu l9k D6 blaks",
        "se blaks",
        "WAts DIs &lIs",
        "6 blak 6 blak",
        "lUk &t D&t dali",
        "WAt du yu TINk 6v D&t dali",
        "&lIs kAm h(",
        "6 bEtR wAn",
        "wAn D&t wIl fl&p",
        "In D6 briz",
        "kAm h( 9 want yu tu sIt Ap h( f% GAst 6",
        "mInIt",
        "9 want tu So yu sAmTIN",
        "lUk",
        "du yu rImEmbR DIs",
        "h(z 6 pApIt",
        "hElo &lIs",
        "hQ # yu",
        "wan6 pEt mi",
        "yu dont l9k It",
        "oke",
        "kOl d&di an D6 tEl6fon",
        "yu du D&t",
        "D&ts r9t",
        "nQ pIk Ap D6 tEl6fon &nd se hElo",
        "hElo d&di",
        "y&",
        "gUd",
        "WAts D&t",
        "D&ts 6 lItL t7 dali"
    ]
    seg.start(utterances)
