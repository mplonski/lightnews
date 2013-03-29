lightnews
=========

light usenet client

version
--------

Lightnews is in prealpha version! (I hope it will be ready in... 1 week?)

```python
def behappy():
	return ':-)'
```

requirements
------------

Lightnews requires:

* Linux (you can modify code to be able to run it on Windows, but we officially support only Linux)
* python (lightnews is tested on python 2.7, 3.0 should be also ok)
* python libraries: os, sys, nntplib, sqlite3, getpass, readline, psycopg2
* lightnews libraries: lnlin, lnio, lncmd (included in repository)
* linux program: Makefile (required to run setup/cleaning automatically)

configuration & cleaning up
---------------------------

**Warning!** I strongly recommend running `make clean` after every update! It is quite possible that database has been changed and it's necessary to destroy old database.

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

As you can see at [user interface](https://github.com/mplonski/lightnews#user-interface) lightnews is operated in command-like style. There're two possible options of command-line.

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

# it's not ready yet :) #

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
gmane.comp.python.committers > list 3
2441 >> Re: Commit privileges for Roger Serwy for IDLE
2442 >> Re: Commit privileges for Roger Serwy for IDLE
2443 >> Re: Commit privileges for Roger Serwy for IDLE
2444 >> Re: Commit privileges for Roger Serwy for IDLE
 gmane.comp.python.committers > list
2434 >> Re: [Infrastructure] test suite dependencies on www.python.org
2435 >> Re: [Infrastructure] test suite dependencies on www.python.org
2436 >> Re: Commit privileges for Roger Serwy for IDLE
2437 >> Re: Commit privileges for Roger Serwy for IDLE
2438 >> Re: Commit privileges for Roger Serwy for IDLE
2439 >> Re: Commit privileges for Roger Serwy for IDLE
2440 >> Re: Commit privileges for Roger Serwy for IDLE
2441 >> Re: Commit privileges for Roger Serwy for IDLE
2442 >> Re: Commit privileges for Roger Serwy for IDLE
2443 >> Re: Commit privileges for Roger Serwy for IDLE
2444 >> Re: Commit privileges for Roger Serwy for IDLE
 gmane.comp.python.committers > list 2430 2435
2430 >> Re: [Infrastructure] test suite dependencies on www.python.org
2431 >> Re: Commit privileges for Roger Serwy for IDLE
2432 >> Re: [Infrastructure] test suite dependencies on www.python.org
2433 >> Re: Commit privileges for Roger Serwy for IDLE
2434 >> Re: [Infrastructure] test suite dependencies on www.python.org
2435 >> Re: [Infrastructure] test suite dependencies on www.python.org
 >
```

Works only in single-group mode.

### listall

Works exactly like `list`, but displays also read (and bold new ones).

### download

Downloads cache for specified group or all groups.

```
 gmane.comp.python.committers > download
Downloading started... stay calm :-) (in case of slow downlink and big cache it may take some time)
Done! Thanks for being patient!
 gmane.comp.python.committers > setgroup
 > download 1
Downloading started... stay calm :-) (in case of slow downlink and big cache it may take some time)
Done! Thanks for being patient!
 >
```

If you run `download` in single-group mode (with no arguments) there will be cache downloaded for current group.

You can define what should be cached (downloaded) using ... .

Works in both modes.

more?
-----

will be something (soon)

