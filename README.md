# IPython Vega
[![PyPI](https://img.shields.io/pypi/v/vega.svg)](https://pypi.python.org/pypi/vega)
[![npm version](https://img.shields.io/npm/v/jupyter-vega.svg)](https://www.npmjs.com/package/jupyter-vega)
[![Build Status](https://github.com/vega/ipyvega/workflows/Test/badge.svg)](https://github.com/vega/ipyvega/actions)

IPython/Jupyter notebook module for [Vega 5](https://github.com/vega/vega), and [Vega-Lite 4](https://github.com/vega/vega-lite). Notebooks with embedded visualizations can be viewed on [GitHub](https://github.com/vega/ipyvega/blob/master/notebooks/VegaLite.ipynb) and [nbviewer](https://nbviewer.jupyter.org/github/vega/ipyvega/blob/master/notebooks/VegaLite.ipynb). If you use JupyterLab (not the notebook), you don't need to install this extension since JupyterLab comes with built-in support for Vega and Vega-Lite.

Available on [pypi](https://pypi.python.org/pypi/vega) and [Conda Forge](https://anaconda.org/conda-forge/vega) as `vega`.

<img src="screenshot.png" width="500">

## Install and run

### Python Package Index

To install `vega` and its dependencies from the Python Package Index using
`pip`, use the following commands:

```sh
pip install jupyter pandas vega
pip install --upgrade notebook  # need jupyter_client >= 4.2 for sys-prefix below
jupyter nbextension install --sys-prefix --py vega
jupyter nbextension enable --py --sys-prefix vega
```

### Conda Forge

If you use Conda, you probably already have the latest versions of the notebook and pandas installed. To install `vega` extension run:

```sh
conda install vega
```

## Usage

Once the package is installed, run
```sh
jupyter notebook
```
to launch the Jupyter notebook server, and use `vega` within the notebook.
See the example notebooks for [Vega-Lite](https://github.com/vega/ipyvega/blob/master/notebooks/VegaLite.ipynb) and [Vega](https://github.com/vega/ipyvega/blob/master/notebooks/Vega.ipynb).

To run the notebooks yourself, you need to get the file [`cars.json`](https://raw.githubusercontent.com/vega/ipyvega/master/notebooks/cars.json).


## Developers

This project uses [Poetry](https://python-poetry.org/). If you prefer a local virtual environment, run `poetry config virtualenvs.in-project true` first. Install requirements: `poetry install`.

Then activate the virtual environment with `poetry shell`.

Symlink files instead of copying files:

```sh
jupyter nbextension install --py --symlink --sys-prefix vega
jupyter nbextension enable --py --sys-prefix vega
```

Run kernel with `jupyter notebook`. Run the tests with `pytest vega`.

To rebuild the JavaScript continuously, run `yarn watch`.

### How to make a release

* Update the JavaScript dependencies by changing `package.json` (e.g. with [ncu](https://www.npmjs.com/package/npm-check-updates)).
* Run `yarn`.
* Update the version number in `pyproject.toml` (with `poetry version [VERSION]`), `package.json`, `widget.py`, and `__init__.py`
* Rebuild the JavaScript with `yarn build`.
* Make sure that everything still works (launch notebook and widgets and try the examples).
* Add a git tag.
* `git push --tags`.
* Run `npm publish` to update https://www.npmjs.com/package/jupyter-vega.
* Then run `poetry publish --build` to update https://pypi.python.org/pypi/vega.

The Conda feedstock for this package is at https://github.com/conda-forge/vega-feedstock. It should update automatically but we may need to merge a pull request with the updates. 

### Visual Regression Tests

ipyvega uses the same technical solution as [ipywidgets](https://github.com/jupyter-widgets/ipywidgets) for visual regression testing (i.e. [Galata](https://github.com/jupyterlab/jupyterlab/tree/master/galata)).

Therefore, the instructions provided for [ipywidgets visual regression tests](https://ipywidgets.readthedocs.io/en/stable/dev_testing.html#visual-regression-tests) apply here.

Currently:

* ipyvega uses `ui-tests/tests/notebooks/vega.ipynb` notebook for testing
* reference images are in the `ui-tests/tests/vega.test.ts-snapshots/` directory.
