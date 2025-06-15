# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Raspberry Pi SDR (Software Defined Radio) Cyberdeck project that provides an easy-to-use interface for controlling SDR hardware and related applications. The system uses FastAPI as a REST API server with an ASGI interface (uvicorn) to control devices, processes, and applications through HTTP methods.

## Essential Commands

### Development Commands
- `make` - Complete setup: install dependencies, setup OS packages, and start server
- `make install` - Install Python packages from requirements.txt
- `make setup` - Install OS packages (rtl-sdr, sox) and create directories
- `make server` - Start the FastAPI server

### Python Environment Management
- **Use `uv` for all Python operations in this project**
- `uv venv` - Create virtual environment
- `uv pip install -r config/requirements.txt` - Install dependencies
- `uv run python src/api/main.py` - Run server with uv
- `uv run python src/api/gui.py -i {IP}` - Run GUI client with uv

### Manual Server Operations
- `cd src/api && python3 main.py` - Start server manually
- `cd src/api && python3 gui.py -i {IP_ADDRESS}` - Start GUI client
- Visit `http://{IP_ADDRESS}:5000/docs` - FastAPI documentation and testing interface

### Hardware Setup Commands
- `rtl_eeprom -d 0 -s 'rf1'` - Set unique serial for first RTL-SDR
- `rtl_eeprom -d 1 -s 'rf2'` - Set unique serial for second RTL-SDR

### Testing Commands
- `python3 src/tests/test_controller.py` - Test controller functionality
- `python3 src/tests/test_battadc.py` - Test battery ADC
- `python3 src/tests/test_bluetoothserver.py` - Test Bluetooth server

## Project Architecture

### Core Components
- **FastAPI Server** (`src/api/main.py`) - REST API endpoint handling
- **Server Class** (`src/api/server.py`) - System orchestration and management  
- **Systems Framework** (`src/api/systems.py`) - Base classes for Device, Process, Application
- **Configuration** (`src/api/config.ini`) - System definitions and parameters
- **GUI Client** (`src/api/gui.py`) - PyQt5-based control interface
- **Packet Handler** (`src/api/packet.py`) - Data packet processing

### System Types
The framework categorizes all subsystems into three types:
1. **Device** - Hardware requiring polling (I2C, GPIO, sensors)
2. **Process** - Software requiring input devices (RF decoders, audio processing)
3. **Application** - GUI applications (navigation, mapping software)

### Configuration Structure
Each subsystem is defined in `config.ini` with:
- `s_id` - Unique system identifier
- `s_name` - Human-readable name
- `s_type` - System type (device/process/application)
- Additional type-specific parameters

### Key Directories
- `src/api/` - Core FastAPI application and system control
- `src/api/gui/` - PyQt5 UI files (.ui format)
- `src/config/` - SDR device configuration files
- `src/controller/` - Arduino controller code and Python interface
- `src/scripts/` - Shell scripts for starting/stopping applications
- `src/tests/` - Hardware and system test scripts
- `config/` - Project configuration and requirements

### External Dependencies
The project integrates with several external tools that must be installed separately:
- **uhubctl** - USB hub control
- **dumpvdl2** - VDL2 decoder
- **dump1090** - ADS-B decoder  
- **acarsdec** - ACARS decoder
- **rtl-ais** - AIS decoder
- **rtl-sdr** - Extended RTL-SDR library with UDP control

### Hardware Integration
- **Raspberry Pi** with official 7" touchscreen (minimal setup)
- **RTL-SDR dongles** with unique serials 'rf1' and 'rf2'
- **I2C devices** for battery monitoring and system control
- **GPIO interfaces** for hardware control
- **Audio interfaces** for SDR processing

## Adding New Subsystems

To add a new subsystem:
1. Add configuration section in `src/api/config.ini`
2. Define system class in `src/api/systems.py` by subclassing Device, Process, or Application
3. Instantiate in `src/api/server.py` and pass the INI section name
4. Add REST API methods in `src/api/main.py` for HTTP control

## Important Development Notes

- **Use `uv` for all Python package management and execution**
- **Server runs on `0.0.0.0:5000`** - Accepts connections on any interface
- **Python 3** is used throughout the project
- **PyQt5** is used for the GUI client interface
- **InfluxDB integration** for system monitoring and data logging
- **Grafana support** for system monitoring dashboards
- **All script execution** happens through the FastAPI server
- **Hardware-specific code** targets Raspberry Pi GPIO and I2C interfaces
- **SDR applications** are controlled via shell scripts in `src/scripts/`

## Testing Strategy

- Hardware tests in `src/tests/` for controller, battery, and Bluetooth
- Manual testing via FastAPI docs interface at `/docs` endpoint
- Integration testing through GUI client connections
- Hardware validation requires actual Raspberry Pi and SDR hardware