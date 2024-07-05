import collections

def termL(text):
	return text.split()
# end def

d0='한국 한국 한국 미국 미국 일본 중국'
d1='한국 중국 일본 일본'
d2='중국 미국'
d3='한국 한국'
d4='미국'
d5='한국'

C=[d0,d1,d2,d3,d4,d5]
Posting={}
for docNo,doc in enumerate(C):
	L=termL(doc)
	TF=collections.Counter(L)
	for t in TF:
		if t not in Posting: Posting[t]={}
		Posting[t][docNo]=TF[t]
	# end for
# end for
print(Posting)

while(True):
	Q=input('Query: ')
	score={}
	for qt in termL(Q):
		if qt not in Posting: continue
		for docNo in Posting[qt]:
			if docNo not in score: score[docNo]=0
			score[docNo]+=Posting[qt][docNo]
		# end for
	# end for

	for docNo in sorted(score,key=score.get,reverse=True):
		print(score[docNo],'d'+str(docNo),C[docNo])
	# end for
# end while
