import readline
import csv

def tupni(message, List):
    
    def completer(text, state):
        options = [x for x in lowlist if x.startswith(text)]
        try:
            return options[state]
        except IndexError:
            return None

    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")

    if List:
        lowlist = [x.lower() for x in List]
        word = raw_input(message)
        
        if not (word in lowlist or word == ""):
            writer = csv.writer(open('Subjects.csv', 'a'), delimiter=',')
            writer.writerow([word.title()])
    else:
        word = raw_input(message)

    return word.title()

def CSVToList(Filename):
    csvfile = Filename + ".csv"
    csvfile = csv.reader(open(csvfile, 'rb'), delimiter=',')
    filelist = []
    for item in csvfile:
        filelist.extend(item)
    return filelist

subjects = CSVToList("Subjects")

#print subjects

a = tupni("a: ", subjects)
print "You entered", a
b = tupni("b: ", subjects)
print "You entered", b
c = tupni("c: ", None)
print "You entered", c


