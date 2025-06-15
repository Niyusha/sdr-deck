# Define the default target
.PHONY: all install server setup # Declare that all, install, server, and setup are not files

all: install server setup # This is the default target that will run if no target is specified, ie do install, setup, and server

# Target to install Python packages
install:
	@echo "Installing python packages from requirements.txt:"
	sudo apt update
	uv venv .venv
	uv pip install -r ./config/requirements.txt

# Target to install OS packages
setup:
	@echo "Installing os packages:"
	# Audio dependencies for pyalsaaudio
	sudo apt install -y libasound2-dev
	# SDR and audio tools
	sudo apt install -y rtl-sdr sox
	@echo "Creating directories"
	mkdir # TODO: needed dirs


# Target to start the server
# Navigate to src/api and init main.py
server:
	cd src/api && uv run python main.py
