
clean:
	rm -rf *~ *.pyc *.log

spotless: clean
	rm -rf *.sqlite3
