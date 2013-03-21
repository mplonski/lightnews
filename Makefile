
help:
	@echo "Options: help setupdb clean"

setupdb:
	@echo "Removing old database..."
	@rm -f ./ln.db
	@echo "Creating new database..."
	@python ./make/setup.py
	@echo "Done"

clean:
	@echo "Removing database..."
	@rm -f ./ln.db
	@echo "Removing *.pyc files..."
	@rm -f ./*.pyc
	@echo "Done"

