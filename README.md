# IPython Vega [![PyPI](https://img.shields.io/pypi/v/vega.svg?maxAge=2592000)]()

IPython/Jupyter notebook module for [Vega](https://github.com/vega/vega-lite), and [Vega-Lite](https://github.com/vega/vega-lite), [Polestar](https://github.com/vega/polestar), and [Voyager](https://github.com/vega/voyager). Notebooks with embedded visualizations can be viewed on github and nbviewer.

Available on [pypi](https://pypi.python.org/pypi/vega).

![screenshot](https://raw.githubusercontent.com/vega/ipyvega/master/screenshot.png "Screenshot of the Vega-Lite module")


## Install and run

```sh
pip install jupyter pandas vega
jupyter nbextension install --py vega
jupyter notebook
```

Now Jupyter should be running and you can create a notebook.


## Usage

Check out the example notebooks for [Vega-Lite](https://github.com/vega/ipyvega/blob/master/notebooks/VegaLite.ipynb) and [Vega](https://github.com/vega/ipyvega/blob/master/notebooks/Vega.ipynb).

To run the notebooks yourself, you need to get the file [`cars.json`](https://raw.githubusercontent.com/vega/ipyvega/master/notebooks/cars.json).


## Developers

Install requirements: `pip install -r requirements.txt`

Symlink files instead of copying files:

```sh
python setup.py develop
jupyter nbextension install --py --symlink vega
```

Run kernel: `jypyter notebook`

To rebuild the javascript continuously, run `npm run watch`.

Publish a new version to pypi with `python3 setup.py sdist upload`.


## Resources

How to implement an nbextension.

* https://github.com/ipython-contrib/IPython-notebook-extensions/blob/master/nbextensions/styling/table_beautifier/main.js
* https://ipywidgets.readthedocs.org/en/latest/index.html
* https://github.com/jovyan/pythreejs
