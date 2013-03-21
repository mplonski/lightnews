lightnews
=========

light usenet client

### version

Lightnews is in prealpha version! (I hope it will be ready in... 1 week?)

```python
def behappy():
	return ':-)'
```

### configuration & cleaning up

To setup database (create tables):

```
make setupdb
```

To delete database:

```
make cleandb
```

To remove temporary files (e.g. .pyc): 

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

Lightnews will be operated in command-line style. Example:

```
 > help
   This program is...
   Author...
   Lincence...
 > addgroup server.name group.name
   Added group group.name on server.name
 >
```

### more?

will be something (soon)

