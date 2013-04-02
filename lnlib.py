#
# name:         lightnews' library
# description:  class for lightnews
# authors:      mplonski / maciej plonski / sokoli.pl
#               ksx4system / ksx4system.net
# licence:      GNU GPL
#

import nntplib

# need help? http://docs.python.org/2/library/nntplib.html :)

class UsenetGroup:
	def __init__(self):
		self.ins = None
		self.group = None
		self.server = None

	def connect ( self, url, user = None, password = None ):
		if self.isconnected():
			self.disconnect()
		if user == None:
			self.ins = nntplib.NNTP( url )
		else:
			self.ins = nntplib.NNTP( url, user, password )
		self.server = url

	def isconnected (self):
		return False if self.ins == None else True

	def disconnect (self):
		self.ins.quit()
		self.ins = None
		self.server = None
		self.group = None

	def getwelcome (self):
		if self.isconnected == False:
			return None
		return self.ins.getwelcome()

	def getnewgroups (self, date, time):
		if self.isconnected == False:
			return None
		response, groups = self.ins.newgroups(date, time)
		return [response, groups]

	def getnewnews (self, group, date, time):
		# usually disabled, TODO with exceptions
		if self.isconnected == False:
			return None
		response, articles = self.ins.newnews(group, date, time)
		return [response, articles]

	def getlist (self):
		if self.isconnected == False:
			return None
		response, nlist = self.ins.list()
		return [response, nlist]

	def getdescription (self, group):
		if not self.isconnected:
			return None
		return self.ins.description(group)

	def getgroupname (self):
		return self.group

	def getservername (self):
		return self.server

	def getgroup (self, name):
		if not self.isconnected:
			return None
		response, count, first, last, name = self.ins.group(name)
		self.group = name
		return [response, count, first, last, name]

	def setservergroup (self, server, group ):
		self.server = server
		self.group = group

	def getstat (self, nid):
		if not self.isconnected:
			return None
		reponse, number, n2id = self.ins.stat(nid)
		return [response, number, n2id]

	def getnext (self):
		if not self.isconnected:
			return None
		response, number, n2id = self.ins.next()
		return [response, number, n2id]

	def getlast (self):
		if not self.isconnected:
			return None
		response, number, n2id = self.ins.last()
		return [response, number, n2id]

	def gethead (self, nid):
		if not self.isconnected:
			return None
		response, number, n2id, nlist = self.ins.head(nid)
		return [response, number, n2id, nlist]

	def getbody (self, nid):
		if not self.isconnected:
			return None
		response, number, n2id, nlist = self.ins.body(nid)
		return [response, number, n2id, nlist]

	def getarticle (self, nid):
		if not self.isconnected:
			return None
		response, number, n2id, nlist = self.ins.article(nid)
		return [response, number, n2id, nlist]

	def getarticles (self, header, first, last):
		if not self.isconnected:
			return None
		response, nlist = self.ins.xhdr(header, "%s-%s" % (first, last))
		return [response, nlist]

	def post (self, filename):
		if not self.isconnected:
			return None
		self.ins.post(filename)
		return None

	def getdate(self):
		if not self.isconnected:
			return None
		response, date, time = self.ins.date()
		return [response, date, time]

	def xgetover (self, start, end):
		if not self.isconnected:
			return None
		response, nlist = self.ins.xover(start, end)
		return [response, nlist]

	def xgetpath (self, nid):
		if not self.isconnected:
			return None
		response, path = self.ins.xpath(nid)
		return [response, path]

	def behappy (self):
		return ":)"


