# 3d-tool
3d visualization tool in python

Follow the steps below to install.

Anaconda is a python installation that comes with
most of the necessary special libraries already installed.


Install Anaconda:
*****************
1)  download python anaconda distribution from http://continuum.io/downloads

1a) execute "bash <downloaded file>" in the shell.

1b) choose installation path of anaconda.


Update Anaconda:
****************
1c) execute "conda update conda" in the shell.

1d) execute "conda update anaconda" in the shell.

1e) execute "conda install mpi4py" in the shell.

1f) execute "conda install bokeh" in the shell.

1g) modify your PATH variable such that python is called
from /YourPathTo/anaconda/bin/python
(newer anaconda distros can do this automatically for you
during the install process)


Install SPICE/ pySPICE
***********************
pySPICE in an unofficial wrapper for the NAIF cspice toolkit

2a) download cspice toolkit from:
http://naif.jpl.nasa.gov/naif/toolkit_C.html.

2b) download pySpice from
https://github.com/rca/PySPICE.

2c) extract both downloaded packages and move the extracted cspice
folder into the PySPICE-master directory.

2d) from inside PySPICE-master execute the following two commands from
the shell:
python setup.py build_ext
python setup.py install
