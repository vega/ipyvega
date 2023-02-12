"""
Functions to stream Altair specifications
"""

import warnings
import logging

from toolz import curried

from IPython.display import display

import pandas as pd
import altair as alt

from .widget import VegaWidget

logger = logging.getLogger(__name__)


def _exceptions(exceptions):
    if exceptions is None:
        exceptions = {}
    elif isinstance(exceptions, list):
        exceptions = {id(exc) if isinstance(exc, pd.DataFrame) else exc
                      for exc in exceptions}
    return exceptions


@curried.curry
def to_streaming(data, context=None, exceptions=None):
    id_ = id(data)
    logger.debug("to_streaming %s", id_)
    exceptions = _exceptions(exceptions)
    if not isinstance(data, pd.DataFrame):
        raise TypeError(f"Expected DataFrame got: {type(data)}")
    if hasattr(data, "__geo_interface__"):
        warnings.warn("Unhandled __geo_interface__, not streaming")
        return alt.to_values(data)
    if id_ in exceptions:
        logger.debug("Exception for %s", id_)
        return alt.to_values(data)
    if isinstance(context, dict):
        name = context.get(id_, None)
        if name is None:
            if len(context) == 0:
                name = "data"
            else:
                name = f"data-{len(context)+1}"
            context[id_] = (name, data)
        else:
            name = name[0]
    else:
        name = "data"
    return {"name": name}


alt.data_transformers.register('streaming', to_streaming)


def stream(alt_spec, exceptions=None, resize=False, reuse=False):
    """
    Send an Altair specification to the notebook using the streaming API

    Parameters
    ----------
    alt_spec : top-level chart object such as Chart or LayeredChart
        the Altair specification
    exceptions : list
        a list of dataframes of id(dataframe) that should be inlined.
        A small dataframe does not benefit from the streaming API.
        A geopandas dataframe is also not compressed anyway. If you send
        one of these, you can put them in the exception list to save
        some cycles.
    reuse : boolean
        if True, return the context dictionary and the widget. The
        context dictionary associate a dataframe id with a pair
        (name, data). The name is useful to reuse the widget for
        streaming more data using the widget `.update` method.
    resize: boolean
        Resize vega component after sending the update. Some charts
        need it, others don't. Defaults to True but can be overridden
        here.
    reuse: boolean
        Return the context and widget if True, None otherwise.
        The context and widget are useful to stream multiple times
        to the same widget. If the `stream` function is used to speed
        up the dataset transfer once and for all (the default),
        there is no need to return the context and widget. It would
        leave a useless value in a notebook cell.

    Returns
    -------
    If the `reuse` parameter is False, return None. Otherwise, return
    a pair containing:
    The context, a dictionary updated by alt.data_transformers.enable,
    and the VegaWidget created to display the alt_spec, to be able to
    update it later.
    """
    context = {}
    with alt.data_transformers.enable('streaming',
                                      context=context,
                                      exceptions=exceptions):
        widget = VegaWidget(alt_spec.to_dict())
        display(widget)
        for name_data in context.values():
            name, data = name_data
            widget.update(name, remove='true', insert=data, resize=resize)
    if reuse:
        return context, widget
    return None
