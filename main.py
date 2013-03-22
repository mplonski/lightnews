#!/usr/bin/python
# name:			lightnews
# description:	light usenet client
# authors:		mplonski / maciej plonski / sokoli.pl
#				ksx4system / ksx4system.net
# licence:		GNU GPL
#

try:
	import os, sys, sqlite3, getpass, readline
	import lnlib, lnio, lncmd
	from psycopg2.extensions import adapt
except:
	sys.exit("Error: python libraries are not available")

database = os.path.expanduser("~") + "/.lightnews.db"
if not os.path.exists(database):
	import make.setupdb
	make.setupdb.setupdb(database)

# init!
ut = lnlib.UsenetGroup()
io = lnio.lnio(database)
co = lncmd.lncmd(ut, io)

print ('Hello! This program is not ready yet ;)')

cmd = co.getcmd()
while (not cmd in co.getend() ):
	co.docmd(cmd)
	cmd = co.getcmd()

