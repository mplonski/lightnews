#!/usr/bin/python
# name:			lightnews
# description:	light usenet client
# authors:		mplonski / maciej plonski / sokoli.pl
#				ksx4system / ksx4system.net
# licence:		GNU GPL
#

try:
	from psycopg2.extensions import adapt
	import getpass, hashlib, time, socket
	import sys, tempfile, os, sqlite3, nntplib
	import getpass, readline
	import lnlib, lnio, lncmd
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
co.quit()

