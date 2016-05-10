# IPython Vega [![PyPI](https://img.shields.io/pypi/v/vega.svg?maxAge=2592000)]()

IPython/Jupyter notebook module for [Vega](https://github.com/vega/vega-lite), and [Vega-Lite](https://github.com/vega/vega-lite), [Polestar](https://github.com/vega/polestar), and [Voyager](https://github.com/vega/voyager).

Available on [pypi](https://pypi.python.org/pypi/vega).

![screenshot](https://raw.githubusercontent.com/vega/ipyvega/master/screenshot.png "Screenshot of the Vega-Lite module")


## Install

```sh
python setup.py install
jupyter nbextension install --py vega
jupyter nbextension enable --py vega
```

## Usage

```
%load_ext vega.disable_autoscroll
```

```py
import pandas as pd
df = pd.read_json('data/cars.json')

from vega import vegalite
vegalite.view(df, {
  "mark": "point",
  "encoding": {
    "y": {"type": "quantitative","field": "Acceleration"},
    "x": {"type": "quantitative","field": "Horsepower"}
  }
})
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

To rebuild the javascript continuously, run `npm run watch`.

Publish a new version to pypi with `python3 setup.py sdist upload`.


## Resources

How to implement an nbextension.

* https://github.com/ipython-contrib/IPython-notebook-extensions/blob/master/nbextensions/styling/table_beautifier/main.js
* https://ipywidgets.readthedocs.org/en/latest/index.html
* https://github.com/jovyan/pythreejs
