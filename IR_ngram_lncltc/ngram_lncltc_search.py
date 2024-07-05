import  math,collections,glob,os

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

def term(doc):
	#return doc.split()
	return ngram(doc)
	#return okt.nouns(doc)
# end def

def indexing(iF):
	posting,docText,docLen,N={},{},{},0.
	for line in open(iF,encoding='utf-8'):
		N+=1
		docNo,doc=line.rstrip().split('\t')
		docText[docNo]=doc[:30]
		TF=collections.Counter(term(doc))
		
		#docLen[docNo]=math.sqrt(sum([(1+math.log(tf))**2 for tf in TF.values()]))
		V=[]
		for tf in TF.values(): V.append((1+math.log(tf))**2)
		docLen[docNo]=math.sqrt(sum(V))
		
		for t,tf in TF.items():
			if t not in posting: posting[t]=[]
			posting[t].append((docNo,tf))
		# end for
	# end for
	
	#df={t:len(posting[t]) for t in posting}
	df={}
	for t in posting: df[t]=len(posting[t])
	
	return {'posting':posting,'docText':docText,'docLen':docLen,'N':N,'df':df}
# end def

def retrieval(Q,IndexDB):
	posting,docLen,N,df=IndexDB['posting'],IndexDB['docLen'],IndexDB['N'],IndexDB['df']
	score,qLen={},0.
	qTF=collections.Counter(term(Q))
	for qt,qtf in qTF.items():
		if qt not in posting: continue
		qtw=(1+math.log(qtf))*math.log(N/df[qt])
		qLen+=qtw*qtw
		for docNo,dtf in posting[qt]:
			if docNo not in score: score[docNo]=0
			dtw=(1+math.log(dtf))
			score[docNo]+=qtw*dtw
		# end for
	# end for
	for docNo in score:
		score[docNo]/=math.sqrt(qLen)*docLen[docNo]
	# end for
	return score
# end def

oF=open('retrievalResult','w',newline='\n')
model,TopN='Lncltc',100
IndexDB=indexing('collection')
for qF in glob.glob('KTset/Query/*'):
	qNo=os.path.basename(qF)
	q=open(qF,encoding='utf-8').read()
	score=retrieval(q,IndexDB)
	for rank,docNo in enumerate(sorted(score,key=score.get,reverse=True)[:TopN]):
		oF.write('%s\t%s\t%s\t%d\t%.4f\tKTSET'%(qNo,model,docNo,rank+1,score[docNo])+'\n')
	# end for
# end while
oF.close()

os.system('trec_eval -m all_trec KTset/KTSET1.0.RJ retrievalResult')
