BASE_CODE, CHO_CODE, JUNG_CODE, MAX_CODE = 44032, 588, 28, 55203
CHO_LIST = list('ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ')
JUNG_LIST = list('ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ')
JONG_LIST = list(' ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ')

KORS = list('ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎㄳㄵㄶㄺㄻㄼㄽㄾㄿㅀㅄㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ ')
ENGS = ['r', 'R', 's', 'e', 'E', 'f', 'a', 'q', 'Q', 't', 'T', 'd', 'w', 'W', 'c', 'z', 'x', 'v', 'g', 'rt', 'sw', 'sg',
        'fr', 'fa', 'fq', 'ft', 'fx', 'fb', 'fh', 'qt', 'k', 'o', 'i', 'O', 'j', 'p', 'u', 'P', 'h', 'hk', 'ho', 'hl',
        'y', 'n', 'nj', 'np', 'nl', 'b', 'm', 'ml', 'l', '']
KOR_ENG_TABLE = dict(zip(KORS, ENGS))


# kor2eng 메소드는 한글 이름 데이터를 영문 타자 데이터로 대응시키고, 추가로 해당 이름 데이터를 '성씨'와 '이름'으로 나눈다.
def kor2eng(text):
    fullName = ''  # 풀네임이 저장되는 변수
    firstName = ''  # 성씨가 저장되는 변수
    mlName = ''  # 이름이 저장되는 변수
    count = 0
    for ch in text:
        word_split = split(ch)  # 튜플 word_split에 각각 한글자씩 잘라서 넣는다. ex) 윤형근 --> 윤, 형, 근
        if word_split is None:  # 예외처리
            fullName += ch
        else:
            for i in range(len(word_split)):
                num = KORS.index(word_split[i])
                fullName += ENGS[num]  # 풀네임 저장
                if count == 0:
                    firstName += ENGS[num]  # 성씨 저장
                else:
                    mlName += ENGS[num]  # 이름 저장
        count += 1
        nameList = [fullName, firstName, mlName]  # 풀네임, 성씨, 이름으로 리스트 구성
    return nameList  # 리스트 반환, EXTEND.py에서 받아서 사용함.


# split 메소드는 각각 한글 문자로 영어로 대응시키는 함수. 대응시에 초성, 중성, 종성 리스트를 사용한다.
def split(kor):
    code = ord(kor) - BASE_CODE  # BASE_CODE는 한글의 유니코드인 44032로 선언함.
    if code < 0 or code > MAX_CODE - BASE_CODE:  # 한글 문자의 범위
        if kor == ' ': return None
        if kor in CHO_LIST: return kor, ' ', ' '    # 초성
        if kor in JUNG_LIST: return ' ', kor, ' '   # 중성
        if kor in JONG_LIST: return ' ', ' ', kor   # 종성
        return None
    return CHO_LIST[code // CHO_CODE], JUNG_LIST[(code % CHO_CODE) // JUNG_CODE], JONG_LIST[
        (code % CHO_CODE) % JUNG_CODE]  # 초성, 중성, 종성의 리스트를 리턴한다.
