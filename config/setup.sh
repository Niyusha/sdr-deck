# Install python packages
echo "Installing python packages from requirements.txt:"
pip install -r requirements.txt

# Install needed os packages
echo "Installing os packages:"
sudo apt update
sudo apt install rtl-sdr sox

echo "Creating directories"
mkdir #Create needed dirs on SD card