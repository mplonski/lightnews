#
# name:         lightnews' library
# description:  class for lightnews
# authors:      mplonski / maciej plonski / sokoli.pl
#               ksx4system / ksx4system.net
# licence:      GNU GPL
#

from psycopg2.extensions import adapt

class lncmd:
	def __init__(self, ut, io):
		self.ut = ut
		self.io = io

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

		elif cm[0] == "removegroup" and len(cm) == 3:
			self.removegroup(cm[1], cm[2])
		elif cm[0] == "removegroup":
			print ("Error! Use 'removegroup server group")

		elif cm[0] == "groups":
			self.listgroups()

		elif cm[0] == "group" and len(cm) == 3:
			self.group(gserver=cm[1], ggroup=cm[2])
		elif cm[0] == "group" and len(cm) == 2:
			self.group(grid=cm[1])
		elif cm[0] == "group":
			print ("Error! Use 'group group_id' or 'group server_name group_name'")

		elif cm[0] == "list" and (len(cm) == 4):
			self.artlist(cm[1], cm[2], cm[3])
		elif cm[0] == "list" and (len(cm) == 2):
			self.artlist(cm[1], None, None)
		elif cm[0] == "list":
			print ("Error! Use 'list group_id' or 'list group_id start end'")

		elif cm[0] == "article" and len(cm) == 2:
			self.article(cm[1])
		elif cm[0] == "article":
			print("Error! Use 'article art_id'")

		elif cm[0] == "download" and ( (len(cm) == 2) or (len(cm) == 3) ):
			self.download(cm)
		elif cm[0] == "download":
			print ("Error! Use 'download all' or 'download group_id' or 'download server group'")

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
	def artlist(self, gid, start = None, end = None): 
		arts = self.io.getarticles(gid, start, end)
		if arts == None:
			# TODO internet...
			pass
		else:
			print("Displaying all cached articles (%s) for group %s on server %s" % ( len(arts), arts[0][3], arts[0][5] ) )
			for k in arts:
				print("%s >> %s" % (k[1], k[6]))

	# getting article
	def article(self, art):
		return 0

	def download(self, cm):
		if len(cm) == 2:
			if cm[1] == 'all':
				# download all
				groups = self.io.getgroups()
			else:
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

	def getcmd(self):
		return raw_input(" > ")

