import enchant
d = enchant.Dict("en_US")
while True:
	word = raw_input ("Enter a name")
	if d.check(word) is False:
		print word + " is incorrect"
	else:
		print word + " is correct"