# lightnews -- light usenet client
# authors:	mplonski / maciej plonski / sokoli.pl
#		ksx4system / ksx4system.net

import lnlib

DEBUG = 1 # 1 -- debug, 0 -- normal

# init!
ut = lnlib.UsenetGroup()

# DEBUG
if  DEBUG == 1:
	ut.connect('news.gmane.org')
	(resp, count, first, last, name) = ut.getgroup('gmane.comp.python.committers')


# THIS IS ALPHA!
if DEBUG == 0:
	rinput = raw_input("Gimme gimme gimme server name >> ")
	ut.connect(rinput)

if ut.isconnected():
	print ut.getwelcome()
else:
	print "error"

if DEBUG == 0:
	rinput = raw_input("Gimme gimme gimme group name >> ")
	(resp, count, first, last, name) = ut.getgroup(rinput)

print ('Group ' + name + ' has '+ count + ' articles, range ' + first + ' to ' + last)

cmd = raw_input(' > ')
while (not (cmd == 'q')):
	print "ok\n"
	cm = cmd.split(" ")
	if cm[0] == "g":
		(resp, count, first, last, name) = ut.getgroup(cm[1])
		print "Done!"
	elif cm[0] == "s":
		ut.disconnect()
		ut.connect(cm[1])
		if ut.connected():
			print ut.getwelcome()
		else:
			print "blad!"
	elif cm[0] == "l" and len(cm) == 1:
		resp, subs = ut.getarticles('subject', first, last)
		for id, sub in subs[-10:]:
			print id, sub
	elif cm[0] == "l" and len(cm) == 3:
		resp, subs = ut.getarticles('subject', first, last)
		for id, sub in subs[int(cm[1]):int(cm[2])]:
			print id, sub
	elif cm[0] == "a" and len(cm) == 2:
		resp, num, n2id, nlist = ut.getbody(cm[1])
		for k in nlist:
			print k
	elif cm[0] == "h" and len(cm) == 2:
		resp, num, n2id, nlist = ut.gethead(cm[1])
		for k in nlist:
			print k
	print cm

	cmd = raw_input(' > ')

resp, subs = ut.getarticles('subject', first, last)
for id, sub in subs[-10:]:
	print id, sub

