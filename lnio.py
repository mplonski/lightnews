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
		self.c.execute("UPDATE options SET val = '%s' WHERE name = '%s'" % (val, name))
		self.conn.commit()
		return 0

	def getgroups(self):
		self.c.execute("SELECT groups.id, groups.name, servers.id, servers.name, groups.cache FROM groups LEFT JOIN servers ON groups.server_id = servers.id")
		return self.c.fetchall()

	def addgroup(self, server, group):
		# checking if server exists...
		self.c.execute("SELECT * FROM servers WHERE name = '%s'" % server)
		ser = self.c.fetchone()
		if ser == None:
			self.c.execute("INSERT INTO servers VALUES (NULL, '%s', NULL, NULL)" % server)
			self.conn.commit()
			self.c.execute("SELECT * FROM servers WHERE name = '%s'" % server)
			ser = self.c.fetchone()
		sid = ser[0]

		# checking if group exists...
		self.c.execute("SELECT * FROM groups WHERE name = '%s' AND server_id = %s" % (group, sid))
		ser = self.c.fetchone()
		if ser == None:
			self.c.execute("INSERT INTO groups VALUES (NULL, %s, '%s', 0, 0, 0, 0)" % (sid, group))
			self.conn.commit()
		return 0

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

	def addarticles(self, data):
		# data = [ [art_id, srv_id, group_id, title, body], [ ... ] ... ]
		if len(data) == 1:
			st = ""
			for l in a[4]:
				st += (l + "\n")
			self.c.execute("INSERT INTO articles VALUES (NULL, %s, %s, %s, %s, %s, 0)" % ( data[0][0], data[0][1]. data[0][2], adapt(data[0][3]), adapt(st) ) )
			self.conn.commit()
		else:
			for a in data:
				st = ""
				for l in a[4]:
					st += (l + "\n")
				self.c.execute("INSERT INTO articles VALUES (NULL, %s, %s, %s, %s, %s, 0)" % ( a[0], a[1], a[2], adapt(a[3]), adapt(st) ) )
				self.conn.commit()

	def getarticles(self, gid, start = None, end = None, is_read = None):
		query = "SELECT articles.id, articles.art_id, servers.id, groups.name, servers.id, servers.name, articles.title, articles.body, articles.is_read FROM articles INNER JOIN servers ON servers.id = articles.server_id INNER JOIN groups ON groups.id = articles.group_id WHERE articles.group_id = %s" % gid
		if not ( (start == None) or (end == None) ):
			query += ( " AND articles.art_id > %s AND articles.art_id < %s" % (start-1, end+1) )
		if not ( is_read == None):
			query += ( " AND articles.is_read = %s" % is_read )
		self.c.execute(query)
		return self.c.fetchall()

