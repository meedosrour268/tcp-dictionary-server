PYTHON = python3

all:
	$(PYTHON) -m py_compile client.py server1.py server2.py server3.py

server1:
	$(PYTHON) server1.py 5000

server2:
	$(PYTHON) server2.py 5000

server3:
	$(PYTHON) server3.py 5000

client:
	$(PYTHON) client.py 127.0.0.1 5000

clean:
	rm -rf __pycache__