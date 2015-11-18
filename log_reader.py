from log_stats import *
from tkinter import *

memoryFolder = glob('logs//*') 
loadMemories(memoryFolder)

color_1 = '#FFFFFF' 
color_2 = '#8A3636' #Root Background RED
color_3 = '#958dba'
color_4 = '#b2ba8d'
color_5 = '#CAE6B8' #Button Background
color_6 = None
button_font = ('courier new',10)
title_font = ('courier new',18)

current = None #Stores the current frame being displayed


root = Tk()

sideBar = Frame(root,bg=color_1,width=160)
sideBar.pack(side='left',fill='both',ipadx=10,ipady=10)
sideBar.pack_propagate(0)


def make_side(container,buttons):
	global current
	Label(container,text='Side Bar',font=title_font,bg=color_6,width=18).pack()
	for button in buttons:
		Button(container,text=button[0],bg=color_5,font=button_font,width=18,command=lambda button=button:change(button[1],current)).pack()

def frame_1(): 
	global current
	mainZone = Frame(root,bg=color_4,width=640)
	mainZone.pack(side='right',fill='both')
	mainZone.pack_propagate(0)
	current = mainZone

	Label(mainZone,text='Search',font=title_font).pack()

def frame_2():
	global current
	mainZone = Frame(root,bg=color_3,width=640)
	mainZone.pack(side='right',fill='both')
	mainZone.pack_propagate(0)
	current = mainZone

def change(toFrame,origin):
	if origin != None:
		origin.destroy()
	toFrame()


buttonList = [('Search',frame_1),('Frame 2',frame_2)]
make_side(sideBar,buttonList)
root.geometry('{}x{}'.format(800,500))
root.config(bg=color_2)
root.mainloop()