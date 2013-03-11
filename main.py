# lightnews -- light usenet client
# authors:	mplonski / maciej plonski / sokoli.pl
#		ksx4system / ksx4system.net

import lnlib

# init!
ut = lnlib.UsenetGroup()

rinput = raw_input("Gimme gimme gimme server name >> ")
ut.connect(rinput)
print "OK" if ut.isconnected() else "NO"


