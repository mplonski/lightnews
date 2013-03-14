all: compile.py main.py lnlib.py
	@python compile.py
	@echo "Done"

clean: *.pyc
	@rm -r ./*.pyc
	@echo "Done"

