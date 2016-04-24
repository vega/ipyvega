# ipython-vega

IPython/Jupyter notebook module for [Vega](/vega/vega-lite), and [Vega-Lite](/vega/vega-lite), [Polestar](/vega/polestar), and [Voyager](/vega/voyager).

## Install

```sh
python setup.py install
jupyter nbextension install --py vega
jupyter nbextension enable --py vega
```

## Developers

Install requirements: `pip install -r requirements.txt`

Symlink files instead of copying files:

```sh
python setup.py develop
jupyter nbextension install --py --symlink vega
jupyter nbextension enable --py vega
```

Run kernel: `jypyter notebook`

### TODO

If you want to help with one of these, or have questions, comment on the corresponding issue.

* Add export functionality to polestar so that a visualization can be saved in a new cell [#3](/vega/ipython-vega/issues/3)
* Save state of voyager and polestar [#19](/vega/ipython-vega/issues/19)

## Resources

https://github.com/ipython-contrib/IPython-notebook-extensions/blob/master/nbextensions/styling/table_beautifier/main.js
https://ipywidgets.readthedocs.org/en/latest/index.html
