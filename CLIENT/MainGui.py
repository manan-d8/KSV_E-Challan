import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk ,Image
import cv2
import numpy as np
import requests
from pprint import pprint
import json
from mysql.connector import MySQLConnection, Error
import mysql.connector
import Challan as chn
from pdf2image import convert_from_path
import datetime
import os
import random
import sys
import subprocess
import re
import Email
import sys

def isWindows():
		is_windows = sys.platform.startswith('win')
		if is_windows:
			return True
		return False

if isWindows():
	from docx2pdf import convert

lbl_load = None
print("Start...!")

x_start, y_start, x_end, y_end = 0, 0, 0, 0
chnNo = "INGJAH"
xline ,yline = 100,100
name,email,vehicletype,vehiclecompany,challancount = "","","","",None
last_img = np.zeros((400,400))
orignal = np.zeros((400,400))
ResizePara = (600, 400)
count ,cropCount,countplace = 0,0,3
moveper = False
plateno = ""
location = ""
FrameCount = 0
Vid_Speed = 1
crop_img = None
conn = None
APIgui = None
DBgui = None
pdfText = None
x = datetime.datetime.now()
date = (x.strftime("%x"))
configjson = open('configure.json',) 
# returns JSON object as  
# a dictionary 
configjson_data = json.load(configjson) 
#print(pages)
#===============================( GUI )============================================
root = tk.Tk()
root.title('Traffic Violation E-Challan Generation')
root.geometry('1366x668')
# root.geometry('1366x768')
root.state('zoomed')
root.configure(background='black')
Video_Path = configjson_data['VideoPath']

cap = cv2.VideoCapture(Video_Path,0)
cap.grab()
ret, frame = cap.retrieve()
def show_frame():
	global last_img
	if var1.get():
		global x_start, y_start, x_end, y_end
		global orignal,ResizePara,count,FrameCount,frame,Vid_Speed
		cap.grab()
		count+=1
		if count%Vid_Speed==0:
			ret, frame = cap.retrieve()
			# for _ in range(16):
			# 	ret, frame = cap.read()
			orignal = frame.copy()
			#grayImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
			cv2image   = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#COLOR_BGR2RGBA)
			img   = Image.fromarray(cv2image).resize(ResizePara)
			last_img = np.asarray(img)
			x_start, y_start, x_end, y_end = 0, 0, 0, 0
			imgtk = ImageTk.PhotoImage(image = img)
			Vidlbl.imgtk = imgtk
			Vidlbl.configure(image=imgtk)
		Vidlbl.after(5 , show_frame)
		FrameCount+=1
	else:
		#=============================draw======================================
		imgcopy = last_img.copy()
		img = cv2.rectangle(imgcopy, (x_start, y_start), (x_end, y_end), (0,0,255), 2)
		img = cv2.line(imgcopy, (xline,0), (xline, ResizePara[1]), (0,0,255), 1)
		img = cv2.line(imgcopy, (xline-4,0), (xline-4, ResizePara[1]), (0,0,255), 1)
		img = cv2.line(imgcopy, (0,yline), (ResizePara[0],yline),  (0,0,255), 1)
		img = cv2.line(imgcopy, (0,yline-4), (ResizePara[0],yline-4),  (0,0,255), 1)
		img   = Image.fromarray(img)
	
		imgtk = ImageTk.PhotoImage(image = img)
		Vidlbl.imgtk = imgtk
		Vidlbl.configure(image=imgtk)
		Vidlbl.after(5 , show_frame)
		FrameCount+=1

def convert_para(x_start, y_start, x_end, y_end):
	global orignal
	#print(orignal.shape) 
	#print((x_start,ResizePara[0],x_start/ResizePara[0]))
	x1 = int(((x_start - 0)/(ResizePara[0]-0))*orignal.shape[1])
	y1 = int(((y_start - 0)/(ResizePara[1]-0))*orignal.shape[0])
	x2 = int(((x_end - 0)/(ResizePara[0]-0))*orignal.shape[1])
	y2 = int(((y_end - 0)/(ResizePara[1]-0))*orignal.shape[0])
	return (x1,y1,x2,y2)

def crop_img_func():
	global orignal,crop_img
	global x_start, y_start, x_end, y_end
	print(x_start, y_start, x_end, y_end)
	x1,y1,x2,y2 = convert_para(x_start, y_start, x_end, y_end)
	crop_img = orignal[y1:y1+(y2-y1), x1:x1+(x2-x1)]

	cv2.imwrite("cropped%d.jpg"%cropCount, crop_img)

def select_file():
	root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
	return (root.filename)

def add_frame():

	img   = Image.open("cropped%d.jpg"%cropCount).resize((200, 200))
	imgtk = ImageTk.PhotoImage(image = img)
	img2   = Image.open("owner.jpg").resize((200, 200))
	imgtk2 = ImageTk.PhotoImage(image = img2)
	imglbl1.imgtk = imgtk
	imglbl1.configure(image=imgtk)
	imglbl2.imgtk = imgtk2
	imglbl2.configure(image=imgtk2)
	global var2,plateno
	var2.set(plateno)
	global lblname , lblemail ,lblvehicletype , lblvehiclecompany
	lblname.configure(text = "Name : "+name)
	lblemail.configure(text = "Email : "+email)
	lblvehicletype.configure(text = "Vehice Type : "+vehicletype)
	lblvehiclecompany.configure(text ="Vehicle Company : "+ vehiclecompany)
	#lblplateno = tk.Label(MidRightFrm,text=plateno,relief=tk.RIDGE,bd=1).grid(row = countplace, column = 1,pady = 5,padx = 5)

def linesonvid(event):
	global xline,yline
	xline,yline = event.x,event.y
	global x_end,y_end
	if moveper:
		x_end = event.x
		y_end = event.y

timer_id = None

def start_loading(n=0):
	global timer_id
	gif = giflist[n%len(giflist)]
	canvas.create_image(gif.width()//2, gif.height()//2, image=gif)
	timer_id = root.after(100, start_loading, n+1) # call this function every 100ms

def stop_loading():
	if timer_id:
		root.after_cancel(timer_id)
		canvas.delete(ALL)

def GenerateChallan():
	try:
		showLoading()
		StatusGui.configure(text="Generating Challan...")
		StatusGui.update()
		global chnNo 
		chnNo = "INDGUJ"
		chnNo += str(random.randrange(10000000, 99999999))
		# global var2,plateno
		# plateno = var2.get()
		location = "akhbarnagar-ahemdabad"
		ccc = chn.challan(chnNo,plateno,date,name,location,vehicletype,tuple(OffenceList),challancount,conn)
		ccc.GenerateChallan()
		ccc.AddChallanToDb()
		if isWindows():
			convert( 'challans/'+str(chnNo)+'.docx',  'Pdfs/'+str(chnNo)+'.pdf')
		else:
			result = convert_to('Pdfs',  'challans/'+str(chnNo)+'.docx', timeout=15)
		StatusGui.configure(text="Challan Generated Successful.")
		StatusGui.update()
		stopLoading()
		showPdf()
		# 
	except Exception as e:
		print(e)
		StatusGui.configure(text="Challan Generated Unsuccessful.")
		StatusGui.update()
		stopLoading()



def SendMail():
	Em = Email.Email_Chn()
	Em.SendMail(email,chnNo,plateno,date,name,location,"Pdfs/"+chnNo+".pdf")
	StatusGui.configure(text="Mail Sent.")
	StatusGui.update()


def showPdf():
	# pages = convert_from_path(r'Pdfs/'+chnNo+'.pdf',size=(800,900))
	pages = convert_from_path(r'Pdfs/'+"INDGUJ15626597"+'.pdf',size=(800,900))

	pdf = tk.Toplevel(root)

	topbar = tk.Frame(pdf,bg=clr2,relief=tk.GROOVE,bd=2)

	sendBut = tk.Button(topbar,text="send",bg="green",command=SendMail,fg="white",relief=tk.GROOVE,bd=2)
	sendBut.pack(side = tk.RIGHT)
	
	global pdfText
	tk.Label(topbar, text= "Send Mail TO : ",bg=clr2, fg=clr3, font=("Helvetica", 15)).pack(side = tk.LEFT , fill = tk.X)
	pdfText= tk.Label(topbar, text= email,bg=clr2, fg=clr3, font=("Helvetica", 15))
	pdfText.pack(side = tk.LEFT , fill = tk.X)

	topbar.pack(side = tk.TOP , fill = tk.X)
	imgfrm = tk.Frame(pdf,bg=clr2,relief=tk.GROOVE,bd=2)
	imgtk4 = ImageTk.PhotoImage(pages[0])#.resize((400, 400)))
	imglbl4 = tk.Label(imgfrm,image=imgtk4,relief=tk.GROOVE,bd=1)
	imglbl4.pack(side = tk.TOP)#grid(row = 1, column = 1,pady = 15,padx = 5,sticky = tk.E)
	imglbl4.update()
	imgfrm.pack(side = tk.TOP , fill = tk.X)
	# imgfrm.update()
	# pdf.update() 


	if email == "":
		sendBut.configure(state=tk.DISABLED)
		sendBut.update()

	pdf.mainloop()
	
def mouse_crop_left(event):
	global x_start, y_start,moveper
	moveper=True
	x_start = event.x
	y_start = event.y

def mouse_crop_right(event):
	global x_end,y_end,moveper
	moveper=False
	y_end = event.y

def skip_part():
	global count,cap	
	count+=100
	cap.set(1,count)
	currentFrame()

def skip_part_back():
	global count,cap	
	count-=100
	cap.set(1,count)
	currentFrame()

def skip_part_small():
	global count,cap	
	count+=30
	cap.set(1,count)
	currentFrame()

def skip_part_back_small():
	global count,cap	
	count-=30
	cap.set(1,count)
	currentFrame()

def currentFrame():
	global btnLive
	if cap.get(1) == FrameCount:
		btnLive.configure(fg="Green")
		return True
	else:
		btnLive.configure(fg="red")
		return False


def GoLive():
	global count
	count = FrameCount
	cap.set(1,FrameCount)
	currentFrame()

def convert_to(folder, source, timeout=None):
	args = [libreoffice_exec(), '--headless', '--convert-to', 'pdf', '--outdir', folder, source]

	process = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
	filename = re.search('-> (.*?) using filter', process.stdout.decode())

	return filename.group(1)


def libreoffice_exec():
	if sys.platform == 'darwin':
		return '/Applications/LibreOffice.app/Contents/MacOS/soffice'
	return 'libreoffice'

def call_Our_API():
	showLoading()
	StatusGui.configure(text="Please Wait Calling API...")
	StatusGui.update()
	if x_start == 0 or y_start == 0 or x_end == 0 or y_end == 0:
		print("Not Selected")
		return 0 
	crop_img_func()
	regions = ['in', 'it']
	with open("cropped%d.jpg"%cropCount, 'rb') as fp:
		response = requests.post(
			# 'http://192.168.1.227:8000/test/',
			configjson_data['APIURL'],
			files=dict(Img_upload=fp))
	print("================== Res Get ====================")
	pprint(response.json())
	val = dict()
	try:    
		dix = json.loads((str(response.content)[2:-1]))
		print(dix)
		dix = dict(dix)
		detected = dix['Key']['No_Plate']
		if detected:
			AllKeys = list(dix['Key']['Detecte_Plates'].keys())
			print(AllKeys)
			for i,key in enumerate(AllKeys):
				print('[KEY]',key)
				plateFound = dix['Key']['Detecte_Plates'][key]['FINAL_PRED']['Result']
				Coord = dix['Key']['Detecte_Plates'][key]['FINAL_PRED']['Coord']
				if len(plateFound)>=1:
					y1,x1,w,h =Coord
					global plateno,var2
					plateno = plateFound
					var2.set(plateno)
					print((x1,x1+w,y1,y1+h))
					cropNoPlate((x1,x1+w,y1,y1+h))
				else:
					StatusGui.configure(text="Plate NotFound.")
					StatusGui.update()
					print("NotFound")
		else:
			StatusGui.configure(text="Plate NotFound.")
			StatusGui.update()

	except Exception as e:
		print(e)
		val={'error':e}
		StatusGui.configure(text="Api Response Failed.")
		StatusGui.update()
	finally:
		img   = Image.open("cropped%d.jpg"%cropCount).resize((200, 200))
		imgtk = ImageTk.PhotoImage(image = img)
		imglbl1.imgtk = imgtk
		imglbl1.configure(image=imgtk)
		StatusGui.configure(text="Got Api Response.")
		StatusGui.update()
		stopLoading()


def call_API():
	if x_start == 0 or y_start == 0 or x_end == 0 or y_end == 0:
		print("Not Selected")
		return 0 
	crop_img_func()
	regions = ['in', 'it']
	with open("cropped%d.jpg"%cropCount, 'rb') as fp:
		response = requests.post(
			'https://api.platerecognizer.com/v1/plate-reader/',
			data=dict(regions=regions),  # Optional
			files=dict(upload=fp),
			headers={'Authorization': 'Token ffc2f3a3f63be539ffa0e80fa92b15a1996d5753'})
	pprint(response.json())
	print(response.json())
	response_dict = response.json()

	try:
		print(response_dict['results'])
		print(len(response_dict['results']))
		print("*"*20)
		if len(response_dict['results'])>0:
			no = (response_dict['results'][0]['plate'])
			cords = (response_dict['results'][0]['box'])
			x1,x2,y1,y2 = cords['xmax'],cords['xmin'],cords['ymax'],cords['ymin']
			print(no)
			global plateno,var2
			plateno = no
			var2.set(plateno)
			print((x1,x2,y1,y2))
			cropNoPlate((x1,x2,y1,y2))
		
	except Error as e:
		print("Error : ",e)
	finally:
		img   = Image.open("cropped%d.jpg"%cropCount).resize((200, 200))
		imgtk = ImageTk.PhotoImage(image = img)
		imglbl1.imgtk = imgtk
		imglbl1.configure(image=imgtk)

class ImageLabel(tk.Label):
	"""a label that displays images, and plays them if they are gifs"""
	def load(self):
		im = 'loading6.gif'
		if isinstance(im, str):
			im = Image.open(im)
		self.loc = 0
		self.frames = []
		try:
			for i in count(1):
				self.frames.append(ImageTk.PhotoImage(im.copy()))
				im.seek(i)
		except EOFError:
			pass

		try:
			self.delay = im.info['duration']
		except:
			self.delay = 100

		if len(self.frames) == 1:
			self.config(image=self.frames[0])
		else:
			self.next_frame()

	def unload(self):
		self.config(image="")
		self.frames = None

	def next_frame(self):
		if self.frames:
			self.loc += 1
			self.loc %= len(self.frames)
			self.config(image=self.frames[self.loc])
			self.after(self.delay, self.next_frame)

def showLoading():
	global lbl_load
	lbl_load = tk.Toplevel(root)
	lbl_load.geometry("500x100")
	lbl_load.overrideredirect(True) 
	lblHeadingpop = tk.Label(lbl_load, text=" ◴ Loading Please Wait...",bg=clr1, fg=clr3, font=("Helvetica", 20),relief=tk.RIDGE,bd=5)
	lblHeadingpop.pack(fill = tk.BOTH , expand=True)
	lbl_load.update()
	x = root.winfo_x()
	y = root.winfo_y()
	ww = root.winfo_width()
	hh = root.winfo_height() 
	w = lbl_load.winfo_width()
	h = lbl_load.winfo_height()  
	lbl_load.geometry("%dx%d+%d+%d" % (w, h, x + (ww//2-w//2), y + (hh//2-h//2) ))
	lbl_load.update()
	# img = ImageLabel(root)
	# img.mainloop()
	# img.load()

def stopLoading():
	# lbl_load.unload()
	try:
		global lbl_load
		lbl_load.destroy()
	except:
		pass

def APIconnection():
	global APIgui
	url = configjson_data['APIURL']
	timeout = 5
	try:
		request = requests.get(url, timeout=timeout)
		print("Connected to the Internet")
		APIgui.configure(text="Connected")
		APIgui.configure(bg="green")
	except (requests.ConnectionError, requests.Timeout) as exception:
		print("No internet connection.")
		APIgui.configure(text="Not Connected")
		APIgui.configure(bg="red")


def write_file(data, filename):
	with open(filename, 'wb') as f:
		f.write(data)


def read_blob(filename,q):
	#===============Database connection====================
	global conn
	
	print("==pass==",conn)
	try:
		cursor = conn.cursor()
		cursor.execute(q)
		photo = cursor.fetchone()[0]
		write_file(photo, filename)

	except Error as e:
		print("==error!!!!!!!!!!!!!!!!!!!")
		print(e)
	finally:
		cursor.close()
		#conn.commit()

def SubmitPlate():
	global E1
	global name,email,vehicletype,vehiclecompany,plateno,challancount
	plateno = E1.get()
	sql = 'SELECT image FROM rto where plateno = "' + plateno +'"'
	read_blob("owner.jpg",sql)
	sql2 = 'SELECT name,email,vehicletype,vehiclecompany,challancount FROM rto where plateno = "' + plateno +'"'
	cursor = conn.cursor()
	cursor.execute(sql2)
	name,email,vehicletype,vehiclecompany,challancount = cursor.fetchone()
	challancount = int(challancount)
	challancount2 = challancount+1
	sqlupdate = 'UPDATE rto SET challancount='+str(challancount2)+' where plateno = "' + plateno +'"'
	cursor.execute(sqlupdate)
	print(name,email,vehicletype,vehiclecompany)
	print("showing now")
	add_frame()
	conn.commit()

def pauseit():
	global btnpause
	if var1.get():
		var1.set(0)
		btnpause.configure(bg = "gray")
	else:
		var1.set(1)
		btnpause.configure(bg = clr1)
	currentFrame()

OffenceList = []

def offenceSum():
	global checkListVars,choices,OffenceList
	OffenceList = []
	for j,i in enumerate(checkListVars):
		if(i.get()):
			print(choices[j])
			OffenceList.append((choices[j],OffenceFine[j],OffenceFine2[j]))
	print()
	GenerateChallan()

def dbconn():
	try :
		showLoading()
		global conn
		conn = mysql.connector.connect(	host=configjson_data['DBconn']['host'],
										user=configjson_data['DBconn']['user'],
										passwd=configjson_data['DBconn']['passwd'],
										database=configjson_data['DBconn']['database'],
										port=configjson_data['DBconn']['port'])
		print(conn)
		DBgui.configure(text="Connected")
		DBgui.configure(bg="green")
		stopLoading()

	except Exception as e:
		DBgui.configure(text="Not Connected")
		DBgui.configure(bg="red")
		stopLoading()

def cropNoPlate(cords):
	global crop_img
	x1,x2,y1,y2 = cords
	noplateimg = crop_img[y1:y2, x1:x2]
	noplateimg = cv2.resize(noplateimg,(200,70))
	noplateimg = Image.fromarray(noplateimg)
	imgtk5 = ImageTk.PhotoImage(image = noplateimg)
	imglbl3.imgtk = imgtk5
	imglbl3.configure(image=imgtk5)

def openVideo():
	filename =  filedialog.askopenfilename(initialdir = configjson_data['VideoPath'],title = "Select file",filetypes = (("MP4 File","*.mp4"),("all files","*.*")))
	print (' [ SELECTED VIDEO ] ',filename)
	global cap,count, FrameCount
	cap = cv2.VideoCapture(filename)
	width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
	height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
	count = 0
	FrameCount = 0

def KeyDown(event):
	#print(event)
	if event.char == " ":
		pauseit()
	elif event.keycode == 37:
		skip_part_back_small()
	elif event.keycode == 39:
		skip_part_small()

def Vid_Speed_set(n):
	global Vid_Speed
	Vid_Speed = n


# clr1 = "#26282B"
# clr2 = "#343434"
# clr3 = "#FFC54A"
clr1 = "#0C0D0B"
clr2 = "#262624"
clr3 = "#FFC54A"


#=============================================================( TOP HEADING )===========================================================
TopFrm = tk.Frame(root,bg=clr1,relief=tk.RAISED,bd=5)

Heading = "Traffic Violation E-Challan Generation"
Heading = "AUTOMATED GENERATION OF CHALLAN ON VIOLATION OF TRAFFIC RULES"

lblHeading = tk.Label(TopFrm, text= Heading,bg=clr1, fg=clr3, font=("Helvetica", 23,"bold"))
lblHeading.grid(row=0, column=0,sticky="news", padx=10, pady=10)

TopFrm.pack(side = tk.TOP,fill = tk.X)

TopFrm.grid_rowconfigure(0, weight=1)
TopFrm.grid_columnconfigure(0, weight=1)

#=============================================================( MANU BAR )===========================================================

def donothing():
   filewin = tk.Toplevel(root)
   button = Button(filewin, text="Do nothing button")
   button.pack()

menubar = tk.Menu(root)

filemenu = tk.Menu(menubar, tearoff = 0)
#filemenu.add_command(label="New", command = donothing)
filemenu.add_command(label = "Open Video", command = openVideo)
#filemenu.add_command(label = "Save", command = donothing)
filemenu.add_command(label = "Connect API", command = APIconnection)
filemenu.add_command(label = "Connect Database", command = dbconn)
filemenu.add_separator()
filemenu.add_command(label = "Exit", command = root.quit)
menubar.add_cascade(label = "File", menu = filemenu)

#editmenu = tk.Menu(menubar, tearoff=0)
#editmenu.add_command(label = "Undo", command = donothing)

# editmenu.add_separator()

# editmenu.add_command(label = "Cut", command = donothing)
# editmenu.add_command(label = "Copy", command = donothing)
# editmenu.add_command(label = "Paste", command = donothing)
# editmenu.add_command(label = "Delete", command = donothing)
# editmenu.add_command(label = "Select All", command = donothing)

#menubar.add_cascade(label = "Edit", menu = editmenu)
helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label = "Help Index", command = donothing)
helpmenu.add_command(label = "About...", command = donothing)
menubar.add_cascade(label = "Help", menu = helpmenu)
root.config(menu = menubar)


#=============================================================( MID FRAME )===========================================================          
MidFrm = tk.Frame(root,bg=clr2)

#===========================================================( MID LEFT FRAME )===========================================================          
MidLeftFrm = tk.Frame(MidFrm,bg=clr2,relief=tk.GROOVE,bd=2)
# default = Image.open("test1.png")
# default = default.resize(ResizePara,Image.ANTIALIAS)

#===========================================================( Video FRAME )===========================================================          
MidLeftTopFrm = tk.Frame(MidLeftFrm,bg=clr2,relief=tk.GROOVE,bd=2)

defaultimg = Image.fromarray(np.zeros((400,400)))
defaultimg = ImageTk.PhotoImage(image = defaultimg)

Vidlbl = tk.Label(MidLeftTopFrm,name="image",image=defaultimg,width=ResizePara[0], height=ResizePara[1],relief=tk.GROOVE,bd=2)
Vidlbl.image = defaultimg
Vidlbl.pack(side = tk.TOP ,fill = tk.Y)
Vidlbl.bind("<Button-1>", mouse_crop_left)
Vidlbl.bind("<ButtonRelease-1>", mouse_crop_right)#<Button-3>
Vidlbl.bind("<Motion>", linesonvid)
#Vidlbl.bind("<B1-Motion>", linesonvid)
Vidlbl.config(cursor="cross")
MidLeftTopFrm.pack(side = tk.TOP,fill = tk.X,expand=False)
#btnok = tk.Label(MidLeftFrm, text="o", fg=clr3, bg=clr1,font=("Helvetica", 10))
#btnok.pack(side = tk.RIGHT)

#======================================================( MID LEFT BOTTOM FRAME )===========================================================          
MidLeftBtmFrm = tk.Frame(MidLeftFrm,bg=clr2)

var1  = tk.IntVar() 
var1.set(1)
#pause = tk.Checkbutton(MidLeftBtmFrm, text='pause', variable=var1).grid(row=0, column = 0, sticky=tk.W)
#btnCrop  = tk.Button(MidLeftBtmFrm, text= "Crop Img", command = crop_img_func,fg="black", bg="#B1A296",font=("Helvetica", 10)).grid(row = 0, column = 0,pady = 5,padx = 5)
btnFFBack    = tk.Button(MidLeftBtmFrm, text= "<<<", command = skip_part_back,fg=clr3, bg=clr1,font=("Helvetica", 10))\
.grid(row = 0, column = 0,pady = 5,padx = 5,sticky="we")
btnFFBack    = tk.Button(MidLeftBtmFrm, text= "<<",  command = skip_part_back_small,fg=clr3, bg=clr1,font=("Helvetica", 10))\
.grid(row = 0, column = 1,pady = 5,padx = 5,sticky="we")
btnpause     = tk.Button(MidLeftBtmFrm, text= "pause", command = pauseit, fg=clr3, bg=clr1,font=("Helvetica", 10))
btnpause.grid(row = 0, column = 2,pady = 5,padx = 5,sticky="we")
btnFF        = tk.Button(MidLeftBtmFrm, text= ">>",  command = skip_part_small, fg=clr3, bg=clr1,font=("Helvetica", 10))\
.grid(row = 0, column = 3,pady = 5,padx = 5,sticky="we")
btnFF        = tk.Button(MidLeftBtmFrm, text= ">>>", command = skip_part, fg=clr3, bg=clr1,font=("Helvetica", 10))\
.grid(row = 0, column = 4,pady = 5,padx = 5,sticky="we")
MidLeftBtmFrm.grid_columnconfigure(0, weight=1)
MidLeftBtmFrm.grid_columnconfigure(1, weight=1)
MidLeftBtmFrm.grid_columnconfigure(2, weight=1)
MidLeftBtmFrm.grid_columnconfigure(3, weight=1)
MidLeftBtmFrm.grid_columnconfigure(4, weight=1)

MidLeftBtmFrm.pack(side = tk.TOP,fill = tk.BOTH,expand=False)


#======================================================( MID LEFT BOTTOM FRAME )===========================================================          
MidLeftBtmFrm2 = tk.Frame(MidLeftFrm,bg=clr2)
btnCall      = tk.Button(MidLeftBtmFrm2, text= "Find No Plate", command = call_Our_API,fg=clr3, bg=clr1,font=("Helvetica", 10))\
.grid(row = 1, column = 0,pady = 5,padx = 5,sticky="we")
btnLive      = tk.Button(MidLeftBtmFrm2, text= "GoLive", command = GoLive,fg=clr3, bg=clr1,font=("Helvetica", 10))
btnLive.grid(row = 1, column = 1,pady = 5,padx = 5,sticky="we")
#btnLive1      = tk.Button(MidLeftBtmFrm2, text= "addData", command = addChallanData,      fg=clr3, bg=clr1,font=("Helvetica", 10))\
#.grid(row = 1, column = 1,pady = 5,padx = 5)
MidLeftBtmFrm2.grid_columnconfigure(0, weight=1)
MidLeftBtmFrm2.grid_columnconfigure(1, weight=1)
MidLeftBtmFrm2.pack(side = tk.TOP,fill = tk.BOTH,expand=False)




MidLeftBtmFrm3 = tk.Frame(MidLeftFrm,bg=clr2)

x1  = tk.Button(MidLeftBtmFrm3, text= "1x", command = lambda : Vid_Speed_set(1),fg=clr3, bg=clr1,font=("Helvetica", 10))\
.grid(row = 0, column = 0,pady = 5,padx = 5,sticky="we")
x2  = tk.Button(MidLeftBtmFrm3, text= "2x", command = lambda : Vid_Speed_set(2),fg=clr3, bg=clr1,font=("Helvetica", 10))\
.grid(row = 0, column = 1,pady = 5,padx = 5,sticky="we")
x4 	= tk.Button(MidLeftBtmFrm3, text= "4x", command = lambda : Vid_Speed_set(4), fg=clr3, bg=clr1,font=("Helvetica", 10))\
.grid(row = 0, column = 2,pady = 5,padx = 5,sticky="we")
x8 	= tk.Button(MidLeftBtmFrm3, text= "8x", command = lambda : Vid_Speed_set(8), fg=clr3, bg=clr1,font=("Helvetica", 10))\
.grid(row = 0, column = 3,pady = 5,padx = 5,sticky="we")
x16	= tk.Button(MidLeftBtmFrm3, text= "16x",command = lambda : Vid_Speed_set(16), fg=clr3, bg=clr1,font=("Helvetica", 10))\
.grid(row = 0, column = 4,pady = 5,padx = 5,sticky="we")
x32	= tk.Button(MidLeftBtmFrm3, text= "32x",command = lambda : Vid_Speed_set(32), fg=clr3, bg=clr1,font=("Helvetica", 10))\
.grid(row = 0, column = 5,pady = 5,padx = 5,sticky="we")
MidLeftBtmFrm3.grid_columnconfigure(0, weight=1)
MidLeftBtmFrm3.grid_columnconfigure(1, weight=1)
MidLeftBtmFrm3.grid_columnconfigure(2, weight=1)
MidLeftBtmFrm3.grid_columnconfigure(3, weight=1)
MidLeftBtmFrm3.grid_columnconfigure(4, weight=1)
MidLeftBtmFrm3.grid_columnconfigure(5, weight=1)

MidLeftBtmFrm3.pack(side = tk.TOP,fill = tk.BOTH,expand=False)



MidLeftFrm.pack(side = tk.LEFT,fill = tk.BOTH,expand=False)

#==========================================================( MID RIGHT FRAME )===========================================================          

MidRightFrm = tk.Frame(MidFrm,bg=clr2,relief=tk.GROOVE,bd=2)

#========================================================( MID RIGHT IMG FRAME )===========================================================          

MidRighttopFrm = tk.Frame(MidRightFrm,bg=clr2)


MidRightImgFrm = tk.Frame(MidRighttopFrm,bg=clr2,relief=tk.GROOVE,bd=2)

imglbl1 = tk.Label(MidRightImgFrm,image=defaultimg,width=200, height=200,relief=tk.GROOVE,bd=1)
imglbl1.grid(row = 0, column = 0,pady = 5,padx = 5)
tk.Label(MidRightImgFrm, text= " Vehicle ",bg=clr1, fg=clr3, font=("Helvetica", 12),relief=tk.RIDGE,bd=2).grid(row = 1, column = 0,pady = 3,padx = 3,sticky="news")

imglbl2 = tk.Label(MidRightImgFrm,image=defaultimg,width=200, height=200,relief=tk.GROOVE,bd=1)
imglbl2.grid(row = 0, column = 1,pady = 5,padx = 5)
tk.Label(MidRightImgFrm, text= " Vehicle owner",bg=clr1, fg=clr3, font=("Helvetica", 12),relief=tk.RIDGE,bd=2).grid(row = 1, column = 1,pady = 3,padx = 3,sticky="news")
MidRightImgFrm.grid_columnconfigure(1, weight=1)
MidRightImgFrm.grid_columnconfigure(0, weight=1)
MidRightImgFrm.grid(row = 0, column = 0,pady = 0,padx = 0,sticky='news')#pack(side = tk.LEFT,fill = tk.BOTH )

#========================================================( MID RIGHT DATA FRAME )===========================================================          

MidRightDataFrm = tk.Frame(MidRighttopFrm,bg=clr2,relief=tk.GROOVE,bd=2)

imglbl3 = tk.Label(MidRightDataFrm,image=defaultimg,width=200, height=70,relief=tk.GROOVE,bd=1)
imglbl3.grid(row = 0, column = 0 ,pady = 5,padx = 5)

var2 = tk.StringVar()
E1 = tk.Entry(MidRightDataFrm,font=("Helvetica", 15),textvariable=var2,bd =1)
btnok 				= tk.Button(MidRightDataFrm, text="Submit Plate", command = SubmitPlate, fg=clr3, bg=clr1,font=("Helvetica", 10))

# tk.Label(MidRightDataFrm,  text= "Name :",bg=clr1, fg=clr3,relief=tk.GROOVE,font=("Helvetica", 10)).grid(row = 3, column = 0,pady = 2,padx = 2, stick = "we")
lblname 			= tk.Label(MidRightDataFrm,  text= name,bg=clr1, fg=clr3,relief=tk.GROOVE,font=("Helvetica", 10),anchor="w")
# tk.Label(MidRightDataFrm,  text= "Email :",bg=clr1, fg=clr3,relief=tk.GROOVE,font=("Helvetica", 10)).grid(row = 4, column = 0,pady = 2,padx = 2, stick = "we")
lblemail 			= tk.Label(MidRightDataFrm,  text= email,bg=clr1, fg=clr3,relief=tk.GROOVE,font=("Helvetica", 10),anchor="w")
# tk.Label(MidRightDataFrm,  text= "Vehicle Type :",bg=clr1, fg=clr3,relief=tk.GROOVE,font=("Helvetica", 10)).grid(row = 5, column = 0,pady = 2,padx = 2, stick = "we")
lblvehicletype 		= tk.Label(MidRightDataFrm,  text= vehicletype,bg=clr1, fg=clr3,relief=tk.GROOVE,font=("Helvetica", 10),anchor="w")
# tk.Label(MidRightDataFrm,  text= "Vehicle Company :",bg=clr1, fg=clr3,relief=tk.GROOVE,font=("Helvetica", 10)).grid(row = 6, column = 0,pady = 2,padx = 2, stick = "we")
lblvehiclecompany 	= tk.Label(MidRightDataFrm,  text= vehiclecompany,bg=clr1, fg=clr3,relief=tk.GROOVE,font=("Helvetica", 10),anchor="w")

E1.grid(				row = 1, column = 0,pady = 3,padx = 5)
btnok.grid(				row = 2, column = 0,pady = 3,padx = 5)
lblname.grid(			row = 3, column = 0,pady = 3,padx = 5 , stick = "we")
lblemail.grid(			row = 4, column = 0,pady = 3,padx = 5 , stick = "we")
lblvehicletype.grid(	row = 5, column = 0,pady = 3,padx = 5 , stick = "we")
lblvehiclecompany.grid(	row = 6, column = 0,pady = 3,padx = 5 , stick = "we")

# MidRightDataFrm.grid_columnconfigure(1, weight=1)
MidRightDataFrm.grid_columnconfigure(0, weight=1)

MidRightDataFrm.grid(row = 0, column = 1,pady = 0,padx = 0,sticky='news')#.pack(side = tk.TOP,fill = tk.X,expand=False)

MidRighttopFrm.grid_rowconfigure(0, weight=1)
MidRighttopFrm.grid_rowconfigure(1, weight=1)
MidRighttopFrm.grid_columnconfigure(1, weight=1)
MidRighttopFrm.grid_columnconfigure(0, weight=1)

MidRighttopFrm.pack(side = tk.TOP,fill = tk.BOTH )



#========================================================( MID RIGHT LIST FRAME )===========================================================          
MidRightbtmFrm = tk.Frame(MidRightFrm,bg = clr2)

MidRightListFrm = tk.Frame(MidRightbtmFrm,bg=clr2,relief=tk.GROOVE,bd=2)
# choices = tuple(configjson_data['Offances'])
# choices = ( 'Violating parking rules',			
# 			'Not wearing a helmet',
# 			'Driving a motor vehicle at a speed which is dangerous to the public',
# 			'Not Wearing Seatbelt',
# 			'Breaching traffic signal',
# 			'having additional Person sitting on driving seat',
# 			'overloading of 2Wheelers',
# 			)
checkListVars = []
choices = []
OffenceFine = []
OffenceFine2 = []
# print(configjson_data['Offances_cost'])
for i in configjson_data['Offances']: 
    choices.append(i['Offance']) 
    OffenceFine.append(i['fine1']) 
    OffenceFine2.append(i['fine2']) 

print(choices)
print(OffenceFine)
print(OffenceFine2)
# OffenceFine = configjson_data['OffenceFine']
# OffenceFine = ["500","1000","1500","1000","500","500","2000"]
# OffenceFine2 = configjson_data['OffenceFine2']
# OffenceFine2 = ["1000","1000","1500","1000","1000","500","2000"]

tk.Label(MidRightListFrm,text="Select Offence",font=("Helvetica", 18 , "bold"),bg=clr1, fg=clr3,bd=2)\
.grid(row=0,column = 0,ipadx = 25,sticky='news',columnspan = 2)
butlocno = 0

for i,line in enumerate(choices):
	varaa1 = tk.IntVar()
	checkListVars.append(varaa1)
	tk.Checkbutton(MidRightListFrm, text=line, variable=checkListVars[i],bg=clr2, fg=clr3,\
	selectcolor=clr1,justify = tk.LEFT,font=("Helvetica", 12),anchor = "w")\
	.grid(row=i+1, sticky='we',column = 0,columnspan = 2)
	butlocno+=1
	
btnTotal = tk.Button(MidRightListFrm, text= "Generate Challan", command = offenceSum, fg=clr3, bg=clr1,font=("Helvetica", 10))\
.grid(row = butlocno+1, column = 0,pady = 10,padx = 10 , sticky="we")
btnTotal = tk.Button(MidRightListFrm, text= "Show Challan", command = showPdf, fg=clr3, bg=clr1,font=("Helvetica", 10))\
.grid(row = butlocno+1, column = 1,pady = 10,padx = 10 , sticky="we")
# btnTotal = tk.Button(MidRightListFrm, text= "GenerateChallan", command = GenerateChallan, fg=clr3, bg=clr1,font=("Helvetica", 10))\
# .grid(row = butlocno+3, column = 0,pady = 5,padx = 5)
MidRightListFrm.grid_columnconfigure(0, weight=1)
MidRightListFrm.grid_columnconfigure(1, weight=1)

MidRightListFrm.pack(side = tk.TOP,fill = tk.BOTH,expand=True)

MidRightbtmFrm.pack(side = tk.BOTTOM,fill = tk.BOTH,expand=True)

MidRightFrm.pack(side = tk.RIGHT,fill = tk.BOTH , expand=True)

MidFrm.pack(side = tk.TOP,fill = tk.BOTH , expand=True)
#=============================================================( Bottom frame )===========================================================

BtmFrm = tk.Frame(root,bg=clr2,relief=tk.RIDGE,bd=2)

StatusGui = tk.Label(BtmFrm, text= "Status....",bg=clr2, fg=clr3, font=("Helvetica", 10))
StatusGui.pack(side = tk.LEFT)
DBgui = tk.Label(BtmFrm, text= "Not Connected",bg="red", fg="white", font=("Helvetica", 10),relief=tk.RIDGE,bd=2)
DBgui.pack(side = tk.RIGHT)
tk.Label(BtmFrm, text= "Database : ",bg=clr2, fg=clr3, font=("Helvetica", 10),relief=tk.RIDGE,bd=2).pack(side = tk.RIGHT)
APIgui = tk.Label(BtmFrm, text= "Connected",bg="green", fg="white", font=("Helvetica", 10),relief=tk.RIDGE,bd=2)
APIgui.pack(side = tk.RIGHT)
tk.Label(BtmFrm, text= "API : ",bg=clr2, fg=clr3, font=("Helvetica", 10),relief=tk.RIDGE,bd=2).pack(side = tk.RIGHT)

BtmFrm.pack(side = tk.BOTTOM,fill = tk.BOTH)


root.bind("<Key>",KeyDown)
#=============================================================( TOP HEADING )===========================================================

APIconnection()
show_frame()
cv2.destroyAllWindows()
root.mainloop()
configjson.close() 