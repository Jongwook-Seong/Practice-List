import ngram
import wc

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
        file = f.read(10000000)
    text = ''.join(file)
    return text

if __name__ == '__main__':
    filename = input("input file name : ")
    codeType = KS_or_UTF8(filename)
    text = readFile(filename, codeType)

    text = ngram.trimTexts(text)
    unigram, bigram, trigram = ngram.getNgrams(text)
    unigramFreq = ngram.getFreqList(unigram)
    bigramFreq = ngram.getFreqList(bigram)
    trigramFreq = ngram.getFreqList(trigram)
    # save 1000 ngrams(uni, bi, tri)
    ngram.save1000ngrams(unigramFreq, bigramFreq, trigramFreq)

    # count ngrams total token number, over 10, and over 3
    count10 = 0; count3 = 0
    for token in unigramFreq:
        if unigramFreq[token] >= 10: count10 += 1
        if unigramFreq[token] >= 3: count3 += 1
    print("Unigram number of total, over 10, over 3 :",\
            len(unigramFreq), count10, count3)
    count10 = 0; count3 = 0
    for token in bigramFreq:
        if bigramFreq[token] >= 10: count10 += 1
        if bigramFreq[token] >= 3: count3 += 1
    print("Bigram number of total, over 10, over 3 :",\
            len(bigramFreq), count10, count3)
    count10 = 0; count3 = 0
    for token in trigramFreq:
        if trigramFreq[token] >= 10: count10 += 1
        if trigramFreq[token] >= 3: count3 += 1
    print("Trigram number of total, over 10, over 3 :",\
            len(trigramFreq), count10, count3)

    # get most frequently represented 3 word
    mostFreqWords = ngram.getMostFreqWords(unigramFreq)

    # show ngrams word cloud about next words to the most frequent 3 words
    bicommon, tricommon = ngram.getMostCommons(mostFreqWords, bigram, trigram)
    bigramwc, trigramwc = wc.genNextWordsWC(bicommon, tricommon)
    wc.showNextWordsWC(mostFreqWords, bigramwc, trigramwc)

    ssWord = ngram.getMostProbableFirstWords(bigramFreq)
    bisent, trisent = ngram.genSents(ssWord, bigramFreq, trigramFreq)

    # print generated bigram and trigram sentences
    print("Bigram Sentence Generation >>>")
    for i in range(3):
        print('<SS>', i, ssWord[i])
        for j in range(10):
            print(j, bisent[i][j])
    print("Trigram Sentence Generation >>>")
    for i in range(3):
        print('<SS>', i, ssWord[i])
        for j in range(10):
            print(j, trisent[i][j])
