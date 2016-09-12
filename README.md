# IPython Vega [![PyPI](https://img.shields.io/pypi/v/vega.svg?maxAge=2592000)](https://pypi.python.org/pypi/vega) [![Build Status](https://travis-ci.org/vega/ipyvega.svg?branch=master)](https://travis-ci.org/vega/ipyvega)

IPython/Jupyter notebook module for [Vega](https://github.com/vega/vega-lite), and [Vega-Lite](https://github.com/vega/vega-lite), [Polestar](https://github.com/vega/polestar), and [Voyager](https://github.com/vega/voyager). Notebooks with embedded visualizations can be viewed on github and nbviewer.

Available on [pypi](https://pypi.python.org/pypi/vega) and [conda-forge](https://github.com/conda-forge/vega-feedstock).

![screenshot](https://raw.githubusercontent.com/vega/ipyvega/master/screenshot.png "Screenshot of the Vega-Lite module")


## Install and run

### Conda (Recommended)
If you are using [conda](http://conda.pydata.org) you can install the most
recent release of this package
from the [conda-forge](http://conda-forge.github.io) channel as follows:
```sh
conda install vega --channel conda-forge
```
The above command automatically installs all dependencies and enables
the ipyvega Jupyter notebook extension.

### Python Package Index
To install ``vega`` and its dependencies from the Python Package Index using
``pip``, use the following commands:

```sh
pip install jupyter pandas vega
jupyter nbextension install --py vega
```

### From Source
To install from source, make sure you have ``jupyter`` and ``pandas`` installed,
then download this repository and run
```sh
python setup.py install
```

## Usage

Once the package is installed, run
```sh
jupyter notebook
```
to launch the Jupyter notebook server, and use ``vega`` within the notebook.
See the example notebooks for [Vega-Lite](https://github.com/vega/ipyvega/blob/master/notebooks/VegaLite.ipynb) and [Vega](https://github.com/vega/ipyvega/blob/master/notebooks/Vega.ipynb).

To run the notebooks yourself, you need to get the file [`cars.json`](https://raw.githubusercontent.com/vega/ipyvega/master/notebooks/cars.json).


## Developers

Install requirements: `pip install -r requirements.txt`

Symlink files instead of copying files:

```sh
python setup.py develop
jupyter nbextension install --py --symlink vega
```

Run kernel: `jupyter notebook`

To rebuild the javascript continuously, run `npm run watch`.

Publish a new version to pypi with `python3 setup.py sdist upload`.


## Resources

How to implement an nbextension.

* https://github.com/ipython-contrib/IPython-notebook-extensions/blob/master/nbextensions/styling/table_beautifier/main.js
* https://ipywidgets.readthedocs.org/en/latest/index.html
* https://github.com/jovyan/pythreejs
