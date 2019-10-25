import re
import operator
import random
import time

def trimTexts(text):
    # substitute "\'" to "'"
    text = re.sub("\\\'", "\'", text)
    text = re.sub("\n", " <SS> ", text)
    return text

def getNgrams(text):
    wordList = text.split(' ')

    # set unigram
    unigram = []
    for i in range(len(wordList)):
        unigram.append((wordList[i],))
    # set bigram
    bigram = []
    for i in range(len(wordList)-1):
        bigram.append((wordList[i], wordList[i+1]))
    # set trigram
    trigram = []
    for i in range(len(wordList)-2):
        trigram.append((wordList[i], wordList[i+1], wordList[i+2]))

    return unigram, bigram, trigram

def getFreqList(ngrams):
    freqList = {}
    for token in ngrams:
        if token in freqList:
            freqList[token] += 1
        else:
            freqList[token] = 1
    return freqList

def save1000ngrams(unigramFreq, bigramFreq, trigramFreq):
    fname = ['unigramFreq1000.txt', 'bigramFreq1000.txt', 'trigramFreq1000.txt']
    ngramFreq = [unigramFreq, bigramFreq, trigramFreq]
    for i in range(3):
        sortedNgramFreq = sorted(ngramFreq[i].items(),\
                        key=operator.itemgetter(1), reverse=True)
        f = open(fname[i], 'w')
        for j in range(1000):
            s = str(sortedNgramFreq[j]) + '\n'
            f.write(s)

def getMostFreqWords(ngramFreq):
    sortedNgramFreq = sorted(ngramFreq.items(),\
                    key=operator.itemgetter(1), reverse=True)
    for token in sortedNgramFreq:
        # remove '<SS>' because it is not word
        if token[0][0] == '<SS>':
            sortedNgramFreq.remove(token)
            break
    retWords = []
    [retWords.append(sortedNgramFreq[i]) for i in range(0, 3)]
    return retWords

def getMostCommons(mostFreqWords, bigram, trigram):
    bicommon = [[], [], []]; tricommon = [[], [], []]
    for i in range(3):
        # set next most common bigram
        for idx, token in enumerate(bigram):
            if token[0] == mostFreqWords[i][0][0]:
                # erase '<SS>' and add next word, and join with '_'
                if token[1] == '<SS>': word = bigram[(idx+1)%len(bigram)][1]
                else: word = token[1]
                bicommon[i].append(word)
        # set next most common trigram
        for idx, token in enumerate(trigram):
            if token[0] == mostFreqWords[i][0][0]:
                # erase '<SS>' and add next word, and join with '_'
                if token[1] == '<SS>':
                    words = token[2] + '_' + trigram[(idx+1)%len(trigram)][2]
                elif token[2] == '<SS>':
                    words = token[1] + '_' + trigram[(idx+1)%len(trigram)][2]
                else:
                    words = token[1] + '_' + token[2]
                tricommon[i].append(words)
    return bicommon, tricommon

def getMostProbableFirstWords(bigramFreq):
    sortedBigramFreq = sorted(bigramFreq.items(),\
                    key=operator.itemgetter(1), reverse=True)
    ssWord = []
    for token in sortedBigramFreq:
        if token[0][0] == '<SS>':
            ssWord.append(token)
    ret = []
    [ret.append(ssWord[i][0][1]) for i in range(0, 3)]
    return ret

def genSents(ssWord, bigramFreq, trigramFreq):
    bisent = [[], [], []]; trisent = [[], [], []]
    bisorted = sorted(bigramFreq.items(),\
                key=operator.itemgetter(1), reverse=True)
    trisorted = sorted(trigramFreq.items(),\
                key=operator.itemgetter(1), reverse=True)
    for i in range(3):
        # generate bigram sentence and compute probability
        for j in range(10):
            # generate j-th bigram sentence
            totbiToken = 0
            for token in bisorted:
                totbiToken += token[1]
            p = 1.0
            bss = []
            for token in bisorted:
                if len(bss) == 50: break
                if token[0][0] == ssWord[i]: bss.append(token)
            random.seed(time.time())
            maxRandInt = len(bss) - 1
            randNum = random.randint(0, maxRandInt)
            # set next ngram of start word and compute its probability
            for token in bisorted:
                if token == bss[randNum]:
                    p = p * (bss[randNum][1] / totbiToken)
                    break
            # if this token has '<SS>', break
            if bss[randNum][0][1] == '<SS>':
                bisent[i].append(bss[randNum][0][0])
                continue
            sent = bss[randNum][0][0]
            next = []
            totbiToken = 0
            for token in bisorted:
                if token[0][0] == bss[randNum][0][1]:
                    next.append(token)
                    totbiToken += token[1]
            while True:
                random.seed(time.time())
                randNum = random.randint(0, 9)
                if len(next) <= randNum:
                    randNum = random.randint(0, len(next)-1)
                # set next ngram and compute its probability
                for token in bisorted:
                    if token == next[randNum]:
                        p = p * (next[randNum][1] / totbiToken)
                        break
                totbiToken = 0
                # if this token has '<SS>', break
                if next[randNum][0][0] == '<SS>': break
                sent += ' ' + next[randNum][0][0]
                prev = next[randNum][0][1]
                next = []
                # next token had been prev
                for token in bisorted:
                    if token[0][0] == prev:
                        next.append(token)
                        totbiToken += token[1]
            bisent[i].append((sent, p))
        # descendant sort by probability
        bisent[i].sort(key=lambda element:element[1], reverse=True)

        # generate trigram sentence and compute probability
        for j in range(10):
            # generate j-th trigram sentence
            tottriToken = 0
            for token in trisorted:
                tottriToken += token[1]
            p = 1.0
            tss = []
            for token in trisorted:
                if len(tss) == 50: break
                if token[0][0] == ssWord[i]: tss.append(token)
            random.seed(time.time())
            maxRandInt = len(tss) - 1
            randNum = random.randint(0, maxRandInt)
            # set next ngram of start word and compute its probability
            for token in trisorted:
                if token == tss[randNum]:
                    p = p * (token[1] / tottriToken)
                    break
            # if this token has '<SS>', break
            if tss[randNum][0][0] == '<SS>':
                trisent[i].append(tss[randNum][0][0])
                continue
            elif tss[randNum][0][1] == '<SS>':
                trisent[i].append(tss[randNum][0][0] + ' ' + tss[randNum][0][1])
                continue
            sent = tss[randNum][0][0] + ' ' + tss[randNum][0][1]\
                    + ' ' + tss[randNum][0][2]
            next = []
            tottriToken = 0
            for token in trisorted:
                if token[0][0] == tss[randNum][0][1] and\
                        token[0][1] == tss[randNum][0][2]:
                    next.append(token)
                    tottriToken += token[1]
            while True:
                random.seed(time.time())
                randNum = random.randint(0, 9)
                if len(next) <= randNum:
                    randNum = random.randint(0, len(next)-1)
                # set next ngram and compute its probability
                for token in trisorted:
                    if token == next[randNum]:
                        p = p * (token[1] / tottriToken)
                        break
                # if this token has '<SS>', break
                if next[randNum][0][2] == '<SS>': break
                tottriToken = 0
                sent += ' ' + next[randNum][0][2]
                prev1 = next[randNum][0][1]
                prev2 = next[randNum][0][2]
                next = []
                # next token had been prev
                for token in trisorted:
                    if token[0][0] == prev1 and token[0][1] == prev2:
                        next.append(token)
                        tottriToken += token[1]
            trisent[i].append((sent, p))
        # descendant sort by probability
        trisent[i].sort(key=lambda element:element[1], reverse=True)
    return bisent, trisent
