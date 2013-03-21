#
# name:         lightnews' library
# description:  class for lightnews
# authors:      mplonski / maciej plonski / sokoli.pl
#               ksx4system / ksx4system.net
# licence:      GNU GPL
#

# TODO: changed cache based on files to sqlite
# everything requires to reconsider and rewrite
# doing it right now, commiting just to backup :-)

class lncmd:
	def __init__(self, ut, io):
		self.ut = ut
		self.io = io

	def analcmd(self, cmd):
		return cmd.split(" ")

	def docmd(self, cmd):
		self.groups = self.io.getgroups()

		cm = self.analcmd(cmd)

		# ONLY FOR DEBUG
		print cm

		if cm[0] == "hello":
			self.hello()
		elif cm[0] == "addgroup" and len(cm) == 3:
			self.addgroup(cm[1], cm[2])
		elif cm[0] == "addgroup":
			print ("Error! Use 'addgroup server group'")
		elif cm[0] == "groups":
			self.listgroups()
		elif cm[0] == "group" and len(cm) == 2:
			self.group(cm[1])
		elif cm[0] == "group":
			print ("Error! Use 'group group_id' or 'group group_name'")
		elif cm[0] == "list" and (len(cm) == 3):
			self.artlist(cm[1], cm[2])
		elif cm[0] == "list":
			self.artlist()
		elif cm[0] == "article" and len(cm) == 2:
			self.article(cm[1])
		elif cm[0] == "article":
			print("Error! Use 'article art_id'")
		elif cm[0] == "help":
			print("Will be one day...")
				
	def hello(self):
		print("Hello! :-)")

	def addgroups(self, server, group):
		self.io.addgroup(server, group)
		print("Added new group")

	def listgroups(self):
		print("Your groups:")
		for g in self.groups:
			c = " " if g[3] == 0 else " [c] "
			print(" " + str(g[0]) + ":" + c + g[2] + " on server " + g[1])

	def group(self, gid):
		return 0

	# dispalying last 10 or chosen articles in group
	def artlist(self, start = None, end = None): 
		return 0

	# getting article
	def article(self, art):
		return 0
