import csv

def CSVCompare(Filename,Comparand):
	csvfile = Filename + ".csv"
	reader = csv.reader(open(csvfile, 'rb'), delimiter=',')
	CompDict = dict(x for x in reader)
	print CompDict

	if Comparand not in CompDict.values():

		ID = int(max(CompDict.iterkeys())) + 1
		CompDict.update({ID:Comparand})

	else:
		ID = CompDict.keys()[CompDict.values().index(Comparand)] 
	
	return ID,Comparand


myfile = CSVCompare("Topics",raw_input("Enter the topic you would like to search for:"))#raw_input("File Name:"),raw_input("Thing to search for:"))

print myfile