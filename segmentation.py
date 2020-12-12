from math import log

class Segmentation:
    def __init__(self):
        pass 
    def evalUtterance(self, u):
        n = len(u) - 1
        bestSegPoint = n 
        bestScore = self.evalWord(u)
        for i in range(n):
            subUtterance = u[:i+1]
            word = u[i+1:]
            score = self.evalUtterance(subUtterance) + self.evalWord(word)
            if score < bestScore:
                bestScore = score
                bestSegPoint = i
        
        self.insertWordBoundary(u, bestSegPoint)
        return bestScore
    def evalWord(self, w):
        score = 0 
        if self.lexicon.frequency(w) == 0:
            escape = self.lexicon.size() / (self.lexicon.size() + self.lexicon.sumFrequencies())
            P_0 = phonemes.relativeFrequency("#")
            score = -log(escape) -log(P_0/(1-P_0))
            for i in range(len(w)):
                score -= log(phonemes.relativeFrequency(w[i]))
        else:
            P_w = self.lexicon.frequency(w) / (self.lexicon.size() + self.lexicon.sumFrequencies())
            score = -log(P_w)
        return score
    def insertWordBoundary(self, u, bestSegPoint):
        pass 

