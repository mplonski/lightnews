
all:
	@echo "Options: setupdb cleandb clean"

setupdb:
	@echo "Removing old database..."
	@rm -f ./ln.db
	@echo "Creating new database..."
	@python ./make/setup.py
	@echo "Done"

cleandb:
	@rm -f ./ln.db
	@echo "Database removed"

clean:
	@rm -f ./*.pyc
	@echo "Removed *.pyc"

