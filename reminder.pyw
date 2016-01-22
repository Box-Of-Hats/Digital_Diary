import glob
from datetime import date
import datetime
from tkinter import *
import os
import log_reader

def todayWritten(folderpath="logs/**"):
	for filename in glob.glob(folderpath):
		name = str(filename)
		name = name.replace("logs\\","")
		name = name.replace(".txt","")
		if str(date.today()) == name:
			return True

def launchReminder():

	def openTXT(documentName):
		os.system("start "+ documentName)

	def createTXT(dateToUse):
		thisDate = str(dateToUse)
		fileString = ("logs\\" +  thisDate + ".txt")
		filename = open(fileString,"w")
		filename.write(thisDate + "\n\n-Title-\n\n")
		filename.close()
		openTXT(fileString)
		root.destroy()

	def closeWindow():
		root.destroy()

	def keyListener(event):
		createTXT(datehere.get())

	def statsLaunch():
		log_reader.main()

	root = Tk()
	Label(text="        ").grid(row=1,column=10)
	Label(text="        ").grid(row=1,column=9)
	Label(text="        ").grid(row=1,column=12)
	Label(text="You haven't written an entry today.\n ").grid(row=10,column=10,columnspan=2)
	Label(text="Would you like to write one now?").grid(row=12,column=10,columnspan=2)
	Button(text="Yes",command= lambda: createTXT(datehere.get())).grid(row=15,column=10)
	Button(text="No",command= lambda: closeWindow()).grid(row=15,column=11)
	Button(text="Stats",command= lambda: statsLaunch()).grid(row=18,column=10,columnspan=2)
	datehere = Entry(root)
	datehere.grid(row=16,column=10,columnspan=2)
	datehere.insert(0,str(date.today()))
	Label(text="     ").grid(row=20,column=10)
	root.bind('<Return>',keyListener)
	root.mainloop()

if __name__ == "__main__":
	if not todayWritten():
		launchReminder()

