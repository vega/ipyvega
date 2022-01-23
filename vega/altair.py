# Functions to stream Altair specifications

import time
import warnings

from toolz import curried

from IPython.display import display

import pandas as pd
import altair as alt
from altair import examples
from altair.utils.execeval import eval_block

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
        print(f'to_streaming {id_}')
    exceptions = _exceptions(exceptions)
    if not isinstance(data, pd.DataFrame):
        raise TypeError(f"Expected DataFrame got: {type(data)}")
    if hasattr(data, "__geo_interface__"):
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
        for name_data in context.values():
            name, data = name_data
            vw.update(name, remove='true', insert=data)
    if reuse:
        return context, vw


def _dataframe_from(url):
    from vega_datasets import data
    if not isinstance(url, str):
        return url
    for dname in data.list_datasets():
        ds = getattr(data, dname.replace("-", "_"))
        if ds.url == url:
            return ds()
    return pd.read_csv(url)


def _exec_example(example):
    """Execute an example return by `iter_examples' and returns the chart.

    Parameters
    ----------
    example: dict
        the example dict should contain the key "filename", as returned by
        `iter_examples`
    """
    with open(example["filename"], "r") as fin:
        code = fin.read()
    return eval_block(code, filename=example["filename"])


def stream_examples(names=None):
    errors = {}
    total = 0
    if names:
        if not isinstance(names, list):
            names = [names]
        print('testing ', names)
        names = set(names)

    for example in examples.iter_examples():
        name = example['name']
        if names and name not in names:
            continue
        print(f"Example #{total+1}: {name}")
        chart = _exec_example(example)
        if chart is None:
            print('Error for', example['name'])
            errors[name] = 'No value returned by '+example['name']
        try:
            chart.data = _dataframe_from(chart.data)
            mid = time.process_time_ns()
            try:
                stream(chart)
            except Exception as exc:
                errors[name] = str(exc) + errors.get(name, "")
                print(str(exc) + errors.get(name, ""))
            print("Time:", (time.process_time_ns() - mid)/1000000000.0, "s")
        except Exception as exc:
            print('Error', exc)
            errors[name] = str(exc) + errors.get(name, "")
        total += 1
    print(f"Total number of examples: {total}, "
          f"Sucess: {total-len(errors)}, "
          f"Error(s): {len(errors)}")
    return errors
