BASE_CODE, CHO_CODE, JUNG_CODE, MAX_CODE = 44032, 588, 28, 55203
CHO_LIST = list('ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ')
JUNG_LIST = list('ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ')
JONG_LIST = list(' ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ')

KORS = list('ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎㄳㄵㄶㄺㄻㄼㄽㄾㄿㅀㅄㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ ')
ENGS = ['r', 'R', 's', 'e', 'E', 'f', 'a', 'q', 'Q', 't', 'T', 'd', 'w', 'W', 'c', 'z', 'x', 'v', 'g', 'rt', 'sw', 'sg', 'fr', 'fa', 'fq', 'ft', 'fx', 'fb', 'fh', 'qt', 'k', 'o', 'i', 'O', 'j', 'p', 'u', 'P', 'h', 'hk', 'ho', 'hl', 'y', 'n', 'nj', 'np', 'nl', 'b', 'm', 'ml', 'l', '']
KOR_ENG_TABLE = dict(zip(KORS, ENGS))



def kor2eng(text):
    fullName = ''
    firstName = ''
    mlName = ''
    count = 0
    for ch in text:
        spl = split(ch)
        print(ch)
        print(type(spl))
        #print(spl[1])
        if spl is None:
            fullName += ch
        else:
            #res += ''.join([v for v in spl if v != ' '])
            for i in range(len(spl)):
                num = KORS.index(spl[i])
                fullName += ENGS[num]
                if(count == 0):
                    firstName += ENGS[num]
                else:
                    mlName += ENGS[num]
        count += 1


        #print(res)
        nameList = [fullName, firstName, mlName]
    return nameList



def split(kor):
    code = ord(kor) - BASE_CODE
    if code < 0 or code > MAX_CODE - BASE_CODE:
        if kor == ' ': return None
        if kor in CHO_LIST: return kor, ' ', ' '
        if kor in JUNG_LIST: return ' ', kor, ' '
        if kor in JONG_LIST: return ' ', ' ', kor
        return None
    return CHO_LIST[code // CHO_CODE], JUNG_LIST[(code % CHO_CODE) // JUNG_CODE], JONG_LIST[(code % CHO_CODE) % JUNG_CODE]


if __name__ == '__main__':
    print(kor2eng('윤형근'))