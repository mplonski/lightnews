#!/usr/bin/python
# name:		lightnews
# description:	light usenet client
# authors:	mplonski / maciej plonski / sokoli.pl
#		ksx4system / ksx4system.net
# licence:	GNU GPL
#

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
		groups = io.getgroups()
		i = 0
		for g in groups:
			c = " " if io.isgroupcache(g[0]) == 0 else " [c] "
			print(" " + str(i) + ":" + c + g[0] + " on server " + g[1])
			i += 1

	# displaying information about group
	elif cm[0] == "group" and len(cm) == 2:
		groups = io.getgroups()
		if int(cm[1]) > len(groups):
			print("Error! This group doesn't exist!")
			return 0
		if io.isgroupcache(g[0]) == -1:
			res, count, first, last, name = ut.getgroup(cm[1])
			print ("Group %s has %s articles, first one is %i and last one is %s" % (name, count, first, last))
			print ("There is no cache available for this group.")
			return 0
		else:
			cache = io.getcache(cm[1])
			print ("Group %s has %s articles, first one is %i and last one is %i" & (cache[3], cache[0], cache[1], cache[2]))
			if cache[4] > 0:
				print ("There is cache available for %s last articles" % cache[4])
			elif cache[4] == 0:
				print ("There is cache available only for group info")
			else:
				print ("There is no cache available for this group.")
	elif cm[0] == "group":
		print("Error! Use 'group groupname'")

	# dispalying last 10 or chosen articles in group
	elif cm[0] == "list" and ( (len(cm) == 3) or (len(cm) == 1) ):
		cache = getcachearticles(ut.getgroupname())
		if cache == None:
			# TODO first, last
			resp, subs = ut.getarticles('subject', first, last)
			# TODO :P
		else:
			for art in cache:
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

