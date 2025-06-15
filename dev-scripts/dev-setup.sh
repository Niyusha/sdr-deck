#!/bin/bash
# SDR Cyberdeck Development Setup Script
# Sets up fluid development environment between dev machine and RPi

set -e

echo "🔧 SDR Cyberdeck Development Environment Setup"
echo "=============================================="

# Configuration
RPI_IP="${RPI_IP:-192.168.1.100}"
RPI_USER="${RPI_USER:-pi}"
PROJECT_PATH="/home/$RPI_USER/sdr-deck"

echo "📡 Target RPi: $RPI_USER@$RPI_IP"
echo "📁 Project path: $PROJECT_PATH"

# Function to check if RPi is reachable
check_rpi() {
    echo "🔍 Checking RPi connectivity..."
    if ping -c 1 -W 3 "$RPI_IP" > /dev/null 2>&1; then
        echo "✅ RPi is reachable at $RPI_IP"
    else
        echo "❌ Cannot reach RPi at $RPI_IP"
        echo "   Please check IP address and network connection"
        exit 1
    fi
}

# Function to setup SSH keys
setup_ssh_keys() {
    echo "🔑 Setting up SSH keys..."
    
    if [ ! -f ~/.ssh/id_rsa ]; then
        echo "🔐 Generating SSH key..."
        ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
    fi
    
    echo "📤 Copying SSH key to RPi..."
    ssh-copy-id "$RPI_USER@$RPI_IP" || {
        echo "❌ Failed to copy SSH key. Please run manually:"
        echo "   ssh-copy-id $RPI_USER@$RPI_IP"
        exit 1
    }
    
    echo "✅ SSH key setup complete"
}

# Function to setup RPi environment
setup_rpi_env() {
    echo "🏗️ Setting up RPi environment..."
    
    ssh "$RPI_USER@$RPI_IP" << 'EOF'
        # Update system
        echo "📦 Updating system packages..."
        sudo apt update && sudo apt upgrade -y
        
        # Install system dependencies
        echo "🔧 Installing system dependencies..."
        sudo apt install -y \
            libasound2-dev \
            rtl-sdr \
            sox \
            git \
            python3 \
            python3-pip \
            python3-venv \
            htop \
            tmux \
            vim
        
        # Install uv if not present
        if ! command -v uv &> /dev/null; then
            echo "🐍 Installing uv..."
            curl -LsSf https://astral.sh/uv/install.sh | sh
            source ~/.local/bin/env
        fi
        
        echo "✅ RPi environment setup complete"
EOF
}

# Function to sync code to RPi
sync_code() {
    echo "📁 Syncing code to RPi..."
    
    # Create project directory on RPi
    ssh "$RPI_USER@$RPI_IP" "mkdir -p $PROJECT_PATH"
    
    # Sync code excluding unnecessary files
    rsync -avz --progress \
        --exclude='.git' \
        --exclude='.venv' \
        --exclude='__pycache__' \
        --exclude='*.pyc' \
        --exclude='.pytest_cache' \
        --exclude='node_modules' \
        --exclude='test_api_*.py' \
        ./ "$RPI_USER@$RPI_IP:$PROJECT_PATH/"
    
    echo "✅ Code sync complete"
}

# Function to setup Python environment on RPi
setup_python_env() {
    echo "🐍 Setting up Python environment on RPi..."
    
    ssh "$RPI_USER@$RPI_IP" << EOF
        cd $PROJECT_PATH
        
        # Create virtual environment
        ~/.local/bin/uv venv .venv --python 3.11
        
        # Install dependencies
        ~/.local/bin/uv pip install -r config/requirements.txt
        
        echo "✅ Python environment setup complete"
EOF
}

# Function to create development scripts
create_dev_scripts() {
    echo "📜 Creating development scripts..."
    
    # Create sync script in project root
    cat > ../sync-to-rpi.sh << EOF
#!/bin/bash
# Quick sync script for development
echo "🔄 Syncing code to RPi..."
rsync -avz --progress \\
    --exclude='.git' \\
    --exclude='.venv' \\
    --exclude='__pycache__' \\
    --exclude='*.pyc' \\
    ./ "$RPI_USER@$RPI_IP:$PROJECT_PATH/"
echo "✅ Sync complete"
EOF
    chmod +x ../sync-to-rpi.sh
    
    # Create remote test script in project root
    cat > ../test-on-rpi.sh << EOF
#!/bin/bash
# Test script that syncs and runs on RPi
echo "🚀 Testing on RPi..."
./sync-to-rpi.sh
ssh "$RPI_USER@$RPI_IP" "cd $PROJECT_PATH && make server"
EOF
    chmod +x ../test-on-rpi.sh
    
    # Create debug script in project root
    cat > ../debug-rpi.sh << EOF
#!/bin/bash
# SSH into RPi with tmux session
echo "🐛 Opening debug session on RPi..."
ssh -t "$RPI_USER@$RPI_IP" "cd $PROJECT_PATH && tmux new-session -s sdr-debug || tmux attach-session -s sdr-debug"
EOF
    chmod +x ../debug-rpi.sh
    
    echo "✅ Development scripts created:"
    echo "   ./sync-to-rpi.sh   - Quick code sync"
    echo "   ./test-on-rpi.sh   - Sync and test"
    echo "   ./debug-rpi.sh     - Remote debug session"
}

# Function to setup live sync (optional)
setup_live_sync() {
    echo "🔄 Setting up live file sync (optional)..."
    
    if command -v fswatch &> /dev/null; then
        cat > ../watch-and-sync.sh << EOF
#!/bin/bash
# Live file sync - watches for changes and syncs automatically
echo "👀 Watching for file changes..."
echo "   Press Ctrl+C to stop"

fswatch -o . | while read f; do
    echo "📁 File changed, syncing..."
    ./sync-to-rpi.sh
done
EOF
        chmod +x ../watch-and-sync.sh
        echo "✅ Live sync script created: ./watch-and-sync.sh"
        echo "   Install fswatch: brew install fswatch (macOS) or apt install fswatch (Linux)"
    else
        echo "ℹ️  Install fswatch for automatic file watching"
    fi
}

# Main setup process
main() {
    case "${1:-all}" in
        "rpi-ip")
            echo "Current RPi IP: $RPI_IP"
            echo "To change: export RPI_IP=your.rpi.ip.address"
            ;;
        "check")
            check_rpi
            ;;
        "ssh")
            setup_ssh_keys
            ;;
        "sync")
            check_rpi
            sync_code
            ;;
        "env")
            check_rpi
            setup_rpi_env
            setup_python_env
            ;;
        "scripts")
            create_dev_scripts
            setup_live_sync
            ;;
        "all"|*)
            check_rpi
            setup_ssh_keys
            setup_rpi_env
            sync_code
            setup_python_env
            create_dev_scripts
            setup_live_sync
            
            echo ""
            echo "🎉 Development environment setup complete!"
            echo ""
            echo "📋 Next steps:"
            echo "   1. Test connection: ./debug-rpi.sh"
            echo "   2. Quick sync: ./sync-to-rpi.sh"
            echo "   3. Test & run: ./test-on-rpi.sh"
            echo "   4. Live sync: ./watch-and-sync.sh (if fswatch installed)"
            echo ""
            echo "🔧 Manual commands:"
            echo "   SSH: ssh $RPI_USER@$RPI_IP"
            echo "   Run server: ssh $RPI_USER@$RPI_IP 'cd $PROJECT_PATH && make server'"
            ;;
    esac
}

# Run main function with arguments
main "$@"