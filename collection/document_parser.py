import	re

def printDoc(doc,oF):
	doc=re.sub('[\r\n]+',' ',doc)
	m=re.search('^\s*<id>\s*(\d+)',doc)
	if m: I=m.group(1)
	m=re.search('\[title\](.+?)<[a-z]+>',doc) # ?: minimal matching
	if m: T=m.group(1)
	m=re.search('<abstract>(.*?)<[a-z]+>',doc)
	if m: A=m.group(1)
	oF.write(I+'\t'+' '.join((T+' '+A).split())+'\n')
	#print(I+'\t'+' '.join((T+' '+A).split()))
# end def

oF=open('collection','w',encoding='utf-8')
doc=''
for line in open('KTset/KTSET1.0-RawCollectionFile',encoding='utf-8'):
	if doc!='' and re.match('^\s*<id>\s*(.+)\s*$',line): printDoc(doc,oF); doc=''
	doc+=line
# end for
if doc!='': printDoc(doc,oF)
oF.close()
