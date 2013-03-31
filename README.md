Lightnews
=========

light usenet client

* [version](#version)
* [requirements](#requirements)
* [configuration & cleaning up](#configuration--cleaning-up)
* [packages](#packages)
* [user interface](#user-interface)
* [default mode and single-group mode](#default-mode-and-single-group-mode)
* [manual](#manual)
* [faq](#faq)

version
--------

Lightnews is in 1.0 beta version!

```python
def behappy():
	return ':-)'
```

requirements
------------

Lightnews requires:

* Linux (you can modify code to be able to run it on Windows, but we officially support only Linux)
* python (lightnews is tested on python 2.7, 3.0 should be also ok)
* python libraries: sys, os, time, nntplib, sqlite3, ycopg2.extensions, getpass, hashlib, socket, tempfile, getpass, readline
* lightnews libraries: lnlin, lnio, lncmd (included in repository)
* linux program: Makefile (required to run setup/cleaning automatically)

configuration & cleaning up
---------------------------

**Warning!** I strongly recommend running `make clean` after every update! It is quite possible that database has been changed and it's necessary to destroy old database. You should also run `./configure` after `make clean` to make sure that everything is ok :-)

To check if all necessary files / libs exist:

```
./configure
```

If everything is ok, Makefile should be generated.

To remove database, temporary files (e.g. .pyc), Makefile: 

```
make clean
```

To display all available commands:

```
make help
```

packages
--------

We hope that lightnews is going to be ready in .deb (Debian/Ubuntu) and .rpm (Fedora) packages (and, in some time, in public repositories).

user interface
--------------

Lightnews is operated in command-line style.

```
 > help
   This program is...
   Author...
   Lincence...
 > addgroup server.name group.name
   Added group group.name on server.name
 >
```

default mode and single-group mode
----------------------------------

As you can see at [user interface](#user-interface) lightnews is operated in command-like style. There're two possible options of command-line.

**First one** is enabled by default and you can run only theese commands: addgroup, removegroup, groups, group, download, help, hello. For example:

```
 > groups
Your groups:
 1: gmane.comp.python.committers on server news.gmane.org
 2: test_s2.test on server test2.test
 >
```

**Second one** is dedicated to work with one group and operates following commands: group, list, article. To switch to this mode you need to run:

```
 > setgroup group_name
Done! Turned on single-group mode for group group_name on server server_name.
 group_name >
```

Command-line is set to work with group named group_name. Now you can simply run:

```
 group_name > list 3
123 >> example topic
124 >> example topic
125 >> example topic
```

`list 3` stands for 'list last 3 messages'.

If you want to exit single-group mode, run:

```
group_name > setgroup
```

manual
------

### beta release -- manual should be up-to-date ###

### hello

Says hello.

```
 > hello
Hello! :-)
 >
```

Works in both modes.

### addgroup

Adds new group.

```
 > addgroup
Error! Use 'addgroup server group'
 > addgroup server.test group.test
Added new group
 >
```

Works in both modes.

### removegroup

Removes group.

Example:

```
 > removegroup
Error! Use 'removegroup server group'
 > removegroup server.test group.test
Group has been removed
 > 
```

Works only in default-mode.

### groups

Display list of groups.

```
 > groups
Your groups:
 1: [c] gmane.comp.python.committers on server news.gmane.org
 2: test_s2.test on server test2.test
 >
```

1/2/... is group's id, [c] stands for enabled cache

Works in both modes.

### list

Display list of **unread** topics in group.

```
 group_name > list 3
2442 >> Re: Commit privileges for Roger Serwy for IDLE
2443 >> Re: Commit privileges for Roger Serwy for IDLE
2444 >> Re: Commit privileges for Roger Serwy for IDLE
 group_name > list
2437 >> Re: Commit privileges for Roger Serwy for IDLE
2438 >> Re: Commit privileges for Roger Serwy for IDLE
2439 >> Re: Commit privileges for Roger Serwy for IDLE
2440 >> Re: Commit privileges for Roger Serwy for IDLE
2441 >> Re: Commit privileges for Roger Serwy for IDLE
2442 >> Re: Commit privileges for Roger Serwy for IDLE
2443 >> Re: Commit privileges for Roger Serwy for IDLE
2444 >> Re: Commit privileges for Roger Serwy for IDLE
 group_name > list 2430 2435
2430 >> Re: [Infrastructure] test suite dependencies on www.python.org
2431 >> Re: Commit privileges for Roger Serwy for IDLE
2432 >> Re: [Infrastructure] test suite dependencies on www.python.org
2433 >> Re: Commit privileges for Roger Serwy for IDLE
2434 >> Re: [Infrastructure] test suite dependencies on www.python.org
2435 >> Re: [Infrastructure] test suite dependencies on www.python.org
 group_name >
```

Works only in single-group mode.

### listall

Works exactly like `list`, but displays also read (and bold new ones).

### article

Displays body of specified article. Number next to `article` is article's id (visible after running `list`).

```
 group_name > article 2435
> Body, body, body...
> Body, body, body...
Body, body, body...

bye,
body, body
 group_name > 
```

Works only in single-group mode.

### send

Sends message to list.

Usage: `send` to send message, `send art_id` to send answer to some mail.

**Warning!** You need to set `setfrom` before running `send`.

Works only in single-group mode.

### setfrom

Sets From Field in sent messages (doesn't work in past).

```
 > setfrom mail@example.com
Done!
 >
```

Works in both modes.

### download

Downloads cache for specified group or all groups.

```
 group_name > download
Downloading started... stay calm :-) (in case of slow downlink and big cache it may take some time)
Done! Thanks for being patient!
 group_name > setgroup
 > download 1
Downloading started... stay calm :-) (in case of slow downlink and big cache it may take some time)
Done! Thanks for being patient!
 >
```

If you run `download` in single-group mode (with no arguments) there will be cache downloaded for current group.

You can define what should be cached (downloaded) using `setcache`.

Works in both modes.

### setcache

Sets cache for exisiting group.

```
 > groups
Your groups:
 1: [c] gmane.comp.python.committers on server news.gmane.org
 2: test_s2.test on server test2.test

 > setcache 1
How many articles are to be cached? (0 means none) 10
Done!

 >
```

### setauth

Sets auth settings for existing server.

```
 > setauth news.gmane.org
Is auth required? [Y/n] n
Done!
 > 
```

FAQ
---

### When are you going to release stable?

We love the idea of endless beta version. How could you know that any software is fully stable?

### Ha ha, I found bug! You suck!

Please [report it](/mplonski/lightnews/issues) and, if possible, figure out why it is not working right, fix it and commit bugfix.

### (...) is not working

1. Check if used syntax is ok. Sometimes it's really important if you are using group's name, id or any other number.
2. Check if this issue is known by our developers. Take a look at [issues](/mplonski/lightnews/issues).
3. If 1. and 2. is not helping, [report a bug](/mplonski/lightnews/issues).
4. After reporting bug you can figure out yourself why it is not working, fix it and commit bugfix.

### Why don't you support Windows?

We love Linux. We use Linux. Why don't you support Windows? Lightnews is under GNU GPL!

### Do you like toasts?

Yes, we do.

