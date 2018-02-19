#! /bin/bash

# Pyt_installed=$(python --version)

echo 'Installing python2.7...'
sudo apt-get -y install python2.7
echo 'Installing python-qt4...'
sudo apt-get -y install python-qt4
echo 'Installing matplotlib...'
sudo apt-get -y install python-matplotlib
echo 'Installing tk...'
sudo apt-get -y install python-tk

PKG_OK=$(dpkg-query -W --showformat='${Status}\n' python-pip|grep "install ok installed")
echo 'Checking for pip:' $PKG_OK

if [ "" == "$PKG_OK" ]; then
  echo "Installing pip..."
  sudo apt-get -y install python-pip
fi

echo "Installing setuptools..."
sudo pip install setuptools
echo "Installing markdown..."
sudo pip install markdown
echo "Installing numpy..."
sudo pip install numpy
echo "Installing sympy..."
sudo pip install sympy
echo "Installing scipy..."
sudo pip install scipy

PKG_OK=$(dpkg-query -W --showformat='${Status}\n' git|grep "install ok installed")
echo 'Checking for git:' $PKG_OK

if [ "" == "$PKG_OK" ]; then
  echo "Installing git..."
  sudo apt-get -y install git
fi

git clone "https://github.com/sybila/BCSgen.git"

# download release of RuleParser from this link: https://gitlab.fi.muni.cz/grp-sybila/rule-parser/tags
# and place it to Core/Import/ directory
