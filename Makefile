# Pymp Makefile

PYTHON=/usr/bin/python

all: clean
	cd src && $(PYTHON) build.py && rm -f ./build.pyc

clean:
	rm -f src/*.pyc
	
#End of file
