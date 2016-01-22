from logClass import *
from glob import glob
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def plot_bestfit(data):
	data = list(data)
	indexes = range(0,len(data))
	m, b = np.polyfit(indexes, data, 1)
	plt.plot(indexes, m*indexes + b, '-',linewidth=0.3)

def plot_average(data,c='r',linewidth=3):
	avg = np.average(data)
	plt.axhline(y=avg,c=c,linewidth=linewidth,label='Average')
	plt.legend(loc='best')

def logLengths_plot(logList,bestFit=False,avg=True):
	"""Plots a graph of log wordCounts over time"""
	lengths = [int(x.wordCount) for x in logList]
	plt.plot(lengths,'y',linewidth=0.3)
	plt.plot(lengths,'y',linewidth=2.0,marker='o')
	if bestFit: plot_bestfit(lengths)
	if avg: plot_average(lengths)
	plt.grid(color='r', linestyle='-', linewidth=0.1)
	plt.title('Length of logs')
	plt.xlabel('Log Number')
	plt.ylabel('Word Count')
	plt.show()

def logLengths_hist(logList,):
	"""Plots a histogram of log wordCounts"""
	logList = list(logList)
	lengths = []
	if isinstance(logList[0],Memory): #Check if logList is a list of Memorys
		for memory in logList:
			lengths.append(memory.wordCount)

	elif isinstance(logList[0],str): #Is list of filenames, using glob
		for memory in loadMemories(logList):
			lengths.append(memory.wordCount)
	else:
		print('Invalid type passed. List of: {} '.format(type(llogList[0])))

	plt.hist(lengths,bins=10,facecolor='y')
	plt.title('Length of logs')
	plt.ylabel('Number of logs')
	plt.xlabel('Word Count')
	plt.tight_layout()
	plt.show()

def logLengths_scat(loglist,color='m',size=50):
	loglist = list(loglist)
	y = [l.wordCount for l in loglist]
	x = [(int(l.month)) for l in loglist]

	plt.xticks(range(1,13),[toMonth(l)[0:3] for l in range(1,13)])
	plt.ylim([0,(max(y)+min(y))])
	plt.xlim([1,12])
	plt.ylabel('Word Count')
	plt.scatter(x,y,c=color,s=size,edgecolor=color)
	plt.show()


if __name__ == '__main__':
	swears = 'wordLists/swearWords.txt'
	people = 'wordLists/people.txt'
	memoryFolder = glob('logs//*') 
	allMems = loadMemories(memoryFolder) #A list of all memories

	logLengths_plot(allMems)

	#allWords = findWords(memoryFolder,hideEmpty=True,minLen=0,ascending=True)
	#for log in allMems:
	#	print(log.title)

