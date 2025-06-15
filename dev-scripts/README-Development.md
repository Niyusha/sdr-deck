# SDR Cyberdeck Development Environment

This document describes the optimal development workflow for the SDR cyberdeck project using a development machine + Raspberry Pi setup.

## 🚀 Quick Start

1. **Set up environment**: 
   ```bash
   export RPI_IP=192.168.1.100  # Your RPi IP
   ./dev-setup.sh
   ```

2. **Start developing**:
   ```bash
   # Edit code locally, then:
   ./sync-to-rpi.sh    # Sync changes
   ./test-on-rpi.sh    # Test on RPi
   ./debug-rpi.sh      # SSH debug session
   ```

## 🔧 Development Workflow Options

### Option 1: Manual Sync (Recommended)
Best for stable development with controlled deployments.

```bash
# 1. Edit code locally
vim src/api/main.py

# 2. Sync to RPi
./sync-to-rpi.sh

# 3. Test remotely
ssh pi@192.168.1.100 'cd /home/pi/sdr-deck && make server'

# 4. Debug if needed
./debug-tools.py --host 192.168.1.100 health
```

### Option 2: Live Sync (Fastest)
Automatically syncs files on changes (requires `fswatch`).

```bash
# Terminal 1: Start live sync
./watch-and-sync.sh

# Terminal 2: SSH session for testing
./debug-rpi.sh

# Terminal 3: Monitor API health
./debug-tools.py --host 192.168.1.100 monitor
```

### Option 3: VS Code Remote Development
Use VS Code tasks and remote debugging.

1. Open VS Code in project directory
2. **Ctrl+Shift+P** → "Tasks: Run Task"
3. Choose from:
   - "Sync to RPi"
   - "Test on RPi" 
   - "Debug RPi Health"
   - "SSH to RPi"
   - "Start Live Sync"

## 🛠️ Development Scripts

### Core Scripts
- `./dev-setup.sh` - Complete environment setup
- `./sync-to-rpi.sh` - Quick code sync
- `./test-on-rpi.sh` - Sync and run server
- `./debug-rpi.sh` - Remote tmux debug session
- `./watch-and-sync.sh` - Live file watching (requires fswatch)

### Debug Tools
```bash
# Health check
./debug-tools.py --host RPi_IP health

# Monitor systems
./debug-tools.py --host RPi_IP monitor --interval 5 --duration 60

# Debug specific system
./debug-tools.py --host RPi_IP debug battery

# Test connectivity
./debug-tools.py --host RPi_IP ping
```

## 🔍 Debugging Strategies

### 1. **API Health Monitoring**
```bash
# Quick health check
./debug-tools.py --host 192.168.1.100 health

# Continuous monitoring
./debug-tools.py --host 192.168.1.100 monitor --interval 3
```

### 2. **Remote tmux Session**
```bash
# SSH with persistent session
./debug-rpi.sh

# Inside tmux:
cd /home/pi/sdr-deck
make server           # Start server
# Ctrl+B, D to detach
# tmux attach to reconnect
```

### 3. **Log Analysis**
```bash
# SSH and check logs
ssh pi@192.168.1.100
cd /home/pi/sdr-deck
journalctl -f         # System logs
tail -f /var/log/syslog  # General logs

# Python debugging
python3 -u src/api/main.py  # Unbuffered output
```

### 4. **Hardware Debugging**
```bash
# Check SDR dongles
rtl_test

# Check I2C devices
i2cdetect -y 1

# Check GPIO status
gpio readall

# Audio system
aplay -l
arecord -l
```

## 🏗️ Environment Setup Details

### RPi Prerequisites
```bash
# System packages (handled by dev-setup.sh)
sudo apt install libasound2-dev rtl-sdr sox git python3 python3-pip

# Python environment
uv venv .venv --python 3.11
uv pip install -r config/requirements.txt
```

### Development Machine
```bash
# Required tools
# - uv (Python package manager)
# - rsync (file sync)
# - ssh (remote access)

# Optional tools
brew install fswatch    # macOS live sync
apt install fswatch     # Linux live sync
```

## 📡 Network Configuration

### Static IP (Recommended)
Set static IP on RPi for consistent connection:

```bash
# On RPi: /etc/dhcpcd.conf
interface wlan0
static ip_address=192.168.1.100/24
static routers=192.168.1.1
static domain_name_servers=192.168.1.1 8.8.8.8
```

### SSH Configuration
```bash
# ~/.ssh/config
Host sdr-rpi
    HostName 192.168.1.100
    User pi
    IdentityFile ~/.ssh/id_rsa
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

## 🐛 Troubleshooting

### Common Issues

1. **SSH Connection Failed**
   ```bash
   # Check RPi is reachable
   ping 192.168.1.100
   
   # Check SSH service
   ssh pi@192.168.1.100 'systemctl status ssh'
   ```

2. **Package Import Errors**
   ```bash
   # Check Python environment on RPi
   ssh pi@192.168.1.100 'cd /home/pi/sdr-deck && uv run python -c "import fastapi; print(\"OK\")"'
   
   # Reinstall dependencies
   ssh pi@192.168.1.100 'cd /home/pi/sdr-deck && uv pip install -r config/requirements.txt'
   ```

3. **Hardware Not Detected**
   ```bash
   # Check RTL-SDR
   ssh pi@192.168.1.100 'rtl_test -t'
   
   # Check I2C
   ssh pi@192.168.1.100 'i2cdetect -y 1'
   
   # Check permissions
   ssh pi@192.168.1.100 'groups $USER'  # Should include dialout, gpio
   ```

4. **API Server Won't Start**
   ```bash
   # Check port availability
   ssh pi@192.168.1.100 'netstat -tulpn | grep :5000'
   
   # Run with debug output
   ssh pi@192.168.1.100 'cd /home/pi/sdr-deck && uv run python -u src/api/main.py'
   ```

## 🚀 Performance Tips

1. **Use tmux for persistent sessions**
2. **Set up SSH key authentication** (no passwords)
3. **Use rsync excludes** to avoid syncing large files
4. **Monitor with htop/iotop** during development
5. **Use Git branches** for experimental features
6. **Keep logs clean** with logrotate

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Raspberry Pi GPIO Documentation](https://www.raspberrypi.org/documentation/usage/gpio/)
- [RTL-SDR Documentation](https://osmocom.org/projects/rtl-sdr/wiki)
- [VS Code Remote Development](https://code.visualstudio.com/docs/remote/remote-overview)