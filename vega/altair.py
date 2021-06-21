# Functions to work with Altair

from toolz import curried

import pandas as pd
import altair as alt

from .dataframes.pandas_adapter import PandasAdapter


@curried.curry
def to_streaming(data, widget=None):
    if not isinstance(data, pd.DataFrame):
        raise TypeError(f"Expected DataFrame got: {type(data)}")
    if hasattr(data, "__geo_interface__"):
        raise TypeError("Unhandled __geo_interface__ for now")
    if widget is not None:
        widget._df = PandasAdapter(data)
    return {"name": "data"}


alt.data_transformers.register('streaming', to_streaming)
