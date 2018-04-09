#! /bin/bash

# Pyt_installed=$(python --version)

echo 'Installing python3...'
sudo apt-get -y install python3
echo 'Installing python-qt4...'
sudo apt-get -y install python3-pyqt4
echo 'Installing matplotlib...'
sudo apt-get -y install python3-matplotlib
echo 'Installing tk...'
sudo apt-get -y install python3-tk
echo 'Installing pyside...'
sudo apt-get -y install python3-pyside

PKG_OK=$(dpkg-query -W --showformat='${Status}\n' python3-pip|grep "install ok installed")
echo 'Checking for pip:' $PKG_OK

if [ "" == "$PKG_OK" ]; then
  echo "Installing pip..."
  sudo apt-get -y install python3-pip
fi

echo "Installing setuptools..."
sudo pip3 install setuptools
echo "Installing markdown..."
sudo pip3 install markdown
echo "Installing numpy..."
sudo pip3 install numpy
echo "Installing sympy..."
sudo pip3 install sympy
echo "Installing scipy..."
sudo pip3 install scipy

PKG_OK=$(dpkg-query -W --showformat='${Status}\n' git|grep "install ok installed")
echo 'Checking for git:' $PKG_OK

if [ "" == "$PKG_OK" ]; then
  echo "Installing git..."
  sudo apt-get -y install git
fi

#git clone "https://github.com/sybila/BCSgen.git"

# download release of RuleParser from this link: https://gitlab.fi.muni.cz/grp-sybila/rule-parser/tags
# and place it to Core/Import/ directory
