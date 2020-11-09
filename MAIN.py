import os
from GUI import dirLoader,Main_Screen,Value_input,Check_box,Popup_Notification,FileLoader, PL_Screen
from TAG import TagChecker,LengthLoader,M_TagWrite,XYL_Writer,XYL_INIT, XYL_Apply
from Playlist import  Make_Playlist, Write_Playlist
from Sync import Make_Log, Copy_File
import time


EXT_List=['.mp3','.flac','.wav']
inst_Name_List=['ｶﾗｵｹ','カラオケ','off vocal','Off vocal','inst','Inst','Off Vocal','Karaoke','karaoke']
def TagScan():
	ROOT=dirLoader("scan") #GUI
	for  root,dirs,files in os.walk(ROOT): #하위폴더까지 전부 검색 
		print(root)
		for name in files:
			ext = os.path.splitext(name)[1]
			if ext in EXT_List: #EXT_List에 존재하는 파일형식(음악파일)만 처리 
					TagChecker(os.path.join(root,name))

def Recent_Playlist():
	flag=0
	banned_tag_flag=0
	ROOT=dirLoader("scan") #GUI
	T=int(Value_input("Recent N days\n Enter N : ")) #어느정도 기간을 플레이리스트로할래?
	PL=Make_Playlist("Recent",ROOT) # 플레이리스트 파일 생성
	dir_list=[]
	for Dirs in os.listdir(ROOT):
		if os.path.isdir(os.path.join(ROOT,Dirs)):
			for root,dirs,files in os.walk(os.path.join(ROOT,Dirs)):
				for name in files:
					ext = os.path.splitext(name)[1]
					if ext in EXT_List:
						flag=1
						break
				if flag==1:
					break
			if flag==1:	
				dir_list.append(Dirs)
			flag=0

	Option=Check_box("옵션선택",["Off vocal 제외","2분미만 6분이상의 파일 제외"])
	Folder=Check_box("동기화폴더 선택(음악파일이 있는 폴더만 표시중)",dir_list)
	for  root,dirs,files in os.walk(ROOT):
		for name in files:
			ext = os.path.splitext(name)[1]
			if ext in EXT_List:
				File=os.path.join(root,name)
				for banned_tag in inst_Name_List:
						if banned_tag in name:
							banned_tag_flag=1
				try:
					ctime=os.path.getctime(File)
				except FileNotFoundError: #제발파일이름에이상한문자좀넣지말아봐
					pass
				if int(time.time()-ctime) < (T+1)*24*60*60: #파일생성시간이 조건을 만족하면
					Length = LengthLoader(File,ext)
					if (Option[1]==False or (Length > 120 and Length < 360)) and banned_tag_flag==0:
						if banned_tag_flag==0:
							RelDir = os.path.relpath(File,ROOT) #상대경로 계산 
							print(RelDir)
							Write_Playlist(PL,RelDir,Length) # 작성 
				banned_tag_flag=0
	PL.close()

def Check_Musicfolder(ROOT):
	dir_list=[]

	flag=0 #폴더안에 음악파일이 있는지 확인해서 음악파일이 있는경우만 리스트로
	for Dirs in os.listdir(ROOT):
		if os.path.isdir(os.path.join(ROOT,Dirs)):
			for root,dirs,files in os.walk(os.path.join(ROOT,Dirs)):
				for name in files:
					ext = os.path.splitext(name)[1]
					if ext in EXT_List:
						flag=1
						break
				if flag==1:
					break
			if flag==1:	
				dir_list.append(Dirs)
			flag=0
	return dir_list

def Folder_Playlist():
	ROOT=dirLoader("Folders inside this folder to playlist (SUB-DIRECTORY EXCLUDED) ")
	dir_list=Check_Musicfolder(ROOT)


	Option=Check_box("옵션선택",["Off vocal 제외","2분미만 6분이상의 파일 제외"])
	Folder=Check_box("동기화폴더 선택(음악파일이 있는 폴더만 표시중)",dir_list)
	Work_list=[] #실제 작업폴더 리스트
	for i in range(len(dir_list)):
		if Folder[i]==True:
			Work_list.append(dir_list[i])
	flag=0
	banned_tag_flag=0 #off vocal에 해당하는 글을 제목에 포함하는가 여부
	print(Work_list)
	for x in Work_list:
		for root,dirs,files in os.walk(os.path.join(ROOT,x)):
			for name in files:
				ext = os.path.splitext(name)[1]
				if Option[0]==True:
					for banned_tag in inst_Name_List:
						if banned_tag in name:
							banned_tag_flag=1 # 만약 inst_Name_List에 포함된 문구가 있으면 banned_tag_flag를 1로 
				if ext in EXT_List:
					if flag == 0:
						PL=Make_Playlist(x,ROOT)
						flag+=1
					File=os.path.join(root,name)
					if os.path.isfile(File): #제발 이름에 이상한것좀 넣지 말아봐
						Length = LengthLoader(File,ext)
						if (Option[1]==False or (Length > 120 and Length < 360)) and banned_tag_flag==0:
							RelDir = os.path.relpath(File,ROOT)
							print("Writing : ",RelDir)
							Write_Playlist(PL,RelDir,Length)
						banned_tag_flag=0 #초기화 
		if flag==1:
			PL.close()
		flag=0

def Sync():
	banned_tag_flag=0
	ROOT=dirLoader("From") #GUI
	To=dirLoader("To")
	Log = Make_Log("LOG",ROOT) #로그생성 
	dir_list=Check_Musicfolder(ROOT)
	Option=Check_box("옵션선택",["Off vocal 제외"])
	Folder=Check_box("동기화폴더 선택(음악파일이 있는 폴더만 표시중)",dir_list)
	Work_list=[] #실제 작업폴더 리스트
	for i in range(len(dir_list)):
		if Folder[i]==True:
			Work_list.append(dir_list[i])
	for x in Work_list:
		for root,dirs,files in os.walk(os.path.join(ROOT,x)):
			RelDir=os.path.relpath(root,ROOT) #폴더 동기화를 위한 폴더 상대경로
			if os.path.exists(os.path.join(To,RelDir))==False: #폴더가 존재하지 않으면
				os.mkdir(os.path.join(To,RelDir)) #만드세요 (폴더동기화)
			for name in files:
				ext = os.path.splitext(name)[1]
				if Option[0]==True:
					for banned_tag in inst_Name_List:
						if banned_tag in name:
							banned_tag_flag=1 # 만약 inst_Name_List에 포함된 문구가 있으면 banned_tag_flag를 1로 
				if ext in EXT_List:  # 음악파일 동기화
					if banned_tag_flag==0:
						File=os.path.join(root,name)
						Status=TagChecker(File) #태그상황
						RelDir=os.path.relpath(File,ROOT) # 파일의 상대경로로 갱신
						try: 
							Log.write(RelDir+"\n"+"".join(Status)+"\n") #로그작성 
						except TypeError:
							pass
						try:
							Copy_File(File,os.path.join(To,RelDir))
						except FileNotFoundError:
							pass
					banned_tag_flag=0
				elif ext == '.m3u8': #재생목록 동기화 
					File=os.path.join(root,name)
					Log.write(os.path.relpath(File,ROOT)+"\n") #로그작성
					Copy_File(File,To)
	Log.close()
	Copy_File(os.path.join(ROOT,"LOG.txt"),To) #목표경로에도 로그 복사 

def Tag_Edit():
	TAG_NAME_LIST=['제목','아티스트','앨범','트랙년도','앨범아트','작곡가']
	Checked_Tag = Check_box("입력할 태그를 선택하세요",TAG_NAME_LIST)
	ROOT=dirLoader("scan") #GUI
	for  root,dirs,files in os.walk(ROOT): #하위폴더까지 전부 검색 
		print(root)
		for name in files:
			ext = os.path.splitext(name)[1]
			if ext in EXT_List: #EXT_List에 존재하는 파일형식(음악파일)만 처리 
				DIR=os.path.join(root,name)
				Tag_Status = TagChecker(DIR)
				for i in range(6):
					if Checked_Tag[i]==True and Tag_Status[i]=='X':
						Popup_Notification(name+" 의"+TAG_NAME_LIST[i]+"를 입력하세요")
						Text=Value_input(TAG_NAME_LIST[i])
						M_TagWrite(DIR,i,Text)
	Popup_Notification("완료")

def Excel_Write():
	num=2
	wb=XYL_INIT()
	ROOT=dirLoader("scan") #GUI
	for  root,dirs,files in os.walk(ROOT): #하위폴더까지 전부 검색 
		print(root)
		for name in files:
			ext = os.path.splitext(name)[1]
			if ext in EXT_List: #EXT_List에 존재하는 파일형식(음악파일)만 처리 
					XYL_Writer(wb,os.path.join(root,name),num)
					num+=1
	dir=dirLoader("저장경로")
	wb.save(dir+'/TEST.xlsx')


while True:
	idx=Main_Screen() #GUI

	if idx==0:
		TagScan()

	if idx==1:
		idx2 = PL_Screen()
		if idx2==0:
			Recent_Playlist()
		if idx2==1:
			Folder_Playlist()


	if idx==2:
		Sync()

	if idx==3:
		Tag_Edit()

	if idx==4:
		Excel_Write()

	if idx==5:
		dir=FileLoader("Excel File")
		XYL_Apply(dir)
