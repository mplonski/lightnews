#
# name:         lightnews' library
# description:  class for lightnews responsible for cache / IO
# authors:      mplonski / maciej plonski / sokoli.pl
#               ksx4system / ksx4system.net
# licence:      GNU GPL
#

import sqlite3
from psycopg2.extensions import adapt

class lnio:
	def __init__(self, filename = None):
		# settings' file name
		# ergh, what? there's no settings' file, I need to think about
		# other locations of ln.db -- user's dir seems to be the best choise
		# and it's set in main.py, but let's think about other location
		# in this file
		self.filename = "./ln.db" if filename == None else filename
		self.conn = sqlite3.connect(self.filename)
		self.c = self.conn.cursor()

	# cleans id's in table
	def cleantable(self, name):
		self.c.execute("SELECT * FROM %s ORDER BY id" % name)
		data = self.c.fetchall()
		wid = 0
		for k in data:
			if not int(k[0]) == wid:
				self.c.execute("UPDATE %s SET id = %s WHERE id = %s" % (name, wid, k[0]))
				self.conn.commit()
				return [k[0], wid]
			wid += 1
		return None

	# cleans table 'servers'
	def cleantableservers(self):
		tr = self.cleantable('servers')
		while not (tr == None):
			self.c.execute("UPDATE groups SET server_id = %s WHERE server_id = %s" % (tr[1], tr[0]))
			self.c.execute("UPDATE articles SET server_id = %s WHERE server_id = %s" % (tr[1], tr[0]))
			self.conn.commit()
			tr = self.cleantable('servers')

	# cleans table 'groups'
	def cleantablegroups(self):
		tr = self.cleantable('groups')
		while not (tr == None):
			self.c.execute("DELETE FROM articles WHERE group_id = %s" % tr[1])
			self.c.execute("DELETE FROM read_art WHERE group_id = %s" % tr[1])
			self.conn.commit()
			self.c.execute("UPDATE articles SET group_id = %s WHERE group_id = %s" % (tr[1], tr[0]))
			self.c.execute("UPDATE read_art SET group_id = %s WHERE group_id = %s" % (tr[1], tr[0]))
			self.conn.commit()
			tr = self.cleantable('groups')

	# cleans database :)
	# do NOT run in single-mode group
	def cleandb(self):
		tr = self.cleantableservers()

		# getting tables 'servers' and 'groups' and removing non-used servers
		self.c.execute("SELECT * FROM servers ORDER BY id")
		ser = self.c.fetchall()
		self.c.execute("SELECT * FROM groups ORDER BY id")
		gr = self.c.fetchall()
		l = []
		for k in ser:
			l.append(0)
		for k in gr:
			l[int(k[1])] += 1
		for i in range(len(l)):
			if l[i] == 0:
				self.c.execute("DELETE FROM servers WHERE id = %s" % i)
				self.conn.commit()
		tr = self.cleantableservers()

		# cheching groups...
		self.cleantablegroups()

		# ergh, done? :-)
		return 0

	# get option
	def getoption(self, name):
		self.c.execute("SELECT * FROM options WHERE name = '%s'" % name)
		opt = self.c.fetchone()
		# only God knows why...
		if opt == None:
			return None
		else:
			return opt[1]

	# update or create option
	def setoption(self, name, val):
		self.c.execute("SELECT * FROM options WHERE name = '%s'" % (name))
		# doesn't exist
		if self.c.fetchone() == None:
			self.c.execute("INSERT INTO options VALUES ('%s', '%s')" % (name, val))
		# exists
		else:
			self.c.execute("UPDATE options SET val = '%s' WHERE name = '%s'" % (val, name))
		self.conn.commit()
		return 0

	# get list of groups
	def getgroups(self):
		self.c.execute("SELECT groups.id, groups.name, servers.id, servers.name, groups.cache FROM groups LEFT JOIN servers ON groups.server_id = servers.id")
		return self.c.fetchall()

	# add server
	def addserver(self, server, sauth):
		self.c.execute("INSERT INTO servers VALUES (NULL, '%s', %s)" % (server, sauth))
		self.conn.commit()
		self.cleandb()

	# add group
	def addgroup(self, server, group, cache):
		# checking if server exists...
		self.c.execute("SELECT * FROM servers WHERE name = '%s'" % server)
		ser = self.c.fetchone()
		sid = ser[0]

		# checking if group exists...
		self.c.execute("SELECT * FROM groups WHERE name = '%s' AND server_id = %s" % (group, sid))
		ser = self.c.fetchone()
		# nope, it doesn't
		if ser == None:
			self.c.execute("INSERT INTO groups VALUES (NULL, %s, '%s', %s, 0, 0, 0)" % (sid, group, cache))
			self.conn.commit()
			self.cleandb()
			return 0
		# whoops, it does
		return 1

	# update auth option
	def updateserver(self, sid, auth):
		self.c.execute("UPDATE servers SET auth = %s WHERE id = %s" % (auth, sid))
		self.conn.commit()

	# removes group
	def removegroup(self, server, group):
		self.c.execute("SELECT groups.id FROM groups LEFT JOIN servers ON groups.server_id = servers.id WHERE groups.name='%s' AND servers.name='%s'" % (group, server))
		rg = self.c.fetchall()
		# sorry, doesn't exist
		if rg == None:
			return -1
		# delete it!
		else:
			gid = rg[0][0]
			self.c.execute("DELETE FROM groups WHERE id = %s" % gid)
			self.c.execute("DELETE FROM articles WHERE group_id = %s" % gid)
			self.c.execute("DELETE FROM read_art WHERE group_id = %s" % gid)
			self.conn.commit()
			self.cleangrouparticle(gid)
			self.cleandb()
			return 0

	# gimme server
	def getserver(self, sid = None, server = None, group = None, gid = None):
		# yupi, got server_id
		if not sid == None:
			self.c.execute("SELECT servers.id, server.name, servers.auth FROM servers WHERE id = %s" % sid)
		# what about server_name?
		elif not server == None:
			self.c.execute("SELECT servers.id, servers.name, servers.auth FROM servers WHERE name = '%s'" % (server))
		# oh, we have group_id!
		else:
			self.c.execute("SELECT servers.id, servers.name, servers.auth FROM servers LEFT JOIN groups ON groups.server_id = servers.id WHERE groups.id = %s" % gid)
		ser = self.c.fetchone()
		# I have no idea what I'm doing
		if ser == None:
			return None
		else:
			return ser

	# get group
	def getgroup(self, server = None, group = None, gid = None):
		# yupu, got group_id
		if not gid == None:
			self.c.execute("SELECT groups.id, groups.name, servers.id, servers.name, groups.cache, groups.count, groups.first, groups.last FROM groups LEFT JOIN servers ON groups.server_id = servers.id WHERE groups.id='%s'" % gid)
		# oh, got server_name and group_name
		else:
			self.c.execute("SELECT groups.id, groups.name, servers.id, servers.name, groups.cache, groups.count, groups.first, groups.last FROM groups LEFT JOIN servers ON groups.server_id = servers.id WHERE groups.name='%s' AND servers.name='%s'" % (group, server))
		group = self.c.fetchone()
		# God... why?
		if group == None:
			return None
		else:
			return group

	# update group
	def updategroup(self, gid, chg):
		gstr = "UPDATE groups SET "
		i = 0
		for k in chg:
			gstr += ", " if i == 1 else " "
			gstr += ("%s = '%s'" % (k[0], k[1]) )
			i = 1
		gstr += (" WHERE id = %s" % gid)
		self.c.execute(gstr)
		self.conn.commit()

	# remove cache for group
	def cleangrouparticle(self, gid):
		self.c.execute("DELETE FROM articles WHERE group_id = %s" %gid)
		self.conn.commit()

	# chech if user has read this article
	def isarticleread(self, art_id, group_id):
		self.c.execute("SELECT * FROM read_art WHERE id = %s and group_id = %s" % (art_id, group_id))
		return (1 if self.c.fetchone() == None else 0)

	# he's just read it
	def setarticleread(self, art_id, group_id):
		self.c.execute("INSERT INTO read_art VALUES (%s, %s)" % (art_id, group_id))
		self.conn.commit()

	# add article to cache
	def addarticles(self, data):
		# data = [ [art_id, srv_id, group_id, title, body], [ ... ] ... ]
		for a in data:
			st = ""
			for l in a[4]:
				st += (l + "\n")
			self.c.execute("INSERT INTO articles VALUES (NULL, %s, %s, %s, %s, %s)" % ( a[0], a[1], a[2], adapt(a[3]), adapt(st) ) )
			self.conn.commit()

	# get articles from cache
	def getarticles(self, gid, start = None, end = None):
		query = "SELECT articles.id, articles.art_id, servers.id, groups.name, servers.id, servers.name, articles.title, articles.body FROM articles INNER JOIN servers ON servers.id = articles.server_id INNER JOIN groups ON groups.id = articles.group_id WHERE articles.group_id = %s" % gid
		if not ( (start == None) or (end == None) ):
			query += ( " AND articles.art_id > %s AND articles.art_id < %s" % (start-1, end+1) )
		self.c.execute(query)
		return self.c.fetchall()

	# get article from cache
	def getarticle(self, gid, aid):
		self.c.execute("SELECT id, title, body FROM articles WHERE art_id = %s AND group_id = %s" % (aid, gid))
		return self.c.fetchone()

