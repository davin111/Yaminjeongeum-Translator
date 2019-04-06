# hangul.py
# 한글 처리 모듈 확장하기

# Author: 변다빈
# 2017/11/03 - 2017/12/18 수정
# Course: Language and Computer

# HW08 - Final term project

# 준비물: 한글 자모 배열 순서
# 초성, 중성, 종성 변수를 data 디렉토리의 jamos 파일에서 불러온 내용으로 만든다.
f = open('data/jamos.txt') # data 디렉토리의 jamos 파일을 불러온다.
LEADING, VOWEL, TRAILING = f.readlines() # 파일을 행별로 끊어서 각 변수에 입력되게 한다.
f.close() # 파일을 닫는다.


# 준비물 가공:
LEADING = LEADING.strip()
VOWEL = VOWEL.strip()
TRAILING = TRAILING.strip()
TCount = len(TRAILING) + 1 # 종성의 개수(종성 없는 경우 추가)
VTCount = len(VOWEL) * TCount # 한 초성을 공유하는 모든 음절의 개수 = (중성 개수)*(종성 개수)


# 한글 자모 분해 함수(여러 음절도 가능)
def decompose(hangul, no_batchim = '', del_nonhangul = True):

    # 인수의 자료형이 문자열인 경우에만 반환을 시도하기
    if type(hangul) == str:
        try:
            if ord('가') <= ord(hangul) <= ord('힣'):
                # 한글 한 음절인 경우
                ind = ord(hangul) - ord('가')
                L = LEADING[ind // VTCount] # 초성
                V = VOWEL[ind % VTCount // TCount] # 중성
                T = TRAILING[ind % TCount - 1] if ind % TCount else no_batchim # 종성
                return ''.join((L,V,T))
            else:
                # 한글 음절이 아닌 문자열인 경우
                return '' if del_nonhangul else hangul
        except:
            # 길이 2 이상의 문자열인 경우 ord()에서 TypeError 발생
            return ''.join(decompose(char, no_batchim, del_nonhangul) for char in hangul)
    else:
        return
