"""
Available functions:

	Saving/Loading:
	
	fullWordList(folderPath):
		[IN]
			folderPath: type(glob): directory containing log files
		[OUT]
			type(list[str]): list containing all instances of all words in a given folder, with duplicates.
	
	loadMemories(folderPath):
		[IN]
			folderPath: type(glob): directory containing log files
		[OUT]
			type(generator[Memory]): all logs as Memory objects
	
	averageLength(folderPath):
		[IN]
			folderPath: type(glob): directory containing log files
		[OUT]
			type(int): the average word count of all log files
	
	lengthRank(folderPath,type,numToReturn,*echo):
		[IN]
			folderPath: type(glob): directory containing log files
			type: type(str): either 'longest' or 'shortest'
			numToReturn: type(int): the  top x number of Memory objects to return
			*echo: type(bool): print out formatted result 
		[OUT]
			type(list[Memory]): orderest list of x Memory objects
	
	findWords(logFile,*query,*ascending,*alphabetical,*minLen,*hideEmpty):
		[IN]
			logFile: type(glob): directory containing log files
			*query: type(str) OR type(list): str, filepath or list; of words to find
			*ascending:  type(bool): result in ascending order
			*alphabetical: type(bool): result in alphabetical order
			*minLen: type(int): minimum letter length of word to return
			*hideEmpty: type(bool): hide words with a count of 0
		[OUT]
			type(list[str]): list of words 
	
	filterByDate(loglist,*date,*day,*month,*year):
		[IN]
			loglist: type(list[Memory]): list of Memory objects
			*date: type(str): ___currently not functioning___
			*day: type(str): specific day to find
			*month: type(str): specific month to find
			*year: type(str): specific year to find
		[OUT]
			type(list[Memory]): all Memory objects that meet a given date criteria
	
	logsByMonth(logList,*month): 
		[IN] 
			logList: type(list[Memory]): list of Memory objects
			*month: type(str): specific month to return
		[OUT]
			type(list[tuple]): ___appears to be broken___
	
	toMonth(monthNo):
		[IN]
			monthNo: type(str): number of chosen month; (1-12)
		[OUT]
			type(str): name of month
	
	sortByLogLength(logList,*ascending):
		[IN]
			logList: type(list[Memory]): list of Memory objects
			*ascending: type(bool): result in ascending order
		[OUT]
			type(list[Memory]): sorted Memory objects by wordCount
	
	stdPrint(values):
		[IN]
			values: type(list[tuple]) OR type(dict): values to output
		[OUT]
			None

	spoolToTxt(loglist,filename):
		[IN]
			loglist: type(list(Memory)): List of memories to spool
			filename: type(str): Name of file to spool to (will be created/overwritten)
		[OUT]
			None
"""
from collections import Counter
from glob import glob
import string

class Memory():
	def __init__(self,textFile):
		"""textFile= *.txt file to be loaded as a memory object"""
		self.components = textFile.split("-")
		self.date = ("/".join((self.components[0:3]))).replace("\n","")
		self.day = self.date[8:10]
		self.month = self.date[5:7]
		self.year = self.date[0:4]
		self.title = str(self.components[3]).replace("\n","")
		self.text = "".join((self.components[4::]))
		self.wordCount = len(self.toList())
		self.wordList = self.toList()
		self.wordDict = Counter(self.toList())

	def toList(self):
		"""Returns a list of words in a memory without punctuation"""
		removalChars = [',','\n','\t','-',';','/','!','.',]
		exclude = set(list(string.punctuation) + ['\r','£','â']) #Creates list of characters to exclude/
		fullText = '{} {}'.format(self.text,self.title)
		for char in removalChars:
			fullText = (fullText).lower().replace(char,' ')
		noPunc = ''.join(ch for ch in fullText if ch not in exclude) #Removes all exception characters from string
		noPunc = noPunc.replace('  ',' ') #Replaces double spaces with singles
		noNums = ''.join(i for i in noPunc if not i.isdigit()) #Removes all numerical digits from string
		return noNums.split(' ') #Returns the final string as a list

def loadMemories(folderPath=glob("logs//*")):
	"""Returns all memory logs in a given directory as Memory objects."""
	for file in folderPath: 
		yield Memory(open(file,'r').read())

def fullWordList(folderPath):
		"""Returns list of every instance of words in a given folder"""
		allWords = []
		for log in loadMemories(folderPath):
			allWords = allWords + log.toList()
		
		return allWords

def averageLength(folderPath):
	total,divider = 0,0
	
	for memory in loadMemories(folderPath):
		total += memory.wordCount
		divider += 1
	return int(total/divider)

def lengthRank(folderPath,type,numToReturn,echo=True,):
	"""Returns a list of the x number of shortest/longest logs in a given log directory"""

	if type == 'shortest':
		lenSorted = sorted(list(loadMemories(folderPath)),key=lambda x: int(x.wordCount))
	elif type == 'longest':
		lenSorted = sorted(list(loadMemories(folderPath)),key=lambda x: -int(x.wordCount))
	else:
		print('type variable must be \'longest\' or \'shortest\'' )

	xLongest = lenSorted[0:numToReturn]
	counter= 1

	if echo:
		print('WordCount\t\tDate\t\tTitle')
		for log in xLongest:
			print('[{}] {}\t|\t{}\t|\t{}'.format(counter,log.wordCount,log.date,log.title,))
			counter +=1

	return xLongest

def findWords(logFile,query=False,ascending=True,alphabetical=False,minLen=False,hideEmpty=False):
	"""
	Used to find the number of words used in all memory logs.
	logFile:   str, Directory path of log files
	query:     str,list or filepath, of words to find
	ascending: bool, decides how returned list is sorted.
	alphabetical: bool, decides how returned list is sorted
	minLen: int, minimum length of word to return. 
	"""

	def wordCounts(folderPath,query=False,minWordLength=False):
		"""
		Returns a dictionary of word counts for a given folder.
		Using a query allows only specific words to be returned.
		"""
		def removeShortWords(wordDict,minLen):
			"""Removes words that are lower than a given length"""
			toremove = []
			for word in wordDict:
				if len(word) <= minLen-1:
					toremove.append(word)
			for key in toremove:
				del wordDict[key]

		listOfWords = fullWordList(logFile)
		if query:
			for word in listOfWords:
				if str(word) not in query:
					listOfWords= list(filter((word).__ne__, listOfWords))

		countedDict = dict(Counter(listOfWords))
		if query:
			if not hideEmpty:
				for word in query:
					if word not in listOfWords:
						countedDict[word] = 0

		if minWordLength:
			removeShortWords(countedDict,minLen=minWordLength)
	
		return countedDict
	
	def sortWords(dictionary,ascending=True,alphabetical=False):
		"""
		Converts a dictionary to a list of tuples and sorts in ascending order.
		"""
		outList = []
		for pair in dictionary:
			outList.append((pair,dictionary[pair]))
	
		if alphabetical:
			index = 0
		else:
			index = 1

		if ascending:
			return sorted(outList,key=lambda x: x[index])
		else:
			return list(reversed(sorted(outList,key=lambda x: x[index])))
	
	def countFromFile(logFile,wordsFile):
		"""Returns a sorted word count of all logs in a directory. Words are taken from a .txt file."""
		with open(wordsFile,'r') as wordsFile:
			loadedWordList = [str(i) for i in wordsFile.read().split(',')]
		return sortWords(wordCounts(fullWordList(logFile), query=loadedWordList,minWordLength=minLen),ascending=ascending,alphabetical=alphabetical)

	def countFromList(logFile, wordList):
		"""Returns a sorted word count of all logs in a directory. List of words is supplied"""
		return sortWords(wordCounts(fullWordList(logFile), query=wordList,minWordLength=minLen),ascending=ascending,alphabetical=alphabetical)

	if query == False:
		return sortWords(wordCounts(fullWordList(logFile),minWordLength=minLen),ascending=ascending,alphabetical=alphabetical)
	elif isinstance(query, str):
		try:
			return countFromFile(logFile,query)
		except FileNotFoundError:
			return sortWords(wordCounts(fullWordList(logFile), query=[query]),ascending=ascending,alphabetical=alphabetical)
	elif isinstance(query, list):
		return countFromList(logFile,query)
	else:
		print('TypeError: findWords(): query must be str or list, not type({})'.format(type(query)))


def findInstances(loglist,word):
	"""Finds all logs that contain a given word"""
	loglist = list(loglist)
	if isinstance(loglist[0], str):
		loglist = loadMemories(loglist)
	elif isinstance(loglist[0], Memory):
		loglist
	for log in loglist:
		if word in log.text:
			yield log

def filterByDate(loglist,date=False,day=False,month=False,year=False):
	"""Searches through a list of logs and returns only those that meet the given date."""
	def checkFor(log,criteria,typeOfCriteria):
		critTypes={
			'day': log.day,
			'month': log.month,
			'year': log.year,
		}
		if criteria:
			if int(critTypes[typeOfCriteria]) == int(criteria):
				return log
		else:
			return True
	logs = list(loglist)
	matches = []

	for log in logs:
		if checkFor(log,day,'day') and checkFor(log,month,'month') and checkFor(log,year,'year'):
			matches.append(log)
	return matches

def totalWordCount(loglist):
	count = 0
	for log in loglist:
		count += log.wordCount
	return count


def logsByMonth(logList,month=False):
	"""Sorts a list of logs by their month"""
	monthCounts = []
	for m in ['01','02','03','04','05','06','07','08','09','10','11','12']:
		monthCounts.append((m,len(filterByDate(logList,month=m))))
	return sorted(monthCounts,key=lambda log:log[1])

def toMonth(monthNo):
	"""Takes a number and returns the corresponding month name"""
	mNames = {
		1: 'January',
		2: 'February',
		3: 'March',
		4: 'April',
		5: 'May',
		6: 'June',
		7: 'July',
		8: 'August',
		9: 'September',
		10: 'October',
		11: 'November',
		12: 'December',
	}
	return mNames[int(monthNo)]

def sortByLogLength(logList,ascending=True):
	"""Sorts a list of memory logs by their wordcount"""
	return sorted(logList, key=lambda mem: mem.wordCount)

def statsPrint(logFile,words=True,logs=True,mostUsed=False):
	"""Takes a directory as an arguement and returns statistics based on the logs found."""
	listOfMemories = list(loadMemories(logFile))
	sortedByUse = findWords(logFile,query=False,ascending=False,alphabetical=False,)
	sortedByLength = sortByLogLength(listOfMemories)
	def wordStats():
		print('-Words')
		print('Total unique words:\t{}'.format(len(sortedByUse)))
		print('Total words used:\t{}'.format(len(fullWordList(logFile))))
		print('Most used word:\t\t\'{}\' ({})'.format(sortedByUse[0][0],sortedByUse[0][1]))
	def logStats():
		print('-Logs')
		print('Number of logs:\t\t{}'.format(len(sortedByLength)))
		print('Average log length:\t{}'.format(averageLength(logFile)))
		print('Longest log:\t\t{}\t({}: {})'.format(sortedByLength[-1].wordCount,sortedByLength[-1].date,sortedByLength[-1].title))
		print('Shortest log:\t\t{}\t({}: {})'.format(sortedByLength[0].wordCount,sortedByLength[0].date,sortedByLength[0].title))
		print('Oldest log:\t\t{}/{}\t({})'.format(listOfMemories[0].day,listOfMemories[0].month,listOfMemories[0].title))
		print('Newest log:\t\t{}/{}\t({})'.format(listOfMemories[-1].day,listOfMemories[-1].month,listOfMemories[-1].title))
		print('Busiest month:\t\t{}\t({} entries)'.format(toMonth(logsByMonth(listOfMemories)[-1][0])[0:3],logsByMonth(listOfMemories)[-1][1]))
		print('Quietest month:\t\t{}\t({} entries)'.format(toMonth(logsByMonth(listOfMemories)[0][0])[0:3],logsByMonth(listOfMemories)[0][1]))
	def mostUsedWords():
		stdPrint(findWords(logFile,query=False,ascending=False,alphabetical=False,minLen=4)[0:9])
	if logs: logStats()
	if words: wordStats()
	if mostUsed: mostUsedWords()

def stdPrint(values):
	"""Prints a list or dictionary in a standard format"""
	if isinstance(values, list):
		for tup in values:
			print('{}\t: {}'.format(tup[0],tup[1]))

	elif isinstance(values, dict):
		for wordKey in values:
			print('{}\t: {}'.format(wordKey,values[wordKey]))
	else:
		print('TypeError: stdPrint() takes dictionary or list of tupes as arg.\ntype({}) was passed'.format(type(values)))

def wordCountToCsv(listOfWords,filename,echo=True):
	"""Exports the current list (with numbers) to a csv file."""
	outCsv = open(filename,'w')
	for tup in listOfWords:
		outCsv.write('{},{}\n'.format(tup[0],tup[1]))
	outCsv.close()
	if echo:
		print('Saved to {}'.format(filename))
	return filename

def spoolToTxt(loglist,filename):
	"""Creates a file from giving logs."""
	to = open(filename,'w')
	for log in loglist:
		to.write('{}: {}'.format(log.date,log.title))
		to.write('{}'.format(log.text))
		to.write('\n\n-------------------------------------\n')
	to.close()

if __name__ == '__main__':
	directory = glob('logs//*')
	allMemories = loadMemories(directory)
	spoolToTxt(allMemories,'testMyAss.txt')