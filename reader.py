import glob, tkinter as tk, pyautogui as pg
logFolder = glob.glob("logs//*")

class Memory():
	def __init__(self,textFile):
		self.components = textFile.split("-")
		self.date = ("/".join((self.components[0:3]))).replace("\n","")
		self.title = str(self.components[3]).replace("\n","")
		self.text = "".join((self.components[4::]))

	def printAttributes(self):
		print("Date: {}".format(self.date))
		print("Title: {}".format(self.title))
		print("Body: {}".format(self.text))

#Variable for current index of memory in memoryList. Used in the Gui, for the buttons.
globalIndex = 0

def buildGui(memoryList):
	def yielder(memoryList):
		for memory in memoryList:
			yield memory
	def changeMemory(direction):
		global globalIndex
		if direction == 'foreword':
			globalIndex += 1
		else:
			globalIndex -= 1

		try:
			thisDate.set(memoryList[globalIndex].date)
			thisTitle.set(memoryList[globalIndex].title)
			thisBody.set(memoryList[globalIndex].text)
		except:
			if direction == 'foreword':
				globalIndex -= 1 
			else:
				globalIndex += 1
			pg.alert("Ran Out Of Dates!")


	root = tk.Tk()
	thisDate = tk.StringVar()
	thisTitle = tk.StringVar()
	thisBody = tk.StringVar()
	topFrame = tk.Frame(root,width=700,height=300)
	topFrame.pack(side='top')

	bottomFrame = tk.Frame(root,width= 800,height=50)
	bottomFrame.pack(side='bottom')
	nextButton = tk.Button(bottomFrame,command=lambda: changeMemory('foreword'),text="Next")
	nextButton.pack(side='right',pady=10)
	prevButton = tk.Button(bottomFrame,command=lambda: changeMemory('backword'),text="Previous")
	prevButton.pack(side='left',pady=10)

	rightFrame  = tk.Frame(root,width=100,height=350)
	rightFrame.pack(side='right')

	currentIndex = 0 
	memory = memoryList[currentIndex]
	memoryContainer = tk.Frame(topFrame,height=500,width=800)
	memoryContainer.pack()
	thisDate.set(memory.date)
	thisTitle.set(memory.title)
	thisBody.set(memory.text)
	toptop = tk.Frame(memoryContainer,height=100,width=800)
	toptop.pack()
	tk.Label(toptop,textvariable=thisDate).pack(padx=100)
	tk.Label(toptop,textvariable=thisTitle,font=(18)).pack()
	tk.Label(memoryContainer,textvariable=thisBody,wrap=600,justify='left').pack(side='bottom')
	root.geometry("{}x{}".format(800,450))
	root.mainloop()

def loadMemories(folderPath):
	alls = []
	for file in logFolder:
		thisFile = open(file,'r').read()
		tempMemory = Memory(thisFile)
		alls.append(tempMemory)
	return alls


if __name__ == '__main__':
	buildGui(loadMemories(logFolder))