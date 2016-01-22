import glob
from datetime import date
import datetime
from tkinter import *
import os
import log_reader

def todayWritten(folderpath="logs/**"):
	"""Checks if there is a file with todays date.txt present. Takes a glob as a folderpath. """
	#for filename in glob.glob(folderpath):
	for filename in folderpath:
		name = str(filename)
		name = name.replace("logs\\","")
		name = name.replace(".txt","")
		if str(date.today()) == name:
			return True
	return False

def openTXT(documentName):
	"""Opens a given document with its default application"""
	os.system("start "+ documentName)

def createTXT(dateToUse,closeAfter=True):
	"""Creates a new text document, with the basic template for diary entries. Uses a date as the filename, in form yyyy/mm/dd"""
	thisDate = str(dateToUse)
	fileString = ("logs\\" +  thisDate + ".txt")
	filename = open(fileString,"w")
	filename.write(thisDate + "\n\n-Title-\n\n")
	filename.close()
	openTXT(fileString)
	if closeAfter: exit()
