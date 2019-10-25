# global variable
utf8Freq = [0] * 65536
kscFreq = [0] * (256 * 25)
sylFreqDict = {}
numofSyl = 0
totSyl = 0

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

# read file
def readFile(filename, codeType):
    f = open(filename, 'rt', encoding=codeType)
    data = f.read()
    f.close()
    return data

# count Syllable Frequency
def countFreq(filename, codeType):
    c = ['', '', '']
    global totSyl

    with open(filename, 'rb') as f:
        try:
            # UTF-8
            if codeType == 'utf-8':
                while True:
                    c[0] = f.read(1)
                    # EOF
                    if c[0] == '':
                        break;
                    # MSB == 0 (ASCII)
                    elif c[0][0] & b'\x80'[0] == 0:
                        utf8Freq[c[0][0]] += 1
                        continue
                    else:
                        c[1] = f.read(1)
                        # 110x xxxx 10xx xxxx
                        if bytes([c[0][0] & b'\xe0'[0]]) == b'\xc0' and\
                                bytes([c[1][0] & b'\xc0'[0]]) == b'\x80':
                            i = (c[0][0] & b'\x1f'[0]) << 6 | (c[1][0] & b'\x3f'[0])
                            utf8Freq[i] += 1
                            continue
                        # 1110 xxxx 10xx xxxx 10xx xxxx
                        else:
                            c[2] = f.read(1)
                            if bytes([c[0][0] & b'\xf0'[0]]) == b'\xe0' and\
                                    bytes([c[1][0] & b'\xc0'[0]]) == b'\x80' and\
                                    bytes([c[2][0] & b'\xc0'[0]]) == b'\x80':
                                i = (c[0][0] & b'\x0f'[0]) << 12\
                                    | (c[1][0] & b'\x3f'[0]) << 6\
                                    | (c[2][0] & b'\x3f'[0])
                                utf8Freq[i] += 1
                    totSyl += 1
            # KSC5601 (CP949)
            elif codeType == 'cp949':
                k = 1000
                while k > 0:
                #while True:
                    c[0] = f.read(1)
                    if c[0] ==  '': break
                    if c[0][0] < b'\xb0'[0] or c[0][0] > b'\xc8'[0]: continue
                    c[1] = f.read(1)
                    kscFreq[(c[0][0] - b'\xb0'[0]) * 256 + c[1][0]] += 1
                    totSyl += 1
                    k -= 1
        except Exception as e:
            print(e)

# convert freq list to dictionary
def listToDict(codeType):
    global sylFreqDict, numofSyl
    if codeType == 'utf-8':
        for i in range(b'\xac'[0], b'\xd7'[0]+1):
            for j in range(b'\x00'[0], b'\xff'[0]+1):
                if i == b'\xd7'[0] and j > b'\xa3'[0]: break
                # 0xAC00 ~ 0xD7A3
                if utf8Freq[i * 256 + j] > 0:
                    b = [b'\xe0'[0] | ((i >> 4) & b'\x0f'[0]),\
                        b'\x80'[0] | ((i & b'\x0f'[0]) << 2) | (j >> 6) & b'\x03'[0],\
                        b'\x80'[0] | (j & b'\x3f'[0])]
                    sylFreqDict[str(bytes([b[0]]) + bytes([b[1]]) + \
                        bytes([b[2]]), encoding='utf-8')]\
                        = [ utf8Freq[i * 256 + j], utf8Freq[i * 256 + j] / totSyl ]
                    numofSyl += 1
    elif codeType == 'cp949':
        for i in range(b'\xb0'[0], b'\xc8'[0]+1):
            for j in range(0, 255):
                if kscFreq[(i - b'\xb0'[0]) * 256 + j] > 0:
                    sylFreqDict[str(bytes([i]) + bytes([j]), encoding='cp949')]\
                        = [ kscFreq[(i - b'\xb0'[0]) * 256 + j],\
                            kscFreq[(i - b'\xb0'[0]) * 256 + j] / totSyl ]
                    numofSyl += 1

# sort descending order by frequency
def printSylFreqDescSort(codeType, n):
    sortedFreqDict = sorted(sylFreqDict.items(), key=lambda x: x[1][0], reverse=True)
    k, cumProb = 0, 0.0
    print("음절\t빈도\t출현확률\t\t누적출현확률")
    for elem in sortedFreqDict:
        if k >= n: break
        cumProb += elem[1][1]
        print(elem[0], " ::\t", elem[1][0], "\t", elem[1][1], "\t", cumProb)
        k += 1

if __name__ == '__main__':
    filename = 'text.txt'
    codeType = KS_or_UTF8(filename)
    readFile(filename, codeType)
    countFreq(filename, codeType)
    listToDict(codeType)
    print("텍스트에서 발견된 한글 음절의 개수 :", numofSyl, "개")
    n = int(input("n 값 입력 : "))
    printSylFreqDescSort(codeType, n)
