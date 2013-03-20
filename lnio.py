#
# name:         lightnews' library
# description:  class for lightnews
# authors:      mplonski / maciej plonski / sokoli.pl
#               ksx4system / ksx4system.net
# licence:      GNU GPL
#

from os import system, listdir
import sqlite3

# WARNING: moved everything to sqlite!
# TODO: cache, cache, cache.
# def getc_group ( server, group )
# return group info ( [count, first, last, name, cache] )
# def getc_group_art ( server, group ) works for current group!
# return articles ( [ [id, title], ... ] )
# def getc_article ( server, group, art_id ) works for current group!
# return article (body)

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
		self.c.execute("SELECT groups.id, servers.name, groups.name, groups.cache FROM groups LEFT JOIN servers ON groups.server_id = servers.id")
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
			self.c.execute("INSERT INTO groups VALUES (NULL, %s, '%s', 0)" % (sid, group))
			self.conn.commit()
		return 0

	def removegroup(self, server, group):
		self.c.execute("SELECT groups.id FROM groups LEFT JOIN servers ON groups.server_id = servers.id WHERE groups.name='%s' AND servers.name='%s'" % (group, server))
		rg = self.c.fetchall()
		if rg == None:
			return -1
		else:
			gid = rg[0][0]
			self.c.execute("DELETE FROM groups WHERE id = %s" & gid)
			self.conn.commit()
		return 0

	
