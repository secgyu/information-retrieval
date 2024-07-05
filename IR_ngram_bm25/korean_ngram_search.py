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
	return ngram(doc)
# end def

def indexing(iF):
	posting,docLen,N={},{},0.
	for line in open(iF,encoding='utf-8'):
		N+=1
		docNo,doc=line.rstrip().split('\t')
		TF=collections.Counter(term(doc))
		docLen[docNo]=sum(TF.values())
		for t,tf in TF.items():
			if t not in posting: posting[t]=[]
			posting[t].append((docNo,tf))
		# end for
	# end for
	avdl=sum(docLen.values())/N
	
	df={}
	for t in posting: df[t]=len(posting[t])
	
	return {'posting':posting,'docLen':docLen,'N':N,'df':df,'avdl':avdl}
# end def

def retrieval(Q,IndexDB):
	posting,docLen,N,df,avdl=IndexDB['posting'],IndexDB['docLen'],IndexDB['N'],IndexDB['df'],IndexDB['avdl']
	score,qLen,k1,k2,b={},0.,1.2,100.,0.75
	qTF=collections.Counter(term(Q))
	for qt,qtf in qTF.items():
		if qt not in posting: continue
		qtw=(k2+1)*qtf/(k2+qtf)
		for docNo,dtf in posting[qt]:
			if docNo not in score: score[docNo]=0
			dtw=(k1+1)*dtf/(k1*((1-b)+b*docLen[docNo]/avdl)+dtf)
			score[docNo]+=math.log((N-df[qt]+.5)/(df[qt]+.5))*dtw*qtw
		# end for
	# end for
	return score
# end def

oF=open('retrievalResult','w',newline='\n')
model,TopN='bm25',100
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

os.system('trec_eval KTset/KTSET1.0.RJ retrievalResult')
