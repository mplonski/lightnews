def tryit():
	try:
		import time
		return 0
	except:
		return 1

if tryit() == 0:
	print ("ok")
else:
	print ("nok")
