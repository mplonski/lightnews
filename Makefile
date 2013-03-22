
help:
	@echo "Options: clean help install setupdb"

install:
	@echo "Installing... (sorry, not available in prealpha)"

setupdb:
	@echo "Removing old database..."
	@rm -f ./ln.db
	@echo "Creating new database..."
	@python ./make/setupdb.py
	@echo "Done"

clean:
	@echo "Removing database..."
	@rm -f ./ln.db
	@echo "Removing *.pyc files..."
	@rm -f ./*.pyc
	@echo "Done"

