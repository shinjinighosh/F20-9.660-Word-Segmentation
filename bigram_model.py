# -*- coding: utf-8 -*-
"""
A Bigram Language model implementation.
Code adapted from Zhang Long
"""

import codecs
import math
from collections import defaultdict
import os

N=1000000
# train_file=".\\data\\wiki-en-train.word"
# testtrain_file=".\\data\\wiki-en-test.txt"
# testtest_file=".\\test\\01-test-input.txt"

train_file = os.path.join("data", "wiki-en-train.word")
testtrain_file= os.path.join("data", "wiki-en-test.txt")
testtest_file = os.path.join("test", "01-test-input.txt")

def witten_bell(u,c):
    return 1-float(u)/float(c+u)

def get_wmap_key(wmap_context_key):
    keylist = wmap_context_key.split(" ")
    return keylist[0]
    
def train_bigram(file_name):
    wmap={}
    wmap_context={}
    pmap={}
    # to calculate wittenbell smoothing lambda
    map_witten_bell_u=defaultdict(set)
    map_witten_bell_c=defaultdict(list)
    pmap_witten_bell={}
    wmap_context['ttitem'] = 0
    
    with codecs.open(file_name,'r', 'utf-8') as lines:
        for line in lines:
            line=line.strip('\n')
            words=line.split(' ')
            words.insert(0,'<s>')
            words.append('</s>')
            
            if words[0] in wmap_context:
                wmap_context[words[0]] += 1
            else:
                wmap_context[words[0]] = 1
            wmap_context['ttitem'] += 1
            
            for i in range(1,len(words)):
                if words[i] in wmap_context:
                    wmap_context[words[i]] +=1
                else:
                    wmap_context[words[i]] = 1
                wmap_context['ttitem'] += 1
                
                word2=words[i-1] + ' ' + words[i]
                if word2 in wmap:
                    wmap[word2] += 1
                else:
                    wmap[word2] =1
                
                #prepare for witten-bell
                map_witten_bell_u[words[i-1]].add(words[i])
                map_witten_bell_c[words[i-1]].append(words[i])
                    
    for word in map_witten_bell_u:
        pmap_witten_bell[word] = witten_bell(len(map_witten_bell_u[word]), \
                        len(map_witten_bell_c[word]))
    
    for key_ in wmap:
        key_context = get_wmap_key(key_)
        pmap[key_] = float(wmap[key_])/float(wmap_context[key_context])
        pmap[key_context] = float(wmap_context[key_context])/float(wmap_context['ttitem'])
    
    # print(pmap)
    return pmap, pmap_witten_bell

# pmap contains both 1-gram and 2-gram
# treat them in different way
def smoothing_pmap_wittenbell(pmap, pmap_witten_bell):
    for item in pmap:
        words = item.split(" ")
        if len(words) > 1:
            word = words[0]
            lm=pmap_witten_bell[word]
            pmap[' '.join(words)] = lm*pmap[' '.join(words)] + (1-lm)*pmap[word]
        else:
            word = words[0]
            lm=pmap_witten_bell[word]
            pmap[word]=lm*pmap[word] + (1-lm)*float(1/float(N))
        
    return pmap

#test-bigram
def test_bigram(pmap, file_name):
    entropy=0
    num_words=0
    with codecs.open(file_name, 'r', 'utf-8') as test_file:
        for line in test_file:
            line = line.strip('\n')
            words=line.split(' ')
            words.insert(0, '<s>')
            words.append('</s>')
            for i in range(1, len(words)):
                word2=words[i-1] +' '+words[i]
                
                #unknown words sequence
                if word2 in pmap:
                    entropy += -math.log2(pmap[word2])
                else:
                    if words[i-1] in pmap:
                        entropy+= -math.log2(pmap[words[i-1]])
                    else:
                        entropy+= -math.log2(1/float(N))
                    if words[i] in pmap:
                        entropy+= -math.log2(pmap[words[i]])
                    else:
                        entropy+=-math.log2(1/float(N))
                num_words+=1
                
    return entropy/float(num_words)

pmap, pmap_wb = train_bigram(train_file)
pmap = smoothing_pmap_wittenbell(pmap, pmap_wb)
# print(test_bigram(pmap, testtrain_file))


def main():
  pass
  # Any code you like

if __name__ == '__main__':
  main()