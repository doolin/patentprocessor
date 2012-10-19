
clean:
	rm -rf *~ *.pyc

softlinks:
	ln -s /data/patentdata/locations/loctbl.sqlite3 .
	ln -s /data/patentdata/NBER/NBER_asg .

spotless: clean
	rm -rf *.sqlite3
