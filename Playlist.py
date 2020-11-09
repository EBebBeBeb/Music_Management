def Make_Playlist(Name,ROOT):
	f=open(ROOT+"/"+Name+".m3u8",'w',-1,'utf-8')
	f.write("#EXTM3U\n")
	return f

def Write_Playlist(FILE,Dir,Length):  
	FILE.write("#EXTINF:{}\n".format(Length))
	FILE.write(Dir+"\n")

