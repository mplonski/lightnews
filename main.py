#!/usr/bin/python
# name:		lightnews
# description:	light usenet client
# authors:	mplonski / maciej plonski / sokoli.pl
#		ksx4system / ksx4system.net
# licence:	GNU GPL
#

# TODO: changed cache based on files to sqlite
# main.py requires to reconsider and rewrite
# doing it right now, commiting just to backup :-)

import sys
try:
	import getpass, readline, lnlib, lnio
except:
	sys.exit("Error: python libraries are not available")

# init!
ut = lnlib.UsenetGroup()
io = lnio.lnio()

print ('Hello! This program is not ready yet ;)')
print ('Need to go to the university, will finish it later')

cmd = raw_input(' > ')
while (not ( (cmd == 'q') or (cmd == 'quit') ) ):
	docmd(cmd)
	cmd = raw_input(' > ')

