#
# name:         lightnews' library
# description:  class for lightnews
# authors:      mplonski / maciej plonski / sokoli.pl
#               ksx4system / ksx4system.net
# licence:      GNU GPL
#

from os import system, listdir

class lnio:
	def __init__(self):
		# settings' file name
		self.filename = "~/.lightnewsrc"

		# list of groups
		self.groups = [ ]

		# -1 -> no cache, 0 -> only groups, 1...n -> groups + 1...n number of topics
		self.cache = None

		# directory with cache
		self.cachedir = "~/.lightnewscache/"

		# 0 -> autodownload on, 1 -> autodownload off
		self.autodownload = None

	def setfilename(self, fdir):
		self.filename = fdir
	
	def getfilename(self):
		return self.filename

	def getoptions(self):
		try:
			f = open(self.filename)
			lines = f.readlines()

			for line in lines:
				name = line.split("=", 1)[0]
				opt = line.split("=", 1)[1]
				if name == "cache":
					self.cache = opt
				elif name == "cachedir":
					self.cachedir = opt
				elif name == "groups":
					groups = opt.split(";")
					for group in groups:
						tmp = group.split(":")
						self.groups.append( [ tmp[0], tmp[1] ] )
					self.groups.sort()
				elif name == "autodownload":
					elf.autodownload = int(opt)
				else:
					# wtf?
					pass
		except IOError:
			return None
		else:
			f.close()
			return 0

	def setoptions(self):
		try:
			f = open(self.filename, "w")
			f.write("cache=" + self.cache)
			f.write("cachedir=" + self.cachedir)
			f.write("autodownload=" + str(self.autodownload))
			tmp = ""
			i = 0
			for group in self.groups:
				tmp += group
				if not i == 0:
					tmp += ";"
				i = 1
			f.write("groups=" + tmp)
		except IOError:
			return None
		else:
			f.close()
			return 0

	def getgroups(self):
		return self.groups

	def addgroup(self, server, group):
		self.groups.append([group, server])
		self.groups.sort()

	def removegroup(self, group):
		self.groups.remove(group)

	def setcache(self, cache):
		self.cache = cache

	def getcache(self):
		return self.cache

	def setcachedir(self, cdir):
		self.cachedir = cdir

	def getcachedir(self):
		return self.cachedir

	def isgroupcache(self, group):
		try:
			f = open(self.cachedir + "/" + group + ".lnset")
		except IOError:
			return -1
		else:
			f.close()
			return 0

	def getcache(self, group):
		try:
			f = open(self.cachedir + "/" + group + ".lnset")
			lines = f.readlines()
			count = -1
			first = -1
			last = -1
			name = None
			for line in lines:
				zname, opt = line.split("=")
				if zname == "count":
					count = int(opt)
				elif zname == "first":
					first = int(opt)
				elif zname == "last":
					last = int(opt)
				elif zname == "name":
					name = opt
				elif zname == "iscache":
					iscache = int(opt)
				if (count > 0) and (first > 0) and (last > 0) and (not name == None):
					return [count, first, last, name, iscache]
		except IOError:
			return None
		else:
			return line
			f.close()

	def movecache(self, newdir):
		# TODO do it nicer :-)
		system("mv " + self.cachedir + " " + newdir)
		self.setcachedir(newdir)

	def writecache(self, group, cache):
		try:
			f = open(self.cache + "/" + group + ".lnset", "w")
			for opt in cache:
				f.write(opt[0] + "=" + opt[1])
		except IOError:
			return None
		else:
			f.close()
			return 0

	def getcachearticles(self, group):
		try:
			files = listdir(self.cache + "/" + group + "/")
		except IOError:
			return None
		else:
			return files

	def getcachearticle(self, group, art):
		try:
			f = open(self.cache + "/" + group + "/" + art)
			lines = f.readlines()
		except IOError:
			return None
		else:
			f.close()
			return lines

	def writecachearticle(self, group, art, cache):
		try:
			f = open(self.cache + "/" + group + "/" + art)
			f.writelines(cache)
		except IOError:
			return None
		else:
			f.close()
			return 0

	def setautodownload(self, auto):
		self.autodownload = auto

	def getautodownload(self):
		return self.autodownload

	
