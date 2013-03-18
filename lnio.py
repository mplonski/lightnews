#
# name:         lightnews' library
# description:  class for lightnews
# authors:      mplonski / maciej plonski / sokoli.pl
#               ksx4system / ksx4system.net
# licence:      GNU GPL
#

class lnio:
	def __init__:
		self.filename = "~/.lightnewsrc"
		self.groups = [ ]
		self.cache = None
		self.autodownload = None

	def getoptions(self):
		f = open(self.filename)
		lines = f.readlines()
		f.close()

		for line in lines:
			name = line.split("=", 1)[0]
			opt = line.split("=", 1)[1]
			if name == "cache":
				self.cache = opt
			elif name == "groups":
				groups = opt.split(";")
				for group in groups:
					self.groups.append(group)
				self.groups.sort()
			elif name == "autodownload":
				elf.autodownload = int(opt)
			else:
				# wtf?
				pass
		return True

	def setoptions(self):
		f = open(self.filename, "w")
		f.write("cache=" + self.cache)
		f.write("autodownload=" + str(self.autodownload))
		tmp = ""
		i = 0
		for group in self.groups:
			tmp += group
			if not i == 0:
				tmp += ";"
			i = 1
		f.write("groups=" + tmp)
		f.close()
		return True

	def getgroups(self):
		return self.groups

	def addgroup(self, group):
		self.groups.append(group)

	def removegroup(self, group):
		self.groups.remove(group)

	def setcache(self, cache)
		self.cache = cache

	def getcache(self):
		return self.cache

	def getcache(self, group):
		f = open(self.cache + "/" + group + ".lnset")
		line = f.readlines()[0]
		f.close()
		return line

	def writecache(self, group, cache):
		f = open(self.cache + "/" + group + ".lnset", "w")
		f.writelines(cache)
		f.close()

	def getcachearticle(self, group, art):
		f = open(self.cache + "/" + group + "/" + art + ".lnset")
		lines = f.readlines()
		f.close()
		return lines

	def writecachearticle(self, group, art, cache)
		f = open(self.cache + "/" + group + "/" + art + ".lnset")
		f.writelines(cache)
		f.close()

	def setautodownload(self, auto):
		self.autodownload = auto

	def getautodownload(self):
		return self.autodownload

	
