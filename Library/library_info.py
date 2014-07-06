import numpy as np
import csv
import matplotlib.pyplot as plt
from collections import OrderedDict
from itertools import groupby


def fitem(item):
	item=item.strip()
	try:
		item=float(item)
	except ValueError:
		pass
	return item

def blankremove(somelist):
	while '' in somelist:
		somelist.remove('')
	return somelist

with open('Master_Library2.csv', 'r') as csvin:

	reader=csv.DictReader(csvin)
	data={k.strip():[fitem(v)] for k,v in reader.next().items()}
	for line in reader:
		for k,v in line.items():
			k=k.strip()
			data[k].append(fitem(v))

yearlist = data["Year"]
sublist = data["subjects"]

yearlist = blankremove(yearlist)
sublist = blankremove(sublist)

sublist2 = []
for x in range(len(sublist)):
	sublist2.append(sublist[x].split(";"))
sublist2 = [item for sublist in sublist2 for item in sublist]


print np.mean(yearlist)
yearlist = [int(x) for x in yearlist]
yearlist.sort(key=int)
yearfreq = [len(list(group)) for key, group in groupby(yearlist)]
Years = list(OrderedDict.fromkeys(yearlist))
print min(Years)
print max(Years)

sublist2.sort(key=str)
subfreq = [len(list(group)) for key, group in groupby(sublist2)]
Subjects = list(OrderedDict.fromkeys(sublist2))
print Subjects[subfreq.index(max(subfreq))],max(subfreq)

plt.figure(1)
plt.plot(Years,yearfreq)
plt.plot(Years,yearfreq,'bo')
# plt.figure(2)
# X = range(len(subfreq))
# plt.xticks(X, Subjects, rotation=90)
# plt.plot(X,subfreq)
plt.show()
