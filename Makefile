make install:
	pip3 install -r ./doc/requirements.txt

make server:
	cd src/api\
	&& python3 main.py