#!/usr/bin/python
# name:		lightnews
# description:	light usenet client
# authors:	mplonski / maciej plonski / sokoli.pl
#		ksx4system / ksx4system.net
# licence:	GNU GPL
#

try:
		import sys, sqlite3, getpass, readline
		import lnlib, lnio, lncmd
except:
	sys.exit("Error: python libraries are not available")

# init!
ut = lnlib.UsenetGroup()
io = lnio.lnio()
co = lncmd.lncmd(ut, io)

print ('Hello! This program is not ready yet ;)')

cmd = co.getcmd()
while (not cmd in co.getend() ):
	co.docmd(cmd)
	cmd = co.getcmd()

