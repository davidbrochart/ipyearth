[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/davidbrochart/ipyearth/master?filepath=examples%2Fdemo.ipynb)

ipyearth
===============================

An IPython Widget for Earth Maps

![alt text](examples/example.png)

Installation
------------

To install, clone this repository and use pip:

    $ git clone https://github.com/davidbrochart/ipyearth.git
    $ cd ipyearth
    $ pip install -e .
    $ jupyter nbextension enable --py --sys-prefix ipyearth


For a development installation (requires npm):

    $ jupyter nbextension install --py --symlink --sys-prefix ipyearth
    $ jupyter nbextension enable --py --sys-prefix ipyearth

For JupyterLab:

    $ jupyter labextension install @jupyter-widgets/jupyterlab-manager
    $ jupyter labextension install ./js
