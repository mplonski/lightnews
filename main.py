# lightnews -- light usenet client
# authors:	mplonski / maciej plonski / sokoli.pl
#		ksx4system / ksx4system.net

import lnlib

# init!
ut = lnlib.UsenetGroup()

# THIS IS ALPHA!
rinput = raw_input("Gimme gimme gimme server name >> ")
ut.connect(rinput)
print "OK" if ut.isconnected() else "NO"

rinput = raw_input("Gimme gimme gimme group name >> ")
(resp, count, first, last, name) = ut.getgroup(rinput)
print ('Group ' + name + ' has '+ count + ' articles, range ' + first + ' to ' + last)


