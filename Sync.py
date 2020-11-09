import shutil

def Make_Log(Name,ROOT):
	f=open(ROOT+"/"+Name+".txt",'w',-1,'utf-8')
	f.write("상대경로\n['제목','아티스트','앨범','트랙년도','앨범아트']\n")
	return f


def Copy_File(From,To):
	shutil.copy2(From,To)

