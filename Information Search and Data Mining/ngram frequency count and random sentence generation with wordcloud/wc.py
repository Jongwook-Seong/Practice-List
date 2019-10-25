from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib as mpl

def genNextWordsWC(bicommon, tricommon):
    bwc = []; twc = []
    font_path = './NanumGothic.ttf'
    for i in range(3):
        # Generate Bigram Word Cloud
        text = ''
        for words in bicommon[i]:
            text += words + ' '
        wc = WordCloud(width=1000, height=800,\
                        background_color='white',\
                        font_path=font_path, min_font_size=10,\
                        max_words=20).generate(text)
        bwc.append(wc)
        # Generate Trigram Word Cloud
        text = ''
        for words in tricommon[i]:
            text += words + ' '
        wc = WordCloud(width=1000, height=800,\
                        background_color='white',\
                        font_path=font_path, min_font_size=10,\
                        max_words=20).generate(text)
        twc.append(wc)
    return bwc, twc

def showNextWordsWC(mostFreqWords, bwc, twc):
    # Bigram Word Cloud
    for i in range(3):
        fig = plt.figure(num=i, figsize=(10, 8))
        plt.imshow(bwc[i])
        plt.axis('off')
        plt.title(mostFreqWords[i][0][0] + ' : Bigram Word Cloud')
        plt.show()
        fig.savefig(mostFreqWords[i][0][0] + ' bigram word cloud.png')

    # Trigram Word Cloud
    for i in range(3):
        fig = plt.figure(num=i+3, figsize=(10, 8))
        plt.imshow(twc[i])
        plt.axis('off')
        plt.title(mostFreqWords[i][0][0] + ' : Trigram Word Cloud')
        plt.show()
        fig.savefig(mostFreqWords[i][0][0] + ' trigram word cloud.png')
