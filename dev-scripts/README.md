# Development Scripts

This directory contains development tools and scripts for the SDR Cyberdeck project.

## Scripts

- **`dev-setup.sh`** - Complete development environment setup
  - Sets up SSH keys, RPi environment, code sync, and creates utility scripts
  - Usage: `./dev-setup.sh` (from project root)

- **`debug-tools.py`** - Remote debugging utilities
  - API health checks, system monitoring, endpoint testing
  - Usage: `python debug-tools.py --host RPi_IP health`

- **`README-Development.md`** - Comprehensive development guide
  - Detailed workflow explanations and troubleshooting

## Generated Scripts (created by dev-setup.sh)

These scripts are created in the project root for easy access:

- `sync-to-rpi.sh` - Quick code synchronization
- `test-on-rpi.sh` - Sync and run server
- `debug-rpi.sh` - Remote SSH debugging session  
- `watch-and-sync.sh` - Live file synchronization (if fswatch available)

## Usage

Run setup from project root:
```bash
cd /path/to/sdr-deck
export RPI_IP=192.168.1.100  # Your RPi IP
./dev-scripts/dev-setup.sh
```

This creates all the utility scripts in the project root for convenient development workflow.