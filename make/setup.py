import sqlite3

DEBUG = 1 # 1 - enabled

conn = sqlite3.connect('ln.db')
c = conn.cursor()

c.execute('CREATE TABLE options  (name text primary key, val text)')
c.execute('CREATE TABLE servers  (id integer primary key, name text, username text, password text)')
c.execute('CREATE TABLE groups   (id integer primary key, server_id integer, name text, cache integer, count integer, first integer, last integer)')
c.execute('CREATE TABLE articles (id integer primary key, art_id integer, server_id integer, group_id integer, title text, body text)')
conn.commit()

if DEBUG == 1:

	c.execute("INSERT INTO servers VALUES (NULL, 'news.gmane.org', NULL, NULL)")
	c.execute("INSERT INTO groups VALUES (NULL, 1, 'gmane.comp.python.committers', 10, 0, 0, 0)")
	c.execute("INSERT INTO servers VALUES (NULL, 'test2.test', NULL, NULL)")
	c.execute("INSERT INTO groups VALUES (NULL, 2, 'test_s2.test', 0, 200, 100, 300)")
	conn.commit()

conn.close()


