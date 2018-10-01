#!/bin/bash
#
# Script to Install
# Linux System Tools and Basic Python Components
# as well as to
# Start Jupyter Notebook Server
#
# Python for Algorithmic Trading
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH
#
# GENERAL LINUX
apt-get update  # updates the package index cache
apt-get upgrade -y  # updates packages
apt-get install -y git screen htop wget nano bzip2 # installs system tools
apt-get upgrade -y bash  # upgrades bash if necessary
apt-get clean  # cleans up the package index cache

# INSTALLING MINICONDA
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O Miniconda.sh
bash Miniconda.sh -b  # installs Miniconda
rm -rf Miniconda.sh  # removes the installer
export PATH="/root/miniconda3/bin:$PATH"  # prepends the new path for current session
# prepends the new path in the shell configuration
cat >> ~/.profile <<EOF
export PATH="/root/miniconda3/bin:$PATH"
EOF

# INSTALLING PYTHON LIBRARIES
conda install -y jupyter  # interactive data analytics in the browser
conda install -y pytables  # wrapper for HDF5 binary storage
conda install -y pandas  #  data analysis package
conda install -y pandas-datareader  # API wrapper for Google Finance
conda install -y matplotlib  # standard plotting library
conda install -y seaborn  # statistical plotting library
conda install -y quandl  # wrapper for Quandl data API
conda install -y scikit-learn  # machine learning library
conda install -y flask  # light weight web framework
conda install -y openpyxl  # library for Excel interaction
conda install -y pyyaml  # library to manage yaml files

pip install --upgrade pip  # upgrading the package manager
pip install q  # logging and debugging
pip install plotly  # interactive D3.js plots
pip install cufflinks  # combining plotly with pandas
pip install tensorflow  # deep learning library
# Python wrapper for Oanda API (v1 & v20)
pip install git+https://github.com/oanda/oandapy.git
pip install v20

# COPYING FILES AND CREATING DIRECTORIES
mkdir /root/.jupyter
mv /root/jupyter_notebook_config.py /root/.jupyter/
mv /root/cert.* /root/.jupyter
mkdir /root/notebook
cd /root/notebook

# STARTING JUPYTER NOTEBOOK
jupyter notebook --allow-root
