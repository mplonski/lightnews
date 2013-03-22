#
# name:         lightnews' library
# description:  class for lightnews responsible for command line
# authors:      mplonski / maciej plonski / sokoli.pl
#               ksx4system / ksx4system.net
# licence:      GNU GPL
#

from psycopg2.extensions import adapt

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

		elif cm[0] == "group" and len(cm) == 3:
			self.group(gserver=cm[1], ggroup=cm[2])
		elif cm[0] == "group" and len(cm) == 2:
			self.group(grid=cm[1])
		elif cm[0] == "group" and len(cm) == 1 and not self.singlegroup == None:
			self.group(grid=self.singlegroup[0])
		elif cm[0] == "group":
			print ("Error! Use 'group group_id' or 'group server_name group_name'")

		elif cm[0] == "list" and (len(cm) == 3) and not self.singlegroup == None:
			self.artlist(None, cm[1], cm[2])
		elif cm[0] == "list" and (len(cm) == 2) and not self.singlegroup == None:
			self.artlist(cm[1], None, None)
		elif cm[0] == "list" and not self.singlegroup == None:
			self.artlist(10, None, None)
		elif cm[0] == "list" and not self.singlegroup == None:
			print("Error! Use 'list' or 'list number' or 'list start end'")
		elif cm[0] == "list":
			print ("Error! Command 'list' is available only in single-group mode.")

		elif cm[0] == "article" and len(cm) == 2 and not self.singlegroup == None:
			self.article(cm[1])
		elif cm[0] == "article" and not self.singlegroup == None:
			print("Error! Use 'article art_id'")
		elif cm[0] == "article":
			print("Error! Command 'article' is available only in single-group mode.")

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
			print("Will be one day...")
				
	def hello(self):
		print("Hello! :-)")

	def addgroup(self, server, group):
		self.io.addgroup(server, group)
		print("Added new group")

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
			if not self.ut.getservername() == server:
				self.ut.connect(server)
			resp, count, first, last, name = self.ut.getgroup(name)
		print("Group %s (id=%s) on server %s has %s articles, range %s to %s" % (name, gid, server, count, first, last))

	# dispalying last 10 or chosen articles in group
	def artlist(self, number = None, start = None, end = None):
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
				if not self.ut.getservername() == group[3]:
					self.ut.connect(group[3])
				if not self.ut.getgroupname() == group[1]:
					resp, count, first, last, name = self.ut.getgroup(group[1])
				if number == None:
					resp, arts = self.ut.getarticles('subject', start, end)
				else:
					resp, arts = self.ut.getarticles('subject', int(last)-number, last)
				for aid, k in arts:
					print("%s >> %s" % (aid, k))
		else:
			print("Displaying last %s cached articles for group %s on server %s" % ( number, arts[0][3], arts[0][5] ) )
			for k in arts[-number:]:
				print("%s >> %s" % (k[1], k[6]))

	# getting article
	def article(self, art):
		gid = self.singlegroup[0]
		try:
			art = int(art)
		except:
			print ("Error! article_id is not a number.")
			return -1
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
				if not self.ut.getservername() == server:
					self.ut.connect(server)
				resp, count, first, last, name = self.ut.getgroup(name)
				self.io.updategroup(gid, [ ["count", count], ["first", first], ["last", last] ])
			if cache > 0:
				self.io.cleangrouparticle(gid)
				art = [ ]
				resp, arts = self.ut.getarticles('subject', str(int(last)-int(cache)+1), last)
				for aid, sub in arts:
					body = self.ut.getbody(aid)[3]
					art.append( [aid, sid, gid, sub, body ] )
				self.io.addarticles(art)
		print("Done! Thanks for being patient!")

	def getend(self):
		return ["q", "quit"]

	def setgroup(self, group):
		if group == None:
			self.singlegroup = None
		else:
			gis = []
			for k in self.groups:
				if k[1] == group:
					gis.append([k[0], k[1], k[2], k[3], k[4]])
			if len(gis) == 0:
				print("Error! Group does not exist")
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

	def getcmd(self):
		return raw_input(" > " if self.singlegroup == None else (" %s > " % (self.singlegroup[1])) )

