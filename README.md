lightnews
=========

light usenet client

### version

Lightnews is in prealpha version! (I hope it will be ready in... 1 week?)

```python
def behappy():
	return ':-)'
```

### requirements

Lightnews requires:

* Linux (you can modify code to be able to run it on Windows, but we officially support only Linux)
* python (lightnews is tested on python 2.7, 3.0 should be also ok)
* python libraries: os, sys, nntplib, sqlite3, getpass, readline, psycopg2
* lightnews libraries: lnlin, lnio, lncmd (included in repository)
* linux program: Makefile (required to run setup/cleaning automatically)

### configuration & cleaning up

To setup database (create tables):

```
make setupdb
```

To remove database and temporary files (e.g. .pyc): 

```
make clean
```

To display all available commands:

```
make help
```

### packages

We hope that lightnews is going to be ready in .deb (Debian/Ubuntu) and .rpm (Fedora) packages (and, in some time, in public repositories).

### user interface

Lightnews is operated in command-line style. Example:

```
 > help
   This program is...
   Author...
   Lincence...
 > addgroup server.name group.name
   Added group group.name on server.name
 >
```

### default mode and single-group mode

As you can see at __user interface__, lightnews is operated in command-like style.

There're two possible options of command-line. *First one* is enabled by default and means that all commands related to group are to declare which group they're going to be about. For example:

```
 > list 3
123 >> example topic
124 >> example topic
125 >> example topic
```

`list 3` means, that you want to display list of topics from group no. 3.

*Second one* is dedicated to work with one group (and *it is not implemented yet*). To switch to this mode you need to run:

```
 > setgroup 3
Done!
 group_name >
```

Now command-line is set to work with group 3, named group_name (remember that server's name is not displayed in this mode). In this mode you can simply run:

```
 > list
123 >> example topic
124 >> example topic
125 >> example topic
```

If you want to exit single-group mode, simply run:

```
group_name > unsetgroup
```

### manual

***it's not ready yet :)***

#### hello

Says hello.

```
 > hello
Hello! :-)
 >
```

#### addgroup

Adds new group.

```
 > addgroup
Error! Use 'addgroup server group'
 > addgroup server.test group.test
Added new group
 >
```

#### removegroup

Removes group.

Example:

```
 > removegroup
Error! Use 'removegroup server group'
 > removegroup server.test group.test
Group has been removed
 > 
```

#### groups

Display list of groups.

```
 > groups
Your groups:
 1: [c] gmane.comp.python.committers on server news.gmane.org
 2: test_s2.test on server test2.test
 >
```

1/2/... is group's id, [c] stands for enabled cache

#### list

Display list of topics in group.

```
 > list
Error! Use 'list group_id' or 'list group_id start end'
 > list 1
Displaying all cached articles (11) for group gmane.comp.python.committers on server news.gmane.org
2429 >> Re: [Infrastructure] test suite dependencies on www.python.org
2430 >> Re: [Infrastructure] test suite dependencies on www.python.org
2431 >> Re: Commit privileges for Roger Serwy for IDLE
2432 >> Re: [Infrastructure] test suite dependencies on www.python.org
2433 >> Re: Commit privileges for Roger Serwy for IDLE
2434 >> Re: [Infrastructure] test suite dependencies on www.python.org
2435 >> Re: [Infrastructure] test suite dependencies on www.python.org
2436 >> Re: Commit privileges for Roger Serwy for IDLE
2437 >> Re: Commit privileges for Roger Serwy for IDLE
2438 >> Re: Commit privileges for Roger Serwy for IDLE
2439 >> Re: Commit privileges for Roger Serwy for IDLE
 > list 1 2436 2438
2436 >> Re: Commit privileges for Roger Serwy for IDLE
2437 >> Re: Commit privileges for Roger Serwy for IDLE
2438 >> Re: Commit privileges for Roger Serwy for IDLE
 >
```

#### download

Downloads cache for group or all groups.

```
 > download
Error! Use 'download all' or 'download group_id' or 'download server group'
 >
```

You can define what should be cached (downloaded) using ... .

### more?

will be something (soon)

