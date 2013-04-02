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
		# ergh, what? there's no settings' file
		self.filename = "./ln.db" if filename == None else filename
		self.conn = sqlite3.connect(self.filename)
		self.c = self.conn.cursor()

	def getoption(self, name):
		self.c.execute("SELECT * FROM options WHERE name = '%s'" % name)
		opt = self.c.fetchone()
		if opt == None:
			return None
		else:
			return opt[1]
		return 0

	def setoption(self, name, val):
		self.c.execute("SELECT * FROM options WHERE name = '%s'" % (name))
		if self.c.fetchone() == None:
			self.c.execute("INSERT INTO options VALUES ('%s', '%s')" % (name, val))
		else:
			self.c.execute("UPDATE options SET val = '%s' WHERE name = '%s'" % (val, name))
		self.conn.commit()
		return 0

	def getgroups(self):
		self.c.execute("SELECT groups.id, groups.name, servers.id, servers.name, groups.cache FROM groups LEFT JOIN servers ON groups.server_id = servers.id")
		return self.c.fetchall()

	def addserver(self, server, sauth):
		self.c.execute("INSERT INTO servers VALUES (NULL, '%s', %s)" % (server, sauth))
		self.conn.commit()

	def addgroup(self, server, group, cache):
		# checking if server exists...
		self.c.execute("SELECT * FROM servers WHERE name = '%s'" % server)
		ser = self.c.fetchone()
		sid = ser[0]

		# checking if group exists...
		self.c.execute("SELECT * FROM groups WHERE name = '%s' AND server_id = %s" % (group, sid))
		ser = self.c.fetchone()
		if ser == None:
			self.c.execute("INSERT INTO groups VALUES (NULL, %s, '%s', %s, 0, 0, 0)" % (sid, group, cache))
			self.conn.commit()
		return 0

	def updategroupcache(self, gid, cache):
		self.c.execute("UPDATE groups SET cache = %s WHERE id = %s" % (cache, gid))
		self.conn.commit()

	def updateserver(self, sid, auth):
		self.c.execute("UPDATE servers SET auth = %s WHERE id = %s" % (auth, sid))
		self.conn.commit()

	def removegroup(self, server, group):
		self.c.execute("SELECT groups.id FROM groups LEFT JOIN servers ON groups.server_id = servers.id WHERE groups.name='%s' AND servers.name='%s'" % (group, server))
		rg = self.c.fetchall()
		if rg == None:
			return -1
		else:
			gid = rg[0][0]
			self.c.execute("DELETE FROM groups WHERE id = %s" % gid)
			self.conn.commit()
			self.cleangrouparticle(gid)
		return 0

	def getserver(self, sid = None, server = None, group = None, gid = None):
		if not sid == None:
			self.c.execute("SELECT servers.id, server.name, servers.auth FROM servers WHERE id = %s" % sid)
		elif not server == None:
			self.c.execute("SELECT servers.id, servers.name, servers.auth FROM servers WHERE name = '%s'" % (server))
		else:
			self.c.execute("SELECT servers.id, servers.name, servers.auth FROM servers LEFT JOIN groups ON groups.server_id = servers.id WHERE groups.id = %s" % gid)
		ser = self.c.fetchone()
		if ser == None:
			return None
		else:
			return ser

	def getgroup(self, server = None, group = None, gid = None):
		if not gid == None:
			self.c.execute("SELECT groups.id, groups.name, servers.id, servers.name, groups.cache, groups.count, groups.first, groups.last FROM groups LEFT JOIN servers ON groups.server_id = servers.id WHERE groups.id='%s'" % gid)
		else:
			self.c.execute("SELECT groups.id, groups.name, servers.id, servers.name, groups.cache, groups.count, groups.first, groups.last FROM groups LEFT JOIN servers ON groups.server_id = servers.id WHERE groups.name='%s' AND servers.name='%s'" % (group, server))
		group = self.c.fetchone()
		if group == None:
			return None
		else:
			return group

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

	def cleangrouparticle(self, gid):
		self.c.execute("DELETE FROM articles WHERE group_id = %s" %gid)
		self.conn.commit()

	def isarticleread(self, art_id, group_id):
		self.c.execute("SELECT * FROM read_art WHERE id = %s and group_id = %s" % (art_id, group_id))
		if self.c.fetchone() == None:
			return 1
		else:
			return 0

	def setarticleread(self, art_id, group_id):
		self.c.execute("INSERT INTO read_art VALUES (%s, %s)" % (art_id, group_id))
		self.conn.commit()

	def addarticles(self, data):
		# data = [ [art_id, srv_id, group_id, title, body], [ ... ] ... ]
		if len(data) == 1:
			st = ""
			for l in a[4]:
				st += (l + "\n")
			self.c.execute("INSERT INTO articles VALUES (NULL, %s, %s, %s, %s, %s)" % ( data[0][0], data[0][1]. data[0][2], adapt(data[0][3]), adapt(st) ) )
			self.conn.commit()
		else:
			for a in data:
				st = ""
				for l in a[4]:
					st += (l + "\n")
				self.c.execute("INSERT INTO articles VALUES (NULL, %s, %s, %s, %s, %s)" % ( a[0], a[1], a[2], adapt(a[3]), adapt(st) ) )
				self.conn.commit()

	def getarticles(self, gid, start = None, end = None):
		query = "SELECT articles.id, articles.art_id, servers.id, groups.name, servers.id, servers.name, articles.title, articles.body FROM articles INNER JOIN servers ON servers.id = articles.server_id INNER JOIN groups ON groups.id = articles.group_id WHERE articles.group_id = %s" % gid
		if not ( (start == None) or (end == None) ):
			query += ( " AND articles.art_id > %s AND articles.art_id < %s" % (start-1, end+1) )
		self.c.execute(query)
		return self.c.fetchall()

	def getarticle(self, gid, aid):
		self.c.execute("SELECT id, title, body FROM articles WHERE art_id = %s AND group_id = %s" % (aid, gid))
		return self.c.fetchone()

