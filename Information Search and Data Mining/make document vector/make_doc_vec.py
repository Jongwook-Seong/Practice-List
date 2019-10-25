import re
import math
from konlpy.tag import Kkma
from collections import Counter

kkma = Kkma()

words_dict = {}
document_freq = {}

def make_words_file(news_list_filename):
    global words_dict, document_freq, codeType_of_news_list_file
    word_id = 1
    print("Creating words file...")
    news_list_file = open(news_list_filename, 'r')
    news_file_path_with_name = re.sub(r'\n', '', news_list_file.readline())
    while news_file_path_with_name:
        # read news files and extract nouns from these
        news_file = open(news_file_path_with_name, 'r')
        news_text = news_file.read()
        nouns = kkma.nouns(news_text)
        # set words file and compute df
        with open('words', 'a') as words_file:
            for noun in nouns:
                if noun in words_dict and noun in document_freq:
                    document_freq[noun] += 1
                    continue
                words_file.write(noun + '\n')
                words_dict[noun] = word_id
                document_freq[noun] = 1
                word_id += 1
        news_file_path_with_name = re.sub(r'\n', '', news_list_file.readline())
    print("words file is completed!")
    news_list_file.close()

def make_document_vector(news_list_filename, totNumofDoc):
    global words_dict, document_freq
    print("Creating document vector...")
    news_list_file = open(news_list_filename, 'r')
    news_file_path_with_name = re.sub(r'\n', '', news_list_file.readline())
    while news_file_path_with_name:
        # read news files and extract nouns from these
        news_file = open(news_file_path_with_name, 'r')
        news_text = news_file.read()
        nouns = kkma.nouns(news_text)
        # get frequency of each terms
        term_freq = Counter(nouns)
        this_tfidf, this_docvec = {}, {}
        # compute tf-idf and make document vector sorted by word id
        for noun in nouns:
            idf = math.log2(totNumofDoc / document_freq[noun])
            this_tfidf[noun] = term_freq[noun] * idf
            this_docvec[noun] = [words_dict[noun], this_tfidf[noun]]
        sorted_this_docvec = sorted(this_docvec.items(), key=lambda x: x[1][0])
        # set a document vector
        with open('DocumentVector', 'a') as docvec_file:
            for vec in sorted_this_docvec:
                docvec_file.write(str(vec[1][0]) + ':' + str(vec[1][1]) + ' ')
            docvec_file.write('\n')
        news_file.close()
        news_file_path_with_name = re.sub(r'\n', '', news_list_file.readline())
    print("Done!")
    news_list_file.close()

if __name__ == '__main__':
    news_list_filename, totNumofDoc = '신문기사 문서\신문기사리스트.txt', 0
    with open(news_list_filename) as f:
        for line in f:
            totNumofDoc += 1
    make_words_file(news_list_filename)
    make_document_vector(news_list_filename, totNumofDoc)
