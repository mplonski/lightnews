#
# name:         lightnews' library
# description:  class for lightnews responsible for command line
# authors:      mplonski / maciej plonski / sokoli.pl
#               ksx4system / ksx4system.net
# licence:      GNU GPL
#

from psycopg2.extensions import adapt
import getpass

class lncmd:
	def __init__(self, ut, io):
		self.ut = ut
		self.io = io
		self.singlegroup = None

	def analcmd(self, cmd):
		return cmd.split(" ")

	def docmd(self, cmd):
		self.groups = self.io.getgroups()

		cm = self.analcmd(cmd)

		if cm[0] == "hello":
			self.hello()

		elif cm[0] == "addgroup" and len(cm) == 3:
			self.addgroup(cm[1], cm[2])
		elif cm[0] == "addgroup":
			print ("Error! Use 'addgroup server group'")

		elif cm[0] == "removegroup" and len(cm) == 3 and self.singlegroup == None:
			self.removegroup(cm[1], cm[2])
		elif cm[0] == "removegroup" and len(cm) == 3 and not self.singlegroup == None:
			print ("Error! 'removegroup' is available only in default mode")
		elif cm[0] == "removegroup":
			print ("Error! Use 'removegroup server group")

		elif cm[0] == "groups":
			self.listgroups()

		elif cm[0] == "setauth" and len(cm) == 2:
			self.setauth(server=cm[1])
		elif cm[0] == "setauth":
			print ("Error! Use 'setauth server_name'")

		elif cm[0] == "setcache" and len(cm) == 1 and not self.singlegroup == None:
			self.setcache(gid=self.singlegroup[0])
		elif cm[0] == "setcache" and len(cm) == 2:
			self.setcache(gid=cm[1])
		elif cm[0] == "setcache" and len(cm) == 3:
			self.setcache(server=cm[1], group=cm[2])
		elif cm[0] == "setcache":
			print ("Error! Use 'setcache' in single-group mode or 'setcache group_id'")

		elif cm[0] == "group" and len(cm) == 3:
			self.group(gserver=cm[1], ggroup=cm[2])
		elif cm[0] == "group" and len(cm) == 2:
			self.group(grid=cm[1])
		elif cm[0] == "group" and len(cm) == 1 and not self.singlegroup == None:
			self.group(grid=self.singlegroup[0])
		elif cm[0] == "group":
			print ("Error! Use 'group group_id' or 'group server_name group_name'")

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

		elif cm[0] == "article" and len(cm) == 2 and not self.singlegroup == None:
			self.article(cm[1])
		elif cm[0] == "article" and not self.singlegroup == None:
			print("Error! Use 'article art_id'")
		elif cm[0] == "article":
			print("Error! Command 'article' is available only in single-group mode.")

		elif cm[0] == "send" and len(cm) == 2 and not self.singlegroup == None:
			self.sendart(cm[1])
		elif cm[0] == "send" and not self.singlegroup == None:
			self.sendart(None)
		elif cm[0] == "send":
			print("Error! Usage 'send' or 'send art_id'. Available only in group mode.")

		elif cm[0] == "download" and ( (len(cm) == 2) or (len(cm) == 3) ):
			self.download(cm)
		elif cm[0] == "download" and not self.singlegroup == None:
			self.download(["download", str(self.singlegroup[0])])
		elif cm[0] == "download":
			print ("Error! Use 'download' in single-group mode or 'download all' or 'download group_id' or 'download server group'")

		elif cm[0] == "setgroup" and len(cm) == 2:
			self.setgroup(cm[1])
		elif cm[0] == "setgroup":
			self.setgroup(None)

		elif cm[0] == "help":
			print("Will be one day... take a look at https://github.com/mplonski/lightnews")
				
	def hello(self):
		print("Hello! :-)")

	def askforauth(self, tmp):
		if not int(tmp) == 0:
			return [None, None]
		print("Authorisation to this server is required!")
		username = raw_input("Username [%s]: " % (getpass.getuser()))
		if username == "":
			username = getpass.getuser()
		password = getpass.getpass()
		return [username, password]

	def auth(self, server = None, sid = None, group = None, gid = None):
		if (server == None) and (sid == None) and (not gid == None):
			sid, server, sauth = self.io.getserver(gid=gid)
		elif not ((server == None) and (sid == None)):
			sid, server, sauth = self.io.getserver(sid=sid, server=server)

		if not ((group == None) and (gid == None)):
			gr = self.io.getgroup(server=server, group=group, gid=gid)
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
				self.ut.connect(self.ut.getservername(), suser, spass)
				return 0
			else: # it's up, don't worry, be happy
				return 0
		# connecting to specified server
		else:
			tmp = self.ut.isconnected()
			# not connected or connected to other server
			if (not tmp) or (tmp and not self.ut.getservername() == server):
				suser, spass = self.askforauth(sauth)
				self.ut.connect(server, suser, spass)
			# if group is set and (not connected or connected to other group)
			if (not group == None) and ((not tmp) or (tmo and not self.ut.getgroupname() == group)):
				self.ut.getgroup(group)
		return 0

	def addserver(self, server):
		if not self.io.getserver(server=server) == None:
			return 1
		ans = ["y", "n", "Y", "N"]
		auth = None
		while not (auth in ans):
			auth = raw_input ("Is auth to this server required? [Y/n] ")
		if (auth == "y") or (auth == "Y"):
			auth = 0
		else:
			auth = 1
		self.io.addserver(server, auth)

	def addgroup(self, server, group):
		if self.io.getserver(server=server) == None:
			self.addserver(server)

		cache = raw_input ("How many articles are to be cached? (0 means none) ")
		try:
			cache = int(cache)
		except:
			print ("%s is not a number, saving 0.")
			cache = 0
		self.io.addgroup(server, group, cache)
		print("Added new group")

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
		self.io.updategroupcache(gr[0], cache)
		print ("Done!")

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

	def removegroup(self, server, group):
		self.io.removegroup(server, group)
		print("Group has been removed")

	def listgroups(self):
		print("Your groups:")
		for g in self.groups:
			c = " " if g[4] == 0 else " [c] "
			print(" " + str(g[0]) + ":" + c + g[1] + " on server " + g[3])

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
			self.auth(server=server)
			resp, count, first, last, name = self.ut.getgroup(name)
			cache = None
		print("Group %s (id=%s) on server %s has %s articles, range %s to %s" % (name, gid, server, count, first, last))
		if not cache == None and cache > 0:
			print ("Cache is enabled for last %s articles" % cache)

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
				self.auth(server = group[3], group = group[1])
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
			self.auth(gid=gid)
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

	def download(self, cm):
		if len(cm) == 2:
			if cm[1] == 'all':
				# download all
				groups = self.io.getgroups()
			else:
				try:
					cm[1] = int(cm[1])
				except:
					print ("Error! Specified group_id (%s) is not a number." % cm[1])
					return -1
				groups = [ self.io.getgroup(gid = cm[1]) ]
		else:
			groups = [ self.io.getgroup(server = cm[1], group = cm[2]) ]
		print ("Downloading started... stay calm :-) (in case of slow downlink and big cache it may take some time)")
		for g in groups:
			gid, name, sid, server, cache, count, first, last = g
			if cache > -1:
				self.auth(server = server)
				resp, count, first, last, name = self.ut.getgroup(name)
				self.io.updategroup(gid, [ ["count", count], ["first", first], ["last", last] ])
			if cache > 0:
				# it's not very nice, TODO do it better :)
				self.io.cleangrouparticle(gid)
				art = [ ]
				resp, arts = self.ut.getarticles('subject', str(int(last)-int(cache)+1), last)
				for aid, sub in arts:
					body = self.ut.getbody(aid)[3]
					art.append( [aid, sid, gid, sub, body ] )
				self.io.addarticles(art)
		print("Done! Thanks for being patient!")

	def sendart(self, aid = None):
		return(":)")

	def getend(self):
		return ["q", "quit"]

	def setgroup(self, group):
		if group == None and self.singlegroup == None:
			print ("Error! Use 'setgroup group_name'")
		elif group == None:
			self.singlegroup = None
		else:
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

	def getcmd(self):
		return raw_input("\n > " if self.singlegroup == None else ("\n %s > " % (self.singlegroup[1])) )

