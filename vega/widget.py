from __future__ import print_function

import json
import pandas as pd
from ._frontend import module_name, EXTENSION_SPEC_VERSION

# from ipytablewidgets.compressors import *
from ipytablewidgets import (serialization,
                             SourceAdapter,
                             PandasAdapter,
                             NumpyAdapter, TableType)

import numpy as np
try:
    import ipywidgets
    from traitlets import Unicode

except ImportError as err:
    new_err = ImportError(
        "vega.widget requires ipywidgets, which could not be imported. "
        "Is ipywidgets installed?"
    )

    # perform manual exception chaining for python 2 compat
    new_err.__cause__ = err
    raise new_err


__all__ = ['VegaWidget']


@ipywidgets.register
class VegaWidget(ipywidgets.DOMWidget):
    """An IPython widget display a Vega chart.

    Specifying the spec directly::

        widget = VegaWidget({...})
        widget.update(remove='datum.t < 5', insert=[{...}, {...}])

    To modify the created plot, additional options can be passed as in::

        widget = VegaWidget(spec, opt)

    Usage with ``altair``::

        widget = VegaWidget(chart.to_dict())

    To select between Vega and Vega-Lite use the ``$schema`` property on
    the ``spec`` dictionary.

    The chart can be updated by setting the ``spec`` property. In additon
    embedding options, such as the used theme, can be set via the ``opt``
    property::

        widget.spec = {...}
        widget.opt = {"theme": "dark"}

    For streaming data, setting the whole spec may be slow. For this use case,
    ``VegaWidget`` offers the ``update`` method. It sends the data to the
    client without persisting it on the Python side. In particular resetting
    the ``spec`` and ``opt`` properties will lose any data changes performed
    via ``update``.
    """
    # Implementation note: there is a small delay between defining the widget
    # and its display in the frontend. Any message sent during this time
    # interval will be silently ignored by the client. To ensure all updates
    # are handled, they are buffered on the python side until the widget is
    # first displayed. The buffer is the `_pending_updates` attribute and the
    # display state is reflected by the `_displayed` attribute.

    _view_name = Unicode('VegaWidget').tag(sync=True)
    _model_name = Unicode('VegaWidgetModel').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(EXTENSION_SPEC_VERSION).tag(sync=True)
    _model_module_version = Unicode(EXTENSION_SPEC_VERSION).tag(sync=True)
    _spec_source = Unicode('null').tag(sync=True)
    _opt_source = Unicode('null').tag(sync=True)
    compression = None
    _df = TableType(None).tag(sync=True, **serialization)
    _img_url = Unicode('null').tag(sync=True)

    def __init__(self, spec=None, opt=None, **kwargs):
        super().__init__(**kwargs)
        self._spec_source = json.dumps(spec)
        self._opt_source = json.dumps(opt)
        self._img_url = "null"
        self._resize = True  # only for pending updates
        self._displayed = False
        self._pending_updates = []

        self.on_msg(self._handle_message)

    def _handle_message(self, widget, msg, _):
        if msg['type'] != "display":
            return

        if self._displayed:
            return

        self._displayed = True

        if not self._pending_updates:
            return

        self.send(
            dict(type="update",
                 updates=self._pending_updates,
                 resize=self._resize)
        )
        self._pending_updates = []

    def _reset(self):
        self._displayed = False
        self._pending_updates = []

    @property
    def spec(self):
        return json.loads(self._spec_source)

    @spec.setter
    def spec(self, value):
        self._spec_source = json.dumps(value)
        self._reset()

    @property
    def opt(self):
        return json.loads(self._opt_source)

    @opt.setter
    def opt(self, value):
        self._opt_source = json.dumps(value)
        self._reset()

    def update(self, key, remove=None, insert=None, resize=True):
        """Update the chart data.

        Updates are only reflected on the client, i.e., after re-displaying
        the widget will show the chart specified in its spec property.

        :param str key:
            the name of the dataset to update, as declared in the data
            section of the spec. To update several datasets, chain multiple
            update calls on the widget.

        :param Optional[str] remove:
            a JavaScript expression of items to remove. The item to test can
            be accessed as ``datum``. For example, the call
            ``update(remove="datum.t < 5")`` removes all items with the
            property ``t < 5``.

        :param Optional[List[dict]] insert:
            new items to add to the chart data.

        :param Optional[Bool] resize:
            trigger a resize of the widget after updating. This is
            required when the update creates or deletes important marks
            in the visualization, i.e. creating a new bar in a bar chart.
        """
        if isinstance(insert, (np.ndarray, NumpyAdapter)):
            return self.update_array2d(key, arr=insert,
                                       columns=['x', 'y', 'z'],
                                       remove=remove,
                                       resize=resize)
        if isinstance(insert, (pd.DataFrame, SourceAdapter)):
            return self.update_dataframe(key, df=insert, remove=remove,
                                         resize=resize)
        update = dict(key=key)

        if remove is not None:
            update['remove'] = remove

        if insert is not None:
            update['insert'] = insert

        if self._displayed:
            self.send(dict(type="update", updates=[update], resize=resize))

        else:
            self._resize = resize
            self._pending_updates.append(update)

    def update_dataframe(self, key, df, remove=None, resize=True):
        """Update the chart data with a DataFrame.

        Updates are only reflected on the client, i.e., after re-displaying
        the widget will show the chart specified in its spec property.

        :param str key:
            the name of the dataset to update, as declared in the data
            section of the spec.

        :param pd.DataFrame df:
            new items to add to the chart data.

        :param Optional[str] remove:
            a JavaScript expression of items to remove. The item to test can
            be accessed as ``datum``. For example, the call
            ``update(remove="datum.t < 5")`` removes all items with the
            property ``t < 5``.

        :param Optional[Bool] resize:
            trigger a resize of the widget after updating.
        """
        if isinstance(df, pd.DataFrame):
            self._df = PandasAdapter(df, touch_mode=True)
        else:
            assert isinstance(df, SourceAdapter)
            self._df = df
        self._df.touch()
        update = dict(key=key)
        if remove is not None:
            update['remove'] = remove
        update['insert'] = "@dataframe"
        self.send(dict(type="update", updates=[update], resize=resize))

    def update_array2d(self, key, arr, columns, remove=None, resize=True):
        """Update the chart data with a 2d array and their column names.

        Updates are only reflected on the client, i.e., after re-displaying
        the widget will show the chart specified in its spec property.

        :param str key:
            the name of the dataset to update, as declared in the data
            section of the spec.

        :param np.ndarray arr:
            new items to add to the chart data as a 2d numpy array.

        :param List[str] columns:
            list of column names for each column of the array.

        :param Optional[str] remove:
            a JavaScript expression of items to remove. The item to test can
            be accessed as ``datum``. For example, the call
            ``update(remove="datum.t < 5")`` removes all items with the
            property ``t < 5``.

        :param Optional[Bool] resize:
            trigger a resize of the widget after updating.

        NB: the array will be wrapped as a one column Table.
        The unique column (fancy_col below) is built as a comma separated
        coords string (i.e. columns param.)
        This naming covention is important because JavaScript will split
        this string to obtain the three names for the x, y, z coords.
        """
        if isinstance(arr, np.ndarray):
            fancy_col = ','.join(columns)
            self._df = NumpyAdapter({fancy_col: arr}, touch_mode=True)
        else:
            assert isinstance(arr, SourceAdapter)
            self._df = arr
        self._df.touch()
        update = dict(key=key)
        if remove is not None:
            update['remove'] = remove
        update['insert'] = "@array2d"
        self.send(dict(type="update", updates=[update], resize=resize))
