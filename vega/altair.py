# Functions to stream Altair specifications

import warnings
import pkgutil

from pprint import pprint
from toolz import curried

from IPython.display import display

import pandas as pd
import altair as alt

from .widget import VegaWidget


def _exceptions(exceptions):
    if exceptions is None:
        exceptions = {}
    elif isinstance(exceptions, list):
        exceptions = set([id(exc) if isinstance(exc, pd.DataFrame) else exc
                          for exc in exceptions])
    return exceptions


@curried.curry
def to_streaming(data, context=None, exceptions=None, debug=False):
    id_ = id(data)
    if debug:
        print('to_streaming '+str(id_))
    exceptions = _exceptions(exceptions)
    if not isinstance(data, pd.DataFrame):
        raise TypeError(f"Expected DataFrame got: {type(data)}")
    if hasattr(data, "__geo_interface__"):
        # raise TypeError("Unhandled __geo_interface__ for now")
        warnings.warn("Unhandled __geo_interface__, not streaming")
        return alt.to_values(data)
    if id_ in exceptions:
        if debug:
            print('Exception for', id_)
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


def stream(alt_spec, exceptions=None, reuse=False, resize=True, debug=False):
    """
    Send an Altair specification to the notebook using the streaming API

    Parameters
    ----------
    alt_spect : top-level chart object such as Chart or LayeredChart
        the Altair specification
    exceptions : list
        a list of dataframes of id(dataframe) that should be inlined
    reuse : boolean
        if True, return the context dictionary and the widget. The
        context dictionary associate a dataframe id with a pair
        (name, data). The name is useful to reuse the widget for
        streaming more data using the widget `.update` method.
    resize: boolean
        Resize vega component after sending the update. Some charts
        need it, others don't. Defaults to True but can be overridden
        here.
    debug: boolean
        if True, prints debugging information
    """
    context = {}
    with alt.data_transformers.enable('streaming',
                                      context=context,
                                      exceptions=exceptions,
                                      debug=debug):
        vw = VegaWidget(alt_spec.to_dict())
        display(vw)
        for id_, name_data in context.items():
            name, data = name_data
            vw.update(name, remove='true', insert=data)
    if reuse:
        return context, vw


def test_altair(names=None):
    import time
    try:
        from altair_examples import iter_examples, exec_example
    except:
        return

    errors = {}
    results = {}
    if names and not isinstance(names, list):
        names = [names]
        print('testing ', names)
    for example in iter_examples():
        name = example['name']
        if names and name not in names:
            continue
        print(name)
        start = time.process_time_ns()
        chart = exec_example(example)
        if chart is None:
            print('Error for', example['name'])
            errors[name] = 'No value returned by '+example['name']
        try:
            mid = time.process_time_ns()
            try:
                stream(chart)
                # vw = VegaWidget(chart.to_dict())
                # display(vw)
            except Exception as exc:
                errors[name] = str(exc) + errors.get(name, "")
            results[name] = (mid - start,
                             time.process_time_ns() - mid)
        except Exception as exc:
            print('Error', exc)
            errors[name] = str(exc) + errors.get(name, "")
    if errors:
        pprint(errors)
    pprint(results)
