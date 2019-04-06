# yominjeongeum_translator.py
# 야민정음 번역기

# Author: 변다빈
# 2017/12/18
# Course: Language and Computer

# Final term project


## 준비물 가져오기 및 가공 ##
import re, hangul, conjoin_hangul_jamos


# 준비물 1(한글 한 글자끼리의 변환쌍 - Aset) 및 주어진 텍스트의 한글을 분해 및 가공하는 함수
def decompose_hangul_jamos(syl):
    if ord('가') <= ord(syl) <= ord('힣'): # 초·중·종성 모두 있거나 종성만 없는 글자들은
        Dsyl = hangul.decompose(syl, no_batchim = '_', del_nonhangul = False) # hangul.decompose로 자소분해
    else: # 자음 또는 모음만 존재하는 것은 자소 분해처럼 처리
        if ord('ㄱ') <= ord(syl) < ord('ㅎ'): # 자음만 존재하는 경우
            Dsyl = syl[0] + '_' + '_' # 자소 분해했을 때 초성만 있는 것처럼
        elif ord('ㅏ') <= ord(syl) < ord('ㅣ'): # 모음만 존재하는 경우
            Dsyl = '_' + syl[0] + '_' # 자소 분해했을 때 중성만 있는 것처럼
    return Dsyl # 분해 및 가공된 한글 한 글자


# 준비물 1: 한글 한 글자끼리의 변환쌍
f = open('data/alternation.txt') # data 디렉토리의 alternation.txt 파일 열기
Asets = [[decompose_hangul_jamos(Aset[0]), decompose_hangul_jamos(Aset[1]), int(Aset[2])]\
for Aset in [line.split() for line in f.readlines()]] # 행별로 끊어 공백을 기준으로 나눈 후, 그에 대해 분해 및 가공 함수 적용
f.close() # 파일 닫기

# 준비물 2: 한글 초·중·종성의 회전꼴
f = open('data/rotation.txt') # data 디렉토리의 rotation.txt 파일 열기
Rsets = [[Rset[0], Rset[1], int(Rset[2])] for Rset in [line.split() for line in f.readlines()]] # 행별로 끊어 공백을 기준으로 나눈 후, 그에 대해 가공(Rset[2]는 그 회전꼴의 회전각)
f.close() # 파일 닫기



## 야민정음 변환법 1: 준비물 1을 활용하여 비슷하거나 관련된 한글/한자로 변환 ##
def similize(syl, degree): # 한글 한 글자와 번역 강도를 인자로 하는 함수
    Dsyl = decompose_hangul_jamos(syl) # 현재 글자를 분해 및 가공

    for p in range(1, degree+1): # 사용 빈도가 높은(p가 1에 가까운) 변환쌍일수록 먼저 확인
        for Aset in Asets: # 변환쌍들을 하나씩 확인
            if Aset[2] <= p: # 현재 탐색 중인 사용 빈도보다 낮은 것(Aset[2]가 p보다 큰 것)은 무시
                for i in range(2): # 변환쌍의 앞 부분과 뒷 부분을 모두 탐색하여 양방향 변환이 가능하도록
                    if i == 0: j = 1
                    else: j = 0

                    # 변환쌍의 앞과 뒤가 초·중·종성이 다른 정도에 따라 구분하여, 현재 글자에 적용할 수 있는지 확인
                    # 특정 자모가 False이면, 그것이 다른 변환쌍인지 확인하고 적용을 시도하는 것(True가 자모 인자의 초깃값)
                    # i) 초성만 다른 변환쌍('푸' ↔ '쭈' 등)
                    Ysyl = similize_check(Dsyl, Aset, i, j, L = False)
                    if Ysyl: return Ysyl # 초성만 바꾸는 변환이 적용 가능하면 그것을 적용해 반환하고 이 함수를 마침
                    # ii) 초성과 중성이 다른 변환쌍('대' ↔ '머' 등) - 변환에 추가 조건이 필요함
                    if (Aset[j][0] == '_' or Aset[j][1] == '_') and Dsyl[2] != '_': pass # 현재 글자의 종성이 존재하는데, 변환 목표가 자음 또는 모음 하나로만 이루어진 경우('구' ↔ 'ㅋ', '시' ↔ 'ㅐ' 등)
                    else: # 그런 경우가 아닐 때에만 정상적인 변환 가능
                        Ysyl = similize_check(Dsyl, Aset, i, j, L = False, V = False)
                        if Ysyl: return Ysyl # 초성과 중성을 바꾸는 변환이 적용 가능하면 그것을 적용해 반환하고 이 함수를 마침
                    # iii) 중성과 종성이 다른 변환쌍('우' ↔ '윽' 등)
                    Ysyl = similize_check(Dsyl, Aset, i, j, V = False, T = False)
                    if Ysyl: return Ysyl # 중성과 종성을 바꾸는 변환이 적용 가능하면 그것을 적용해 반환하고 이 함수를 마침
                    # iv) 모든 자모가 다른 변환쌍('통' ↔ 듷', '김' ↔ '숲' 등)
                    Ysyl = similize_check(Dsyl, Aset, i, j, L = False, V = False, T = False)
                    if Ysyl: return Ysyl # 모든 자모를 바꾸는 변환이 적용 가능하면 그것을 적용해 반환하고 이 함수를 마침

    Ysyl = Dsyl # 번역 강도 내에서 어떤 변환쌍도 이용할 수 없는 경우
    return Ysyl # 원래 글자를 반환함


# 야민정음 변환법 1에서 반복되는 부분을 일반화하여 처리하는 함수
def similize_check(Dsyl, set, i, j, L = True, V = True, T = True): # 분해된 음절과 현재 살피고 있는 변환쌍, 변환쌍의 앞/뒤 중 어디를 보고 있는지, 어떤 자모가 다른 것에 주목하는지를 인자로 하는 함수
    set_L, set_V, set_T = bool(set[i][0] == set[j][0]), bool(set[i][1] == set[j][1]), bool(set[i][2] == set[j][2]) # 자모 인자에 따라 변환쌍의 앞과 뒤 비교 조건이 달라지는 것을 구현하는 준비
    match_list = [bool(Dsyl[0] == set[i][0]), bool(Dsyl[1] == set[i][1]), bool(Dsyl[2] == set[i][2])] # 자모 인자에 따라 현재 글자에 변환이 적용 가능한지 확인하는 조건이 달라지는 것을 구현하는 준비

    LVT_bools = [L, V, T] # 자모 인자들을 한 번에 효율적으로 활용하기 위한 준비(초·중·종성 순서일 때 True와 False가 항상 연속된 두 부분으로 나눠짐에 착안)
    k = LVT_bools.index(False) # False가 처음 등장하는 위치를 k
    try: l = LVT_bools.index(True) # True가 처음 등장하는 위치를 l (초·중·종성 순서일 때 False 범위를 자동으로 나타내는 것이 목적)
    except: l = 3 # True가 없는 경우(모든 자모를 바꾸는 변환), l에 3을 부여하여 [0:3]을 나타냄
    if k > l: l = 3 # False가 True보다 나중에 등장하는 경우(중성과 종성을 바꾸는 변환), l에 3을 부여하여 [1:3]을 나타냄

    if L == set_L and V == set_V and T == set_T: # 주어진 모든 자모 인자들의 bool 값과, 변환쌍의 앞뒤 비교 결과의 bool 값이 같고
        if all(match_list[k:l]): # 주어진 인자가 False인 현재 글자의 자모에 변환이 모두 적용 가능하면
            Ysyl = Dsyl.replace(Dsyl[k:l], set[j][k:l]) # 해당 범위에 변환을 적용하여 Ysyl로 저장
            print(Dsyl, '>', Ysyl, 'LVT'[k:l]) # 원래 글자의 어떤 자모가 변환되어 새로운 글자가 되었는지 기록 출력
            return Ysyl # Ysyl 반환



## 야민정음 변환법 2: 준비물 2를 활용하여 한 단어를 같은 방향으로 회전하여 변환 ##
def rotate(syl): # 한글 한 글자를 인자로 하는 함수
    Dsyl = decompose_hangul_jamos(syl) # 현재 글자를 분해 및 가공
    Rdics = [{0: Dsyl[0]}, {0: Dsyl[1]}, {0: Dsyl[2]}] # 분해한 글자의 현재 초·중·종성을 각각의 딕셔너리에 0이라는 키를 만들어 그 값으로 저장

    for Rset in Rsets: # 회전꼴들을 하나씩 확인
        for k in range(3): # 초·중·종성 각각에 대해
            if Dsyl[k] == Rset[0]: # 회전꼴의 앞 부분에 대응되면
                Rdics[k][Rset[2]] = Rset[1] # 해당 회전각을 키로 만들어 새로운 회전꼴을 그 값으로 저장
            if Dsyl[k] == Rset[1]: # 회전꼴의 뒷 부분에 대응되면
                Rdics[k][360-Rset[2]] = Rset[0] # 360 - 해당 회전각을 키로 만들어 새로운 회전꼴을 그 값으로 저장

    if Dsyl.endswith('_'): # 현재 글자의 종성이 없으면
        try: # 각 자모를 모두 90도 회전할 수 있는지 확인
            return rotate_check(90, Dsyl, Rdics) # 가능하면 그것을 적용해 반환하고 이 함수를 마침
        except: pass # 가능하지 않으면 넘어가기
        try: # 각 자모를 모두 270도 회전할 수 있는지 확인
            return rotate_check(270, Dsyl, Rdics) # 가능하면 그것을 적용해 반환하고 이 함수를 마침
        except: Ysyl, angle = False, False # 90도와 270도 모두 가능하지 않으면 False들을 저장
    else: # 현재 글자의 종성이 있으면
        try: # 각 자모를 모두 180도 회전할 수 있는지 확인
            if Rdics[0][180] and Rdics[1][180] and Rdics[2][180]:
                Ysyl, angle = Rdics[2][180] + Rdics[1][180] + Rdics[0][180], 180 # 가능하면 그것을 적용
                print(Dsyl, '>', Ysyl, '180°') # 원래 글자를 몇 도 회전하여 새로운 글자가 되었는지 기록 출력
                return Ysyl, angle # 반환하고 이 함수를 마침
        except: Ysyl, angle = False, False # 가능하지 않으면 False들을 저장

    return Ysyl, angle # 모든 회전에 실패한 경우 False들을 반환


# 야민정음 변환법 2에서 반복되는 부분을 일반화하여 처리하는 함수
def rotate_check(a, Dsyl, Rdics): # 회전각과 분해된 음절, 각 자모별 회전꼴들을 인자로 하는 함수
    if Rdics[0][a] and Rdics[1][a]: # 초성과 중성을 주어진 회전각만큼 모두 회전할 수 있으면
        Ysyl, angle = Rdics[0][a] + Rdics[1][a] + '_', a # 그것을 적용
        print(Dsyl, '>', Ysyl, str(a) + '°') # 원래 글자를 몇 도 회전하여 새로운 글자가 되었는지 기록 출력
        return Ysyl, a # 반환하고 이 함수를 마침(불가능하면 아무것도 반환하지 않음)



## 야민정음 변환 종합 ##
def yaminize(s, degree = 3): # 텍스트 전체와 번역 강도를 인자로 하는 함수
    print('--------------------') # 텍스트 변환 기록 출력의 시작을 나타내는 선
    return ''.join([yaminize_word(word, degree) for word in re.split('([^가-힣ㄱ-ㅎㅏ-ㅣ]+)', s)]) # 한글이 아닌 것을 기준으로 단어를 나눈 후, 그 각각에 대해 함수를 적용하여 변환하고 다시 합쳐 반환


# 단어 단위의 야민정음 변환 #
def yaminize_word(word, degree): # 한 단어와 번역 강도를 인자로 하는 함수
    if re.search('[가-힣ㄱ-ㅎㅏ-ㅣ]+', word): # 한글을 한 글자 이상 포함하는 단어만 취급
        print('word:', word) # 단어별 변환 기록을 구분하는 선

        # 야민정음 변환법 2(회전 변환)를 먼저 시도
        Rsyls = [rotate(syl) for syl in word] # 현재 단어의 각 음절들에 대해 rotate 함수를 적용한 결과들을 list로 저장
        try:
            angle = Rsyls[0][1] # 첫 음절의 회전각을 기준으로 함(False일 수도 있음)
            if all(Rsyl[1] == angle for Rsyl in Rsyls): # 단어의 모든 음절들이 같은 회전각을 지니면
                if angle == 90: # 그 회전각이 90도인 경우
                    new_word = ''.join([conjoin_hangul_jamos.conjoin(Rsyl[0]) for Rsyl in Rsyls]) # 모든 음절을 90도 회전하고 자소조합해 한 단어로 이어붙이기
                else: # 그 회전각이 90도가 아닌 경우(180도, 270도)
                    Rsyls.reverse() # 단어 내에서 음절들의 순서를 거꾸로 하여
                    new_word = ''.join([conjoin_hangul_jamos.conjoin(Rsyl[0]) for Rsyl in Rsyls]) # 모든 음절을 해당 각만큼 회전하고 자소조합해 한 단어로 이어붙이기
                print('★ 회전 성공:', new_word, '\n----------') # 단어 단위의 회전에 성공했다는 기록 출력
                return new_word # 회전한 단어를 반환
            else: print('- 회전 불가능/방향 불일치 글자 포함:', word) # 모든 음절들이 같은 회전각을 지니지 않거나 하나라도 회전이 불가하면 실패
        except: # 모든 음절들이 회전각으로 False를 가지면
            print('- 회전 가능한 글자 없음:', word) # 마찬가지로 실패

        # 변환법 2에 실패한 경우 변환법 1을 음절 단위로 시도
        print('\n...비슷한 한글로 한 글자씩 변환') # 다른 변환법을 시도하는 것을 기록
        new_word = ''.join([conjoin_hangul_jamos.conjoin(syl) if syl.count('_') < 2 else syl.replace('_', '') for syl in [similize(syl, degree) for syl in word]])
        # 각 음절들에 대해 similize 함수를 적용한 결과들을 list로 저장하여, 그 각각에 대해 자소조합 등을 적용해 한 단어로 다시 이어붙이기
        print('★ 변환 완료:', new_word, '\n----------') # 변환 결과를 출력
        return new_word # 변환한 결과를 반환

    else: # 한글을 한 글자도 포함하지 않는 단어는
        return word # 그대로 반환
