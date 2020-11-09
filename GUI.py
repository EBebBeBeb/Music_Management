import PySimpleGUI as sg

def dirLoader(text):
		file_list_column = [
		    [
		        sg.Text("Folder to "+text),
		        sg.In(size=(25, 1), enable_events=True, key="FOLDER"),
		        sg.FolderBrowse()
		    ],[
		    	sg.Button("OK")
		    ]
		]

		layout = [
		    [
		        sg.Column(file_list_column),
		    ]
		]
		window = sg.Window("Choose Directory", layout)

		while True:
			event, values = window.read()
			if event=="FOLDER":
				ROOT=values["FOLDER"]
			if event == "OK" or event == sg.WIN_CLOSED:
				break
		window.close()
		return ROOT

def FileLoader(text):
		file_list_column = [
		    [
		        sg.Text("Folder to "+text),
		        sg.In(size=(25, 1), enable_events=True, key="FOLDER"),
		        sg.FileBrowse(file_types=((".xlsx File", "*.xlsx"),))
		    ],[
		    	sg.Button("OK")
		    ]
		]

		layout = [
		    [
		        sg.Column(file_list_column),
		    ]
		]
		window = sg.Window("Choose Directory", layout)

		while True:
			event, values = window.read()
			if event=="FOLDER":
				ROOT=values["FOLDER"]
			if event == "OK" or event == sg.WIN_CLOSED:
				break
		window.close()
		return ROOT

def Popup_Notification(Text):
	Popup = [
		[sg.Text(Text)],
		[sg.Button("OK")]
	]
	layout = [
		[sg.Column(Popup)]
	]
	window=sg.Window("Message",layout)
	while True:
		event,values = window.read()
		if event == "OK":
			window.close()
			break


def Main_Screen():
	Main = [
		[sg.Text("Select Function")],
		[sg.Button("Tag Scan")],
		[sg.Button("Tag Edit mode")],
		[sg.Button("Playlist Management")],
		[sg.Button("File Status to Excel")],
		[sg.Button("Sync")],
		[sg.Button("Apply Excel Tag")],
	]
	layout = [
		[
		sg.Column(Main)
		]
	]
	window = sg.Window("Music Management",layout)

	while True:
		event, values = window.read()
		if event == "Tag Scan":
			window.close()
			return 0
		if event == "Playlist Management":
			window.close()
			return 1
		if event == "Sync":
			Popup_Notification("음악전용 폴더를 따로 만드신다음 진행하는 것을 권장합니다.")
			window.close()
			return 2
		if event == "Tag Edit mode":
			window.close()
			return 3
		if event == "File Status to Excel":
			window.close()
			return 4
		if event == "Apply Excel Tag":
			window.close()
			return 5

		if event == WIN_CLOSED:
			window.close()

def Value_input(text):
	value_column = [
		    [
		        sg.Text(text),
		        sg.InputText()
		    ],[
		    	sg.Button("OK")
		    ]
		]

	layout = [
		    [
		        sg.Column(value_column),
		    ]
		]
	window = sg.Window("Enter Value", layout)

	while True:
		event, values = window.read()
		if event == "OK" or event == WIN_CLOSED:
			window.close()		
			break
		window.close()
	return values[0]

def Check_box(text,List):
	Checked_Tag=[]
	CB=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
	Bool=True
	temp=[[]]
	frame_layout =[[sg.Text(text)]]
	count=0
	row=0
	for name in List:
		CB[row].append(sg.CB(name,default=Bool))
		count+=1
		if count==5:
			row+=1
			count=0
	frame_layout.extend(CB)
	print(frame_layout)

	layout = [
		#[sg.Button("Select all"),sg.Button("Deselect all")],
		[sg.Column(frame_layout)],
		[sg.Button("Submit")]
	]

	window = sg.Window('Checkbox',layout)
	event, values = window.read()			
	if event == "Submit" or event == WIN_CLOSED:
		window.close()
	for i in range(len(List)):
		Checked_Tag.append(values[i])
	print(Checked_Tag)

	return Checked_Tag

def PL_Screen():
	Main = [
		[sg.Text("Select Function")],
		[sg.Button("Recently added")],
		[sg.Button("Folder List to ")],
	]
	layout = [
		[
		sg.Column(Main)
		]
	]
	window = sg.Window("Music Management",layout)

	while True:
		event, values = window.read()
		if event == "Recently added":
			window.close()
			return 0
		if event == "Folder List to ":
			window.close()
			return 1

		if event == WIN_CLOSED:
			window.close()
