# Define the default target
.PHONY: all install server setup # Declare that all, install, server, and setup are not files

all: install server setup # This is the default target that will run if no target is specified, ie do install, setup, and server

# Target to install Python packages
install:
	@echo "Installing python packages from requirements.txt:"
	pip install -r requirements.txt

# Target to install OS packages
setup:
	@echo "Installing os packages:"
	sudo apt update
	sudo apt install -y rtl-sdr sox
	@echo "Creating directories"
	mkdir # TODO: needed dirs

# Target to start the server
# Navigate to src/api and init main.py
server:
	cd src/api &&
	python3 main.py
