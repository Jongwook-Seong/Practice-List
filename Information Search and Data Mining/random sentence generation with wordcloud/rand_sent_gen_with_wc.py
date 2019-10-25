from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import operator
import random
import time

# set encoding type of file
def KS_or_UTF8(filename):
    f = open(filename, 'rb')
    data = f.read(10)
    if bytes([data[0] & b'\xf0'[0]]) == b'\xe0' and\
            bytes([data[1] & b'\xc0'[0]]) == b'\x80' and\
            bytes([data[2] & b'\xc0'[0]]) == b'\x80':
        # UTF-8
        return 'utf-8'
    else:
        # CP949 (KSC5601)
        for i in range(10):
            if data[i] >= b'\xb0'[0] and data[i] <= b'\xc8'[0] and\
                    data[i+1] >= b'\xa1'[0] and data[i+1] <= b'\xfe'[0]:
                return 'cp949'

def readFile(filename, codeType):
    with open(filename, 'r', encoding='cp949', newline='\n') as f:
        file = f.read()
    text = ''.join(file)
    return text

# delete needless ngram words like ('', '', '') ...
def deleteNeedlessNgrams(ngrams, numGram):
    needlessValue = [(''), ('', ''), ('', '', ''),\
                    ('', '', '', ''), ('', '', '', '', '')]
    for i in range(0, numGram):
        if needlessValue[i] in ngrams:
            ngrams.remove(needlessValue[i])

    if numGram == 1 or numGram == 2:
        pass
    else:
        todel = []
        for i in range(0, len(ngrams) - 1):
            for j in range(1, numGram - 1):
                if ngrams[i][j] == '' or ngrams[i][j] is None:
                    todel.append(ngrams[i])
                    break
        for todelItem in todel:
            ngrams.remove(todelItem)
    if ('',) in ngrams:
        ngrams.remove(('',))
    if ('', '',) in ngrams:
        ngrams.remove(('', '',))

    return ngrams;

def word_ngram(text, numGram):
    # in the case a file is given, remove excape characters
    text = text.replace('\n', ' ').replace('\r', ' ')
    sentences = tuple(text.split(' '))
    ngrams = [sentences[x : x + numGram] for x in range(0, len(sentences))]
    # set '' to next word of end point
    if numGram > 1:
        for idx, words in enumerate(ngrams):
            lstwords = list(words)
            for i in range(0, numGram):
                if i >= len(words): continue
                if words[i] == '': continue
                if words[i][-1] == '.' and i < numGram - 1:
                    lstwords[i + 1] = ''
                    ngrams[idx] = tuple(lstwords)
                    break
    # return to core ngram words which is deleted needless words
    ngrams = deleteNeedlessNgrams(ngrams, numGram)
    return tuple(ngrams)

def makeFreqList(ngrams):
    freqList = {}
    for ngram in ngrams:
        if ngram in freqList:
            freqList[ngram] += 1
        else:
            freqList[ngram] = 1
    return freqList;

def genNgramWC(ngrams, numGram):
    text = ""
    for wordx in ngrams:
        xto_word = ''
        for x in wordx:
            if x == '': continue
            xto_word = xto_word + x
            if numGram > 1 and len(wordx) > 1:
                if x != wordx[-1] and \
                        not (x == wordx[-2] and wordx[-1] == ''):
                    xto_word += '_'
        text += (xto_word + ' ')
    stopwords = set(STOPWORDS)
    font_path = './NanumGothic.ttf'
    wc = WordCloud(width=1000, height=800, background_color='white',\
                    stopwords=stopwords, font_path=font_path,\
                    min_font_size=10).generate(text)
    return wc

# make frequency lists and word clouds from unigram to n-gram
def make_Ngrams_and_NgramFreqList_and_WordCloud(text, numGram):
    ngrams = {}
    ngramFreqList = {}
    ngramwc = {}
    for n in range(1, numGram + 1):
        ngrams[n] = word_ngram(text, n)
        ngramFreqList[n] = makeFreqList(ngrams[n])
        ngramwc[n] = genNgramWC(ngrams[n], n)
    return ngrams, ngramFreqList, ngramwc

def showNgramWordClouds(ngramWordCloud, numGram):
    ngramName = ['Unigram', 'Bigram', 'Trigram', 'Fourgram', 'Fivegram']

    for n in range(1, numGram + 1):
        fig = plt.figure(num=n, figsize=(10, 8))
        plt.imshow(ngramWordCloud[n])
        plt.axis('off')
        plt.title(ngramName[n-1] + ' Word Cloud')
        plt.show()
        fig.savefig(ngramName[n-1] + 'WordCloud.png', dpi=900)

def freqDescSort(ngramFreqList, numGram):
    sortedNgramFreqList = []
    tempDict = {}
    for n in range(1, numGram + 1):
        tempDict = sorted(ngramFreqList[n].items(),\
                        key=operator.itemgetter(1), reverse=True)
        sortedNgramFreqList.insert(n, tempDict)
    return sortedNgramFreqList

def genRandSentence(ngrams, numGram):
    ngramSentence = []
    ngramSentence.append('')
    for n in range(1, numGram + 1):
        random.seed(time.time())
        ngramSentence.append('')

        if n == 1:
            maxRandInt = len(ngrams[n]) - 1
            while (True):
                randNum = random.randint(0, maxRandInt)
                if ngrams[n][randNum][0] != '':
                    ngramSentence[n] += (ngrams[n][randNum][0] + ' ')
                    if ngrams[n][randNum][0][-1] == '.':
                        break
        else:
            nextWord = []
            for word in ngrams[n]:
                if word[0] == '' and word[1] != '':
                    nextWord.append(word)
            maxRandInt = len(nextWord) - 1
            randNum = random.randint(0, maxRandInt)

            if n == 2:
                ngramSentence[n] += (nextWord[randNum][1] + ' ')

                while (True):
                    if nextWord[randNum][1] == '':
                        break
                    if nextWord[randNum][1][-1] == '.':
                        break

                    preWord = nextWord[randNum][1]
                    nextWord = []
                    for word in ngrams[n]:
                        if word[0] == preWord:
                            nextWord.append(word)
                    maxRandInt = len(nextWord) - 1
                    randNum = random.randint(0, maxRandInt)
                    ngramSentence[n] += (nextWord[randNum][1] + ' ')
            elif n == 3:
                ngramSentence[n] += (nextWord[randNum][1] + ' '\
                                        + nextWord[randNum][2] + ' ')

                while (True):
                    if nextWord[randNum][2] == '':
                        break
                    if nextWord[randNum][2][-1] == '.':
                        break

                    preWord = []
                    preWord.append(nextWord[randNum][1])
                    preWord.append(nextWord[randNum][2])
                    nextWord = []
                    for word in ngrams[n]:
                        if word[0] == preWord[0] and word[1] == preWord[1]:
                            nextWord.append(word)
                    maxRandInt = len(nextWord) - 1
                    randNum = random.randint(0, maxRandInt)
                    ngramSentence[n] += (nextWord[randNum][2] + ' ')

    return ngramSentence

if __name__ == '__main__':
    filename = input("input file name : ")
    codeType = KS_or_UTF8(filename)
    text = readFile(filename, codeType)
    # compute frequency of ngrams
    numGram = 3
    ngramWordCloud = {}
    ngrams, ngramFreqList, ngramWordCloud =\
        make_Ngrams_and_NgramFreqList_and_WordCloud(text, numGram)
    showNgramWordClouds(ngramWordCloud, numGram)

    #sortedNgramFreqList = freqDescSort(ngramFreqList, numGram)
    print("========== Generated Random Sentence ==========")
    ngramRandSentence = genRandSentence(ngrams, numGram)
    print("Unigram >>> " + ngramRandSentence[1])
    print("Bigram  >>> " + ngramRandSentence[2])
    print("Trigram >>> " + ngramRandSentence[3])
