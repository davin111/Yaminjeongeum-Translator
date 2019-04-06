# conjoin_hangul_jamos.py
# 한글 자모 조합하기

# Author: 변다빈
# 2017/10/26 - 2017/12/18 수정
# Course: Language and Computer

# HW07심화 - Final term project


# 준비물 1: 한글 자모 배열 순서
LEADING = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ' # 초성
VOWEL = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ' # 중성
TRAILING = 'ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ' # 종성(종성 없는 경우를 추가해야 함)

# 준비물 1 가공:
LCount = len(LEADING) # 초성의 개수
VCount = len(VOWEL) # 중성의 개수
TCount = len(TRAILING) + 1 # 종성의 개수(종성 없는 경우 추가)
NCount = VCount * TCount # 한 초성을 공유하는 모든 음절의 개수 = (중성 개수)*(종성 개수)

# 준비물 2: 음절의 유니코드 값
SBase = ord('가') # 한글 첫 번째 음절 '가'의 유니코드 값을 가져온다.


def conjoin(syl):
# 과정 1: 입력받은 초성, 중성, 종성이 각각의 배열에서 몇 번째인지를 파악한다.
    LIndex = LEADING.find(syl[0]) # 초성
    VIndex = VOWEL.find(syl[1]) # 중성
    if syl[2] == '_': # 종성이 없는 경우
        TIndex = 0 # 종성 배열의 맨 앞인 것으로 파악한다.
    else: # 종성이 있는 경우
        TIndex = TRAILING.find(syl[2]) + 1 # 종성이 없는 경우를 고려해 1을 더한다
# 과정 2: 입력받은 초성, 중성, 종성을 조합했을 때 '가'로부터 몇 번째 다음으로 나오는지 파악한다.
    SIndex = LIndex*NCount + VIndex*TCount + TIndex

# 종합: 순서를 알았으므로 실제 음절을 가져온다.
    return chr(SBase+SIndex)
