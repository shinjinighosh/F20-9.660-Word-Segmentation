# -*- coding: utf-8 -*-
"""
A simple word segment algorithm employing a viterbi algorithm.
Code adapted from Zhang Long
"""

import math
import codecs
from bigram_model import train_bigram, smoothing_pmap_wittenbell
from collections import defaultdict
import os

# train_file=".\\data\\wiki-ja-train.word"
# test_train_file=".\\data\\wiki-ja-test.txt"
train_file = os.path.join("data", "wiki-ja-train.word")
test_train_file = os.path.join("data", "wiki-ja-test.txt")

# train a unigram model
model, pmapwb = train_bigram(train_file)
model = smoothing_pmap_wittenbell(model, pmapwb)

# chinese seg using bigram model. NShort algorithm
# implemented (a.k.a Viterbi using bigram model).
# it's better to make it sentence-based instead of
# file-base.
def wordseg_bigram(model, test_file, result_file):
    best_score = []
    best_edge = []
    lines = codecs.open(test_file, 'r', 'utf-8')
    # result = codecs.open(result_file, 'w', 'utf-8')
    result = open(result_file, 'w')

    # below implemented Viterbi algorithm
    for line in lines:
        line = line.strip('\n')

        # a trick to make insert really works
        # note: insert(idx, val) always insert
        # into the last one when idx > len(list)
        best_score = [None] * len(line)
        best_edge = [None] * len(line)
        best_score.insert(0, 0.0)

        # forward step
        for word_end in range(1, len(line) + 1):
            # print(word_end)
            best_score.insert(word_end, 1e10)
            for word_begin in range(0, len(line) + 1):
                word = line[word_begin:word_end]
                if word in model:
                    prob = model[word]
                elif len(word) == 1:
                    prob = 1e-6
                else:
                    continue
                my_score = best_score[word_begin] + -math.log(prob)
                if my_score < best_score[word_end]:
                    best_score[word_end] = my_score
                    best_edge.insert(word_end, [word_begin, word_end])

        # backstep
        words = []
        # print(best_edge)
        for i in best_edge[::-1]:
            if i:
                next_edge = i
                break
        # next_edge = best_edge[len(best_edge) - 1]
        # print(next_edge)
        while next_edge:
            word = line[next_edge[0]:next_edge[1]]
            print(word)
            words.append(word)
            next_edge = best_edge[next_edge[0]]
        # print(words)
        words.reverse()
        words = ' '.join(words)
        result.write(words)
    print(words)
    result.close()


wordseg_bigram(model, test_train_file, os.path.join("test", 'mandarin_bigram_result.txt'))


def main():
    pass


if __name__ == '__main__':
    main()
