# ipython-vega

IPython/Jupyter notebook module for [Vega](/vega/vega-lite), and [Vega-Lite](/vega/vega-lite), [Polestar](/vega/polestar), and [Voyager](/vega/voyager).

![screenshot](https://raw.githubusercontent.com/vega/ipython-vega/rewrite/screenshot.png "Screenshot of the Vega-Lite module")


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


## Resources

https://github.com/ipython-contrib/IPython-notebook-extensions/blob/master/nbextensions/styling/table_beautifier/main.js
https://ipywidgets.readthedocs.org/en/latest/index.html
