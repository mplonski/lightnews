#
# name:         lightnews' library
# description:  class for lightnews responsible for command line
# authors:      mplonski / maciej plonski / sokoli.pl
#               ksx4system / ksx4system.net
# licence:      GNU GPL
#

from psycopg2.extensions import adapt
import getpass
import nntplib
import random
import hashlib
import time
import socket
import sys
import tempfile
import os

class lncmd:
	def __init__(self, ut, io):
		self.ut = ut
		self.io = io
		self.singlegroup = None

	def analcmd(self, cmd):
		return cmd.split(" ")

	# do your job!
	def docmd(self, cmd):
		self.groups = self.io.getgroups()

		cm = self.analcmd(cmd)

		# Hi!
		if cm[0] == "hello":
			self.hello()

		# sets from field in sent messages
		elif cm[0] == "setfrom" and len(cm) == 2:
			self.setfrom(cm[1])
		elif cm[0] == "setfrom":
			print ("Error! Use 'setfrom name@example.com'")

		# search for groups
		elif cm[0] == "glist" and len(cm) == 3:
			self.getgrouplist(cm[1], cm[2])
		elif cm[0] == "glist":
			print ("Error! Use 'glist server pattern'")

		# adds group
		elif cm[0] == "addgroup" and len(cm) == 3:
			self.addgroup(cm[1], cm[2])
		elif cm[0] == "addgroup":
			print ("Error! Use 'addgroup server group'")

		# removes group
		elif cm[0] == "removegroup" and len(cm) == 3 and self.singlegroup == None:
			self.removegroup(cm[1], cm[2])
		elif cm[0] == "removegroup" and len(cm) == 3 and not self.singlegroup == None:
			print ("Error! 'removegroup' is available only in default mode")
		elif cm[0] == "removegroup":
			print ("Error! Use 'removegroup server group'")

		# list groups
		elif cm[0] == "groups":
			self.listgroups()

		# set auth option for server
		elif cm[0] == "setauth" and len(cm) == 2:
			self.setauth(server=cm[1])
		elif cm[0] == "setauth":
			print ("Error! Use 'setauth server_name'")

		# set cache for group
		elif cm[0] == "setcache" and len(cm) == 1 and not self.singlegroup == None:
			self.setcache(gid=self.singlegroup[0])
		elif cm[0] == "setcache" and len(cm) == 2:
			self.setcache(gid=cm[1])
		elif cm[0] == "setcache" and len(cm) == 3:
			self.setcache(server=cm[1], group=cm[2])
		elif cm[0] == "setcache":
			print ("Error! Use 'setcache' in single-group mode or 'setcache group_id'")

		# gimme group info ;)
		elif cm[0] == "group" and len(cm) == 3:
			self.group(gserver=cm[1], ggroup=cm[2])
		elif cm[0] == "group" and len(cm) == 2:
			self.group(grid=cm[1])
		elif cm[0] == "group" and len(cm) == 1 and not self.singlegroup == None:
			self.group(grid=self.singlegroup[0])
		elif cm[0] == "group":
			print ("Error! Use 'group group_id' or 'group server_name group_name'")

		# messages' list
		elif cm[0] == "list" and (len(cm) == 3) and not self.singlegroup == None:
			self.artlist(0, None, cm[1], cm[2])
		elif cm[0] == "list" and (len(cm) == 2) and not self.singlegroup == None:
			self.artlist(0, cm[1], None, None)
		elif cm[0] == "list" and not self.singlegroup == None:
			self.artlist(0, 10, None, None)
		elif cm[0] == "list" and not self.singlegroup == None:
			print("Error! Use 'list' or 'list number' or 'list start end'")
		elif cm[0] == "list":
			print ("Error! Command 'list' is available only in single-group mode.")

		# messages' list, with read ones
		elif cm[0] == "listall" and (len(cm) == 3) and not self.singlegroup == None:
			self.artlist(1, None, cm[1], cm[2])
		elif cm[0] == "listall" and (len(cm) == 2) and not self.singlegroup == None:
			self.artlist(1, cm[1], None, None)
		elif cm[0] == "listall" and not self.singlegroup == None:
			self.artlist(1, 10, None, None)
		elif cm[0] == "listall" and not self.singlegroup == None:
			print("Error! Use 'listall' or 'listall number' or 'listall start end'")
		elif cm[0] == "list":
			print ("Error! Command 'listall' is available only in single-group mode.")

		# gimme article
		elif cm[0] == "article" and len(cm) == 2 and not self.singlegroup == None:
			self.article(cm[1])
		elif cm[0] == "article" and not self.singlegroup == None:
			print("Error! Use 'article art_id'")
		elif cm[0] == "article":
			print("Error! Command 'article' is available only in single-group mode.")

		# send message
		elif cm[0] == "send" and len(cm) == 2 and not self.singlegroup == None:
			self.sendart(cm[1])
		elif cm[0] == "send" and not self.singlegroup == None:
			self.sendart(None)
		elif cm[0] == "send":
			print("Error! Usage 'send' or 'send art_id'. Available only in group mode.")

		# download messages
		elif cm[0] == "download" and ( (len(cm) == 2) or (len(cm) == 3) ):
			self.download(cm)
		elif cm[0] == "download" and not self.singlegroup == None:
			self.download(["download", str(self.singlegroup[0])])
		elif cm[0] == "download":
			print ("Error! Use 'download' in single-group mode or 'download all' or 'download group_id' or 'download server group'")

		# start/end single-group mode
		elif cm[0] == "setgroup" and len(cm) == 2:
			self.setgroup(cm[1])
		elif cm[0] == "setgroup":
			self.setgroup(None)

		# help
		elif cm[0] == "help":
			self.help()

		else:
			print("Command not found. Run 'help' to display available commands.")
			return 0
				
	def hello(self):
		print("Hello! :-)")

	# just asking for username / password
	def askforauth(self, tmp):
		# 0 means auth is enabled for server
		if not int(tmp) == 0:
			return [None, None]
		print("Authorisation to this server is required!")
		username = raw_input("Username [%s]: " % (getpass.getuser()))
		if username == "":
			username = getpass.getuser()
		password = getpass.getpass()
		return [username, password]

	# powerfull def, checks connection and connects to server/group
	def auth(self, server = None, sid = None, group = None, gid = None, sauth = None):
		if (server == None) and (sid == None) and (not gid == None):
			sid, server, sauth = self.io.getserver(gid=gid)
		elif not ((server == None) and (sid == None)):
			tmp = self.io.getserver(sid=sid, server=server)
			if tmp == None:
				sid = -1
				server = server
				sauth = sauth
			else:
				sid, server, sauth = tmp

		if not ((group == None) and (gid == None)):
			gr = self.io.getgroup(server=server, group=group, gid=gid)
			if gr == None:
				gid = -1
				group = group
			else:
				gid = gr[0]
				group = gr[1]

		# just checking if connection is up
		if server == None and group == None and sid == None and gid == None:
			if not self.ut.isconnected(): # it's not
				group = self.ut.getgroupname()
				server = self.ut.getservername()
				sid, server, sauth = self.io.getserver(server=server)
				gr = self.io.getgroup(server=server, group=group)

				suser, spass = self.askforauth(sauth)
				try:
					self.ut.connect(self.ut.getservername(), suser, spass)
				except:
					print("Error! Cannot connect to the server. Check server name and internet connection")
					return 1
				return 0
			else: # it's up, don't worry, be happy
				return 0
		# connecting to specified server
		else:
			tmp = self.ut.isconnected()
			# not connected or connected to other server
			if (not tmp) or (tmp and not self.ut.getservername() == server):
				suser, spass = self.askforauth(sauth)
				try:
					self.ut.connect(server, suser, spass)
				except:
					print("Error! Cannot connect to the server. Check server name and internet connection")
					return 1
			# if group is set and (not connected or connected to other group)
			if (not group == None) and ((not tmp) or (tmp and not self.ut.getgroupname() == group)):
				try:
					self.ut.getgroup(group)
				except:
					print("Error! Cannot get specified group. Check group_name and internet connection")
					return 1
		return 0

	# get list of group
	def getgrouplist(self, server, pattern):
		print("Please wait...")
		if self.auth(server=server) == 1:
			return None
		gr = self.ut.getlist()[1]
		if len(gr) == 0:
			print("Error! No groups available on this server")
			return 0
		# TODO: is it the best way? what about regex?
		i = 0
		for g in gr:
			if pattern in g[0]:
				print("%s [flags: %s]" % (g[0], g[3]))
				i = 1
		if i == 0:
			print("Sorry, no groups found matching '%s'." % pattern)

	# adds server
	def addserver(self, server):
		if not self.io.getserver(server=server) == None:
			return 0
		ans = ["y", "n", "Y", "N"]
		auth = None
		while not (auth in ans):
			auth = raw_input ("Is auth to this server required? [Y/n] ")
		if (auth == "y") or (auth == "Y"):
			auth = 0
		else:
			auth = 1
		if self.auth(server=server, sauth=auth) == 1:
			print("Server has NOT been added")
			return 1
		self.io.addserver(server, auth)
		print("Server has been added")
		return 0

	# adds group
	def addgroup(self, server, group):
		if self.addserver(server) == 1:
			print("Group has NOT been added")
			return None

		cache = raw_input ("How many articles are to be cached? (0 means none) ")
		try:
			cache = int(cache)
		except:
			print ("%s is not a number, saving 0.")
			cache = 0

		if self.auth(server=server, group=group) == 1:
			print("Group has NOT been added.")
			return 1

		self.io.addgroup(server, group, cache)
		print("Added new group")

	# sets cache for existing group
	def setcache(self, server = None, group = None, gid = None):
		if not gid == None:
			try:
				gid = int(gid)
			except:
				print ("Selected group_id (%s) is not a number!" % (gid))
				return 1
		gr = self.io.getgroup(server=server, group=group, gid=gid)
		if gr == None:
			print ("Error! Group not found!")
			return 1
		cache = raw_input ("How many articles are to be cached? (0 means none) ")
		try:
			cache = int(cache)
		except:
			print ("%s is not a number, saving 0.")
			cache = 0
		self.io.updategroup(gr[0], [ ['cache', cache] ])
		print ("Done!")

	# sets auth for existing server
	def setauth(self, server = None, group = None, gid = None):
		ser = self.io.getserver(server=server, group=group, gid=gid)
		if ser == None:
			print ("Error! Server not found!")
			return 1
		ans = ["y", "n", "Y", "N"]
		auth = None
		while not (auth in ans):
			auth = raw_input ("Is auth required? [Y/n] ")
		if (auth == "y") or (auth == "Y"):
			auth = 0
		else:
			auth = 1
		self.io.updateserver(ser[0], auth)
		print ("Done!")

	# removes group
	def removegroup(self, server, group):
		self.io.removegroup(server, group)
		print("Group has been removed")

	# gimme groups
	def listgroups(self):
		print("Your groups:")
		for g in self.groups:
			c = " " if g[4] == 0 else " [c] "
			print(" " + str(g[0]) + ":" + c + g[1] + " on server " + g[3])

	# give info about group
	def group(self, grid = None, gserver = None, ggroup = None):
		if not grid == None:
			try:
				grid = int(grid)
			except:
				print ("Error! Specified group_id (%s) is not a number." % (grid))
				return -1
			dgroup = self.io.getgroup(gid=grid)
		else:
			dgroup = self.io.getgroup(server = gserver, group = ggroup)
		# user gave us wrong id / server / group
		if dgroup == None:
			print("Error! Group not found.")
			return -1
		# yupi, group exists!
		gid, name, sid, server, cache, count, first, last = dgroup
		if cache == -1:
			if self.auth(server=server) == 1:
				return 1
			resp, count, first, last, name = self.ut.getgroup(name)
			cache = None
		print("Group %s (id=%s) on server %s has %s articles, range %s to %s" % (name, gid, server, count, first, last))
		if not cache == None and cache > 0:
			print ("Cache is enabled for last %s articles" % cache)

	# does not display article
	# 1) in case of list: printing new messages, passing in case of read
	# 2) in case of listall: printing all messaged, new ones are bolded
	def displayarticle(self, new, art_id, topic):
		r = self.io.isarticleread(art_id, self.singlegroup[0])
		if new == 0:
			if r == 0:
				return 0
			else:
				print (str(art_id) + " >> " + topic)
				return 0
		else:
			if r == 1:
				bolds = "\033[1m"
				bolde = "\033[0;0m"
				print (str(art_id) + " >> " + bolds + topic + bolde)
			else:
				print (str(art_id) + " >> " + topic)

	# dispalying last 10 or chosen articles in group
	def artlist(self, new, number = None, start = None, end = None):
		# new: 0 - only new, 1 - bold-new
		try:
			gid = self.singlegroup[0]
			if not (start == None):
				start = int(start)
				end = int(end)
			if not number == None:
				number = int(number)
		except:
			print ("Error! count or start or end is not a number.")
			return -1
		arts = self.io.getarticles(gid, start, end)
		group = self.io.getgroup(gid = gid)
		last = group[7]
		if arts == []:
			if self.singlegroup[4] > 0:
				print("Group is empty")
			else:
				if self.auth(server = group[3], group = group[1]) == 1:
					return 1
				resp, count, first, last, name = self.ut.getgroup(group[1])
				if number == None:
					resp, arts = self.ut.getarticles('subject', start, end)
				else:
					resp, arts = self.ut.getarticles('subject', int(last)-number, last)
				for aid, k in arts:
					self.displayarticle(new, aid, k)
		else:
			print("Displaying last %s cached articles for group %s on server %s" % ( number, arts[0][3], arts[0][5] ) )
			for k in arts[-number:]:
				self.displayarticle(new, k[1], k[6])

	# getting article
	def article(self, art):
		gid = self.singlegroup[0]
		try:
			art = int(art)
		except:
			print ("Error! article_id is not a number.")
			return -1
		dart = self.io.getarticle(gid, art)
		if dart == None:
			if self.auth(gid=gid) == 1:
				return 1
			dart = self.ut.getbody(str(art))
			dart = dart[3]
			tmp = ""
			for k in dart:
				tmp += ("%s\n" % k)
			dart = tmp
		else:
			dart = dart[2]
		self.io.setarticleread(art, gid)
		print dart
		return 0

	# downloading cache
	def download(self, cm):
		if len(cm) == 2:
			# download all
			if cm[1] == 'all':
				groups = self.io.getgroups()
			# download group based on group_id
			else:
				try:
					cm[1] = int(cm[1])
				except:
					print ("Error! Specified group_id (%s) is not a number." % cm[1])
					return -1
				groups = [ self.io.getgroup(gid = cm[1]) ]
		# download group based on server and group_name
		else:
			groups = [ self.io.getgroup(server = cm[1], group = cm[2]) ]
		# the fun begins
		print ("Downloading started... stay calm :-) (in case of slow downlink and big cache it may take some time)")
		for g in groups:
			gid, name, sid, server, cache, count, first, last = g
			if cache > -1:
				if self.auth(server = server) == 1:
					return 1
				resp, count, first, last, name = self.ut.getgroup(name)
				self.io.updategroup(gid, [ ["count", count], ["first", first], ["last", last] ])
			if cache > 0:
				# it's not very nice, TODO do it better :)
				# note to myself: removing all messages from cache and downloading them again
				# is not the best thing to do, TODO check messages available in cache and download
				# only new messages. should be simple to do, but it's 3am and it's 'doc' commit (;
				self.io.cleangrouparticle(gid)
				art = [ ]
				resp, arts = self.ut.getarticles('subject', str(int(last)-int(cache)+1), last)
				for aid, sub in arts:
					body = self.ut.getbody(aid)[3]
					art.append( [aid, sid, gid, sub, body ] )
				self.io.addarticles(art)
		print("Done! Thanks for being patient!")

	def genmsgid(self):
		mid = ("%s@%s" % (hashlib.sha224("%sRn%sD%s" % ( time.time(), random.randint(0, 999999999999), socket.gethostname() ) ).hexdigest(), socket.gethostname() ))
		try:
			self.ut.getarticle('<%s>' % mid)
		except nntplib.NNTPTemporaryError as e:
			print e
			if int(str(e).split(" ")[0]) == 430:
				return mid
		return self.genmsgid()

	# send article
	def sendart(self, aid = None):
		topic = None
		msubject = ""
		# if you're responding to some post
		if self.auth(gid=self.singlegroup[0]) == 1:
			return 1
		if not aid == None:
			try:
				aid = int(aid)
			except:
				print("Error! %s seems not to be a number")
				return 1
			art = self.ut.getarticles('subject', aid, aid)[1]
			if len(art) == 0:
				print("Error! Cannot find article no. %s" % aid)
				return 1
			topic = art[0][1]

		# gathering necessary info about group/server
		group = self.singlegroup[1]
		server = self.singlegroup[3]

		# is from field defined?
		mfrom = self.io.getoption('from')
		if mfrom == None:
			print("Error! Fristly set option from")
			return 1

		# subject!
		ask = "Topic: " if topic == None else ("Topic [Re: %s]: " % topic)
		while (msubject == ""):
			msubject = raw_input(ask)
			if msubject == "" and not topic == None:
				msubject = ("Re: %s" % topic)

		# geting all required options -- msg-id, date, content
		mid = self.genmsgid()
		mdate = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
		print("Text: (Ctrl+D to finish)")
		mcontent = sys.stdin.readlines()

		# checking availability of temp file
		tmp = tempfile.gettempdir()
		if tmp == None:
			tmp = "/tmp"
		k = 0
		i = 0
		while (k == 0):
			try:
				f = open( ("%s/lightnews-message%s" % (tmp, i) ), 'r')
				i += 1
			except IOError:
				k = 1
			else:
				f.close()
		fname = "%s/lightnews-message%s" % (tmp, i)

		# generating mail
		f = open(fname, 'w')
		f.write("From: %s\n" % mfrom)
		f.write("Date: %s\n" % mdate)
		f.write("Newsgroups: %s\n" % group)
		f.write("Subject: %s\n" % msubject)
		f.write("Message-ID: <%s>\n" % mid)
		f.write("Path: %s\n" % server)
		f.write("User-Agent: Lightnews\n")
		for k in mcontent:
			f.write(k)
		f.close()
		
		# auth & send
		if self.auth(gid=self.singlegroup[0]) == 1:
			print("Message has NOT been sent. It has been saved to %s" % fname)
			return 1
		self.ut.post( fname % (tmp, i) )

		# remove file
		os.remove( fname % (tmp, i) )
		# happy end

	# set from field
	def setfrom(self, wfrom):
		self.io.setoption('from', wfrom)
		print("Done!")

	# commands defining exit
	def getend(self):
		return ["q", "quit"]

	# tasks to do at the end
	def quit(self):
		if self.ut.isconnected():
			self.ut.disconnect()

	# enable/disable single-group mode
	# note to myself:
	# self.singlegroup = [group_id, group_name, server_id, server_name, cache]
	# TODO update singlegroup if there's any change done to group during s-g mode
	# or, simplier, disable changing group during single-group mode
	def setgroup(self, group):
		# you're dumb or you don't remember how to use setgroup
		if group == None and self.singlegroup == None:
			print ("Error! Use 'setgroup group_name'")
		# disabling single-group mode
		elif group == None:
			self.singlegroup = None
		# trying to enable single-group mode
		else:
			# trying if 'group' is a number
			try:
				group = int(group)
				n = 0
				for k in self.groups:
					if k[0] == group:
						self.singlegroup = [k[0], k[1], k[2], k[3], k[4]]
					if self.singlegroup == None:
						n += 1
				if self.singlegroup == None:
					print("Error! Group does not exist")
					return 1
				print("Switched to single-group mode -- group %s on server %s" % (self.groups[n][1], self.groups[n][3]))
				self.group(grid=self.singlegroup[0])
				return 0
			except:
				pass
			# oh, 'group' is not a number
			gis = []
			for k in self.groups:
				if k[1] == group:
					gis.append([k[0], k[1], k[2], k[3], k[4]])
			if len(gis) == 0:
				print("Error! Group does not exist")
				return -1
			elif len(gis) == 1:
				self.singlegroup = [gis[0][0], gis[0][1], gis[0][2], gis[0][3], gis[0][4]]
				print("Switched to single-group mode -- group %s on server %s" % (gis[0][1], gis[0][3]))
			else:
				print("Found several groups with selected name. Please chose group_id:")
				i = 0
				for l in gis:
					print(" %s - %s on server %s" % (i, l[1], l[3]))
					i += 1
				g2id = raw_input("Enter group id >> ")
				try:
					g2id = int(g2id)
				except:
					print("group id must be number!")
					return -1
				if (g2id < 0) or (g2id >= len(gis)):
					print("group is not in range")
					return -1
				self.singlegroup = [gis[g2id][0], gis[g2id][1], gis[g2id][2], gis[g2id][3], gis[g2id][4]]
				print("Switched to single-group mode -- group %s on server %s" % (gis[g2id][1], gis[g2id][3]))
			self.group(grid=self.singlegroup[0])

	# get command-line
	def getcmd(self):
		return raw_input("\n > " if self.singlegroup == None else ("\n %s > " % (self.singlegroup[1])) )

	def help(self):
		print("Lightnews")
		print("Version: 1.1 beta\n")
		print("This help does NOT contain all available options. Take a look at https://github.com/mplonski/lightnews :-)\n")
		print("Manual:")
		print(" - hello -- says hello")
		print(" - addgroup server_name group_name -- adds group")
		print(" - removegroup server_name group_name -- removes group")
		print(" - glist server_name pattern -- displays list of groups on server_name matching pattern")
		print(" - groups -- displays list of groups")
		print(" - setgroup -- enables/disables single-group mode")
		print(" - list -- displays list of unread topics in group")
		print(" - listall -- displays list of topics in group")
		print(" - article -- displays body of specified article")
		print(" - send -- send message")
		print(" - setfrom -- sets from field in sent messages")
		print(" - download -- downloads cache")
		print(" - setcache -- sets cache")
		print(" - setauth -- sets auth")
		print(" - help -- displays help")
		return 0

