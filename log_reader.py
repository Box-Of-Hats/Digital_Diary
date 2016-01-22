from log_stats import *
from tkinter import *
import log_reminder as rem
from datetime import date
import subprocess
from win32api import GetSystemMetrics


current = None #Stores the current frame being displayed
onTop = False #Should the window be always on top

def main():
	global current
	pathToUse = glob('logs//*')

	color_1 = '#FFFFFF' #White
	color_2 = '#8A3636' #Root Background RED
	color_3 = '#CCDAE0' #Main Frames
	color_4 = '#BCE3E1' #Sidebar
	color_5 = '#CAE6B8' #Button Background,
	color_6 = None
	button_font = ('courier new',10,'bold')
	title_font = ('courier new',18,'bold')
	body_font = ('courier new',10)


	root = Tk()
	sideBar = Frame(root,bg=color_4,width=160)
	sideBar.pack(side='left',fill='both',ipadx=10,ipady=10)
	sideBar.pack_propagate(0)


	def make_side(container,buttons):
		global current
		Label(container,text='Side Bar',font=title_font,bg=color_4,width=18).pack()
		for button in buttons:
			Button(container,text=button[0],bg=color_5,font=button_font,width=18,command=lambda button=button:change(button[1],current)).pack()

	def frame_1(container,): # Today Frame. Allows user to create a new log and view stats of todays, if written.
		bg = color_3
		container.config(bg=bg)
		Label(container,text='Today',font=title_font,bg=bg).pack()
		if rem.todayWritten(pathToUse):
			Label(container,text='You\'ve already written a log entry today.',font=title_font,bg=bg).pack()
			Button(container,text='Open/Edit',font=button_font,bg=color_5,command=lambda: rem.openTXT('logs/{}.txt'.format(date.today()))).pack()
		else:
			Label(container,text='You haven\'t written a log entry today.',font=title_font,bg=bg).pack()
			dateToWrite = Entry(container,)
			dateToWrite.pack()
			dateToWrite.insert(0,date.today())
			Button(container,text='Write Entry',font=button_font,bg=color_5,command=lambda: rem.createTXT(str(dateToWrite.get()))).pack()

	def frame_stats(container,):
		bg = color_3
		container.config(bg=bg)
		Label(container,text='Log Stats',font=title_font,bg=bg).pack()

		#Calculations required for stats:
		listOfMemories = list(loadMemories(pathToUse))
		sortedByLength = sortByLogLength(listOfMemories)

		stats = [('Total number of logs',len(sortedByLength)),
				('Average word count', averageLength(pathToUse)),
				('Longest log entry','{} words ({})'.format(sortedByLength[-1].wordCount,sortedByLength[-1].title)),
				('Shortest log entry','{} words ({})'.format(sortedByLength[0].wordCount,sortedByLength[0].title)),
				('Oldest log','{} ({})'.format(listOfMemories[0].date,listOfMemories[0].title)),
				('Newest log','{} ({})'.format(listOfMemories[-1].date,listOfMemories[-1].title)),
				('Busiest month','{} ({} entries)'.format(toMonth(logsByMonth(listOfMemories)[-1][0])[0:3],logsByMonth(listOfMemories)[-1][1])),
				('Quietest month','{} ({} entries)'.format(toMonth(logsByMonth(listOfMemories)[0][0])[0:3],logsByMonth(listOfMemories)[0][1])),
				('Total word count','{} words'.format(totalWordCount(listOfMemories)))
				]

		#Create labels for each statistic:
		for stat in stats:
			Label(container,text='{}: {}'.format(stat[0],stat[1]),font=body_font,bg=bg).pack(pady=2,padx=2,anchor='w')

		#Graph Buttons:
		graphFrame = Frame(container,bg=bg)
		graphFrame.pack()
		bestFit = IntVar()

		Checkbutton(graphFrame,text='Best Fit',variable=bestFit,bg=bg,font=body_font).pack(anchor='w')
		Button(graphFrame,text='Length Hist',command=lambda:logLengths_hist(listOfMemories),font=button_font,bg=color_5).pack(side='right')
		Button(graphFrame,text='Length Scat',command=lambda:logLengths_scat(listOfMemories,),font=button_font,bg=color_5).pack(side='right')
		Button(graphFrame,text='Length Plot',command=lambda:logLengths_plot(listOfMemories,bestFit=bool(bestFit.get())),font=button_font,bg=color_5).pack(side='right')


	def frame_word_stats(container,args=[1,10,3]):
		"""args is a list, such that:
		args[0] = lower bound of words to list
		args[1] = upper bound of words to list
		args[2] = minimum word length to list
		"""
		def mostUsed(container):
			def returnPress(event):
				change(frame_word_stats,container,args=[1,10,int(ent_minlen.get())])

			def search(bot=1,top=10,minlen=3):
				change(frame_word_stats,container,args=[int(bot),int(top),int(minlen)])
			#Most used words:
			mostUsedFrame = Frame(container)
			mostUsedFrame.pack(anchor='w',)
			minlenCont = Frame(mostUsedFrame)
			minlenCont.pack(anchor='w')
			ent_minlen = Entry(minlenCont)
			ent_minlen.pack(side='right')
			ent_minlen.focus_set()
			Label(minlenCont,text='Min Length:',bg=bg,font=body_font).pack(side='right')
			ent_minlen.insert(0,args[2])
			Button(container,text='Search',font=button_font,bg=color_5,command=lambda: search(top=10,minlen=ent_minlen.get())).pack(anchor='w')

			botx = args[0]
			topx = args[1]
			minlen = args[2]

			ranks = findWords(pathToUse,query=False,ascending=False,alphabetical=False,minLen=minlen)[botx-1:topx]
			counter = botx
			for rank in ranks:
				Label(container,text='{}. {}: {}'.format(counter,rank[0],rank[1]),font=body_font,bg=bg).pack(anchor='w')
				counter+=1

			ent_minlen.bind("<Return>", returnPress)

		bg = color_3
		container.config(bg=bg)
		Label(container,text='Word Stats',font=title_font,bg=bg).pack()
		mostUsed(container)

	def frame_options(container,):
		def toggle_ontop():
			global onTop
			onTop = not onTop
			root.wm_attributes("-topmost",onTop)

		def open_code(filename):
			program = 'C:\Program Files\Sublime Text 2\sublime_text.exe'
			subprocess.Popen('{} {}'.format(program,filename))
			quit()

		bg = color_3
		Label(container,text='Options',font=title_font,bg=bg).pack()
		container.config(bg=bg)
		Button(container,width=18,text='Toggle On Top',font=button_font,bg=color_5,command=lambda:toggle_ontop()).pack()
		Button(container,width=18,text='Sourcecode',font=button_font,bg=color_5,command=lambda:open_code('log_reader.py')).pack()
		txtName = Entry(container,font=body_font)
		txtName.pack()
		txtName.insert(0,'fullSpooled.txt')
		Button(container,width=18,text='Spool To Txt',font=button_font,bg=color_5,command=lambda:spoolToTxt(loadMemories(pathToUse),txtName.get())).pack()


	def change(toFrame,origin,args=False):
		if origin != None:
			origin.destroy()
		global current
		mainZone = Frame(root,bg=color_3,width=640)
		mainZone.pack(side='right',fill='both')
		mainZone.pack_propagate(0)
		current = mainZone
		if args:
			toFrame(mainZone,args)
		else:
			toFrame(mainZone)

	buttonList = [('Today',frame_1),('Log Stats',frame_stats),('Word Stats',frame_word_stats),('Options',frame_options)]
	make_side(sideBar,buttonList)
	change(frame_1,None)
	sw,sh = GetSystemMetrics(0),GetSystemMetrics(1)
	ww,wh = 800,500
	root.geometry('{}x{}+{}+{}'.format(ww,wh,int(0.5*sw-ww/2),int(0.5*sh-wh/2)))
	root.config(bg=color_2)
	root.wm_attributes("-topmost",onTop)
	root.mainloop()

if __name__ == '__main__':
	main()
