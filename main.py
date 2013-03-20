#!/usr/bin/python
# name:		lightnews
# description:	light usenet client
# authors:	mplonski / maciej plonski / sokoli.pl
#		ksx4system / ksx4system.net
# licence:	GNU GPL
#

# TODO: changed cache based on files to sqlite, main.py require
# to reconsider and rewrite
# doing it right now, commiting just to backup :-)

settings = None

import sys
try:
	import getpass, readline, lnlib, lnio
except:
	sys.exit("Error: python libraries are not available")

DEBUG = 1 # 1 -- debug, 0 -- normal

# init!
ut = lnlib.UsenetGroup()
io = lnio.lnio()

if not settings == None:
	io.setfilename(settings)
io.getoptions()

print ('Hello! This program is not ready yet ;)')

def docmd(cmd):
	groups = io.getgroups()

	cm = cmd.split(" ")

	# ONLY FOR DEBUG
	print cm

	# adding group
	if cm[0] == "addgroup" and len(cm) == 3:
		io.addgroup(cm[1], cm[2])
		print("Added new group")
	elif cm[0] == "addgroup":
		print("Error! Use 'addgroup server group'.")

	# displaying groups
	elif cm[0] == "groups":
		print("Your groups:")
		i = 0
		for g in groups:
			c = " " if io.isgroupcache(g[0]) == 0 else " [c] "
			print(" " + str(i) + ":" + c + g[0] + " on server " + g[1])
			i += 1
		if i == 0:
			print("No groups found")

	# displaying information about group
	elif cm[0] == "group" and len(cm) == 2:
		if int(cm[1]) >= len(groups):
			print("Error! This group doesn't exist!")
			return 0

		# get group info & cache for group
		group = groups[cm[1]]
		cache = getc_group(group[1], group[0])
		ut.setservergroup(group[1], group[0])

		# there is no cache for this group
		if cache == None:
			if not group[1] == ut.getservername():
				ut.connect(group[1])
			res, count, first, last, name = ut.getgroup(cm[1])
			iscache = -1
		else:
			res, count, first, last, name, iscache = cache

		print ("Group %s has %s articles, first one is %i and last one is %s" % (name, count, first, last))

		if iscache > 0:
			print ("Cache is enabled for last %s articles" % cache[4])
		elif iscache == 0:
			print ("Cache is enabled only for group info")
		else:
			print ("There is no cache available for this group.")
	elif cm[0] == "group":
		print("Error! Use 'group groupid'")

	# dispalying last 10 or chosen articles in group
	elif cm[0] == "list" and ( (len(cm) == 3) or (len(cm) == 1) ):
		cache = getc_group_art(ut.getservername(), ut.getgroupname())
		if cache == None:
			# TODO first, last
			if ut.getservername() == ut.
			res, count, first, last, name = ut.getgroup(
			resp, subs = ut.getarticles('subject', first, last)
			# TODO :P
		else:
			for art in cache[-10:]:
				print(" " + str(art) + ": " + getcachearticle(ut.getgroupname(), art))
		resp, subs = ut.getarticles('subject', first, last)
		for id, sub in subs[int(cm[1]):int(cm[2])]:
			print id, sub

	# getting article
	elif cm[0] == "article" and len(cm) == 2:
		resp, num, n2id, nlist = ut.getbody(cm[1])
		for k in nlist:
			print k

	# getting head
	elif cm[0] == "h" and len(cm) == 2:
		resp, num, n2id, nlist = ut.gethead(cm[1])
		for k in nlist:
			print k
	else:
		print "Commands: will be one day ;)"

cmd = raw_input(' > ')
while (not (cmd == 'q')):
	docmd(cmd)
	cmd = raw_input(' > ')

