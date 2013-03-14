all: compile.py main.py lnlib.py
	@python -B compile.py
	@echo "Done"

clean: *.pyc
	@rm -r ./*.pyc
	@echo "Done"

