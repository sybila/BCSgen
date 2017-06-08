#! /bin/bash

# Pyt_installed=$(python --version)

echo 'Installing python2.7...'
sudo apt-get -y install python2.7
echo 'Installing python-qt4...'
sudo apt-get -y install python-qt4
echo 'Installing matplotlib...'
sudo apt-get -y install python-matplotlib

PIP_installed=$(dpkg-query -W --showformat='${Status}\n' python-pip|grep "install ok installed")
echo 'Checking for pip:' $PKG_OK

if [ "" == "$PKG_OK" ]; then
  echo "Installing pip..."
  sudo apt-get -y install python-pip
fi

echo "Installing markdown..."
sudo pip install markdown
echo "Installing numpy..."
sudo pip install numpy
echo "Installing sympy..."
sudo pip install sympy
echo "Installing scipy..."
sudo pip install scipy

echo "-----------------------------------------------------"
echo "Proceeding to rule parser."
echo "Installing g++..."
sudo apt-get -y install g++
echo "Installing swig..."
sudo apt-get -y install swig
echo "Installing python-dev..."
sudo apt-get -y install python-dev

PIP_installed=$(dpkg-query -W --showformat='${Status}\n' git|grep "install ok installed")
echo 'Checking for pip:' $PKG_OK

if [ "" == "$PKG_OK" ]; then
  echo "Installing git..."
  sudo apt-get -y install git
fi

cd Core/Import/
git clone "https://xtrojak@gitlab.fi.muni.cz/grp-sybila/rule-parser.git"
cd rule-parser
echo "Builing rule parser..."
make pv=python python
cp swig/RuleParser.py ../
cp swig/_RuleParser.so ../
cd ..
rm -rf rule-parser
