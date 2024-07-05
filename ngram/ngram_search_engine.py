import collections

def ngram(doc):
    L=[]
    for t in doc.split():
        if len(t)==1: L.append(t); continue
        for i in range(len(t)):
            if i+1<len(t): L.append(t[i:i+2])
        # end for
    # end for
    return L
# end def

def termL(text):
    #return text.split()
    return ngram(text)
# end def


d1='아프가니스탄에서 차량 폭탄 테러로 의심되는 폭발이 있었다.'
d2='아프간에서 발생한 차량 테러로 인해 큰 인명 피해가 있었다.'
d3='뭄바이에서 발생한 테러와 관련하여 한국대사관에서는 한국인들의 사망과 부상 피해를 조사 중이다.'
d4='테러 위협으로 인해 뭄바이 공항의 보안이 강화되었다.'
d5='최근 테러리스트들의 잇단 테러 위협이 증가하고 있다.'
d6='최근 발생한 폭탄테러로 인해 한국 정부는 해외 거주 한국인의 안전 여부를 파악 중에 있다.'

#C=[d1,d2,d3,d4,d5,d6] # 문서집합, 문서컬렉션
C=[]
for doc in open('collection_for_IR_00_ngram.txt',encoding='UTF-8'):
    C.append(doc.rstrip())
# end for

# 색인모듈
Posting,docNo={},0
for doc in C:
    L=ngram(doc)
    TF=collections.Counter(L)
    for t in TF:
        if t not in Posting: Posting[t]={}
        Posting[t][docNo]=TF[t] # tf(t,docNo)
    # end for
    docNo+=1
# end for

# 검색모듈
while(True):
    Q=input('Query: ')
    score={}
    for qt in ngram(Q):
        if qt not in Posting: continue
        for docNo in Posting[qt]:
            if docNo not in score: score[docNo]=0
            score[docNo]+=Posting[qt][docNo] # TF의 합으로 유사도 계산
        # end for
    # end for
    rankedList=sorted(score,key=score.get,reverse=True)
    rank=1
    for docNo in rankedList:
        print('%02d'%rank,score[docNo],docNo,C[docNo])
        rank+=1
    # end for
# end while
