import json
import os
import copy

import numpy as np
import pandas as pd

import pytest

from ..utils import sanitize_dataframe, nested_update, prepare_spec

PANDAS_DATA = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
JSON_DATA = {
    "values": [
        {"x": 1, "y": 4},
        {"x": 2, "y": 5},
        {"x": 3, "y": 6}
    ]
}

VEGALITE_SPEC = {
    "mark": "circle",
    "encoding": {
        "x": {"field": "x", "type": "quantitative"},
        "y": {"field": "y", "type": "quantitative"}
    }
}


def test_nested_update():
    D = {'A': {'a': 4, 'b': 5}}
    U = {'A': {'a': 40, 'c': 6}, 'B': {'foo': 'bar'}}
    output = nested_update(D, U)
    assert output is D
    assert D == {'A': {'a': 40, 'b': 5, 'c': 6}, 'B': {'foo': 'bar'}}


def test_sanitize_dataframe():
    # create a dataframe with various types
    df = pd.DataFrame({'s': list('abcde'),
                       'f': np.arange(5, dtype=float),
                       'i': np.arange(5, dtype=int),
                       'd': pd.date_range('2012-01-01', periods=5, freq='H'),
                       'c': pd.Series(list('ababc'), dtype='category')})

    # add some nulls
    df.ix[0, 's'] = None
    df.ix[0, 'f'] = np.nan
    df.ix[0, 'd'] = pd.NaT

    # JSON serialize. This will fail on non-sanitized dataframes
    df_clean = sanitize_dataframe(df)
    s = json.dumps(df_clean.to_dict(orient='records'))

    # Re-construct pandas dataframe
    df2 = pd.read_json(s)

    # Re-apply original types
    for col in df:
        if str(df[col].dtype).startswith('datetime'):
            # astype(datetime) introduces time-zone issues:
            # to_datetime() does not.
            df2[col] = pd.to_datetime(df2[col])
        else:
            df2[col] = df2[col].astype(df[col].dtype)

    assert df.equals(df2)


def test_prepare_spec():
    spec1 = copy.deepcopy(VEGALITE_SPEC)
    spec1view = prepare_spec(spec1, PANDAS_DATA)
    assert spec1 is spec1view  # should modify in-place

    spec2 = copy.deepcopy(VEGALITE_SPEC)
    spec2view = prepare_spec(spec2, JSON_DATA['values'])
    assert spec2 is spec2view  # should modify in-place

    spec3 = copy.deepcopy(VEGALITE_SPEC)
    spec3['data'] = JSON_DATA
    spec3view = prepare_spec(spec3)
    assert spec3 is spec3view  # should modify in-place

    # all three approaches should match
    assert spec1 == spec2 == spec3

    # Check for error when no data is provided
    spec4 = copy.deepcopy(VEGALITE_SPEC)
    with pytest.raises(ValueError) as err:
        prepare_spec(spec4)
    assert str(err.value) == 'No data provided'
