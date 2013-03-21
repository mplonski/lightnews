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

### manual

#### test

#### test2

### more?

will be something (soon)

