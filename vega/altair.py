# Functions to stream Altair specifications

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


def stream(alt_spec, exceptions=None, reuse=False, debug=False):
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


def test_altair():
    import ast
    errors = {}
    for ex in alt.examples.iter_examples():
        print(ex['name'])
        with open(ex['filename'], 'r') as fin:
            code = fin.read()
        locs = {}
        root_node = ast.parse(code, ex['filename'], mode='exec')
        last_expr = root_node.body[-1]
        if isinstance(last_expr, ast.Expr):
            last = ast.Assign(targets=[ast.Name(id='result', ctx=ast.Store(),
                                                lineno=0, col_offset=0)],
                              value=last_expr.value,
                              lineno=last_expr.lineno,
                              col_offset=last_expr.col_offset)
            root_node.body[-1] = last
        # print(ast.dump(root_node, indent=4))
        try:
            code = compile(root_node, ex['filename'], mode='exec')
            exec(code, globals(), locs)
            if 'result' in locs:
                stream(locs['result'])
        except Exception as exc:
            print('Error', exc)
            errors[ex['name']] = str(exc)
            pass
    if errors:
        pprint(errors)
