# IPython Vega 3 [![PyPI](https://img.shields.io/pypi/v/vega3.svg?maxAge=2592000)](https://pypi.python.org/pypi/vega3) [![Build Status](https://travis-ci.org/vega/ipyvega.svg?branch=vega3)](https://travis-ci.org/vega/ipyvega)

IPython/Jupyter notebook module for [Vega 3](https://github.com/vega/vega), and [Vega-Lite 2](https://github.com/vega/vega-lite). Notebooks with embedded visualizations can be viewed on [GitHub](https://github.com/vega/ipyvega/blob/vega3/notebooks/VegaLite.ipynb) and [nbviewer](https://nbviewer.jupyter.org/github/vega/ipyvega/blob/vega3/notebooks/VegaLite.ipynb).

Available on [pypi](https://pypi.python.org/pypi/vega3).

![screenshot](https://raw.githubusercontent.com/vega/ipyvega/vega3/screenshot.png "Screenshot of the Vega-Lite module")


## Install and run

### Python Package Index

To install ``vega`` and its dependencies from the Python Package Index using
``pip``, use the following commands:

```sh
pip install jupyter pandas vega3
pip install --upgrade notebook  # need jupyter_client >= 4.2 for sys-prefix below
jupyter nbextension install --sys-prefix --py vega3  # not needed in notebook >= 5.3
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
See the example notebooks for [Vega-Lite](https://github.com/vega/ipyvega/blob/vega3/notebooks/VegaLite.ipynb) and [Vega](https://github.com/vega/ipyvega/blob/vega3/notebooks/Vega.ipynb).

To run the notebooks yourself, you need to get the file [`cars.json`](https://raw.githubusercontent.com/vega/ipyvega/vega3/notebooks/cars.json).


## Developers

Install requirements: `pip install -r requirements.txt`

Symlink files instead of copying files:

```sh
python setup.py develop
jupyter nbextension install --py --symlink vega3  # not needed in notebook >= 5.3
```

Run kernel: `jupyter notebook`

To rebuild the javascript continuously, run `yarn watch`.

Publish a new version to pypi with `python3 setup.py sdist upload`.

### How to make a release

* Update the javascript dependendencies by changing `package.json`
* Run `yarn`
* Rebuild the javascript with `yarn build`
* Make sure that everything still works (launch notebook and try the examples)
* Update the version number in `package.json` and `__index__.py`
* `git push`
* Run `python setup.py sdist upload` to update https://pypi.python.org/pypi/vega3
