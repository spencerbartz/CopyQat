clean:
	find . -type f -name '*.pyc' -delete

server:
	python serverdriver.py

client:
	python clientdriver.py --file 'testfile0.txt;testfile1.txt'

