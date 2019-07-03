from __future__ import print_function

import contextlib
import json
import uuid
import sys

try:
    from ipywidgets import DOMWidget
    from traitlets import Unicode, Dict

except ImportError as err:
    new_err = ImportError(
        "vega.widget requires ipywidgets, which could not be imported. "
        "Is ipywidgets installed?"
    )

    # perform manual exception chaining for python 2 compat
    new_err.__cause__ = err
    raise new_err


__all__ = ['VegaWidget']


class VegaWidget(DOMWidget):
    """An IPython widget display a vega chart.

    Specifying the spec directly::

        widget = VegaWidget({...})
        widget.update(remove='datum.t < 5', insert=[{...}, {...}])

    To modify the created plot, additional options can be passed as in::

        widget = VegaWidget(spec, opt)

    Usage with ``altair``::

        widget = VegaWidget(chart.to_dict())

    To select between vega and vega-lite use the ``$schema`` property on
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
    _view_module = Unicode('nbextensions/jupyter-vega/widget').tag(sync=True)
    _view_module_version = Unicode('0.1.0').tag(sync=True)
    _spec_source = Unicode('null').tag(sync=True)
    _opt_source = Unicode('null').tag(sync=True)

    def __init__(self, spec=None, opt=None, **kwargs):
        super().__init__(**kwargs)
        self._spec_source = json.dumps(spec)
        self._opt_source = json.dumps(opt)

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

        self.send(dict(type="update", updates=self._pending_updates))
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

    def update(self, key, remove=None, insert=None):
        """Update the chart data.

        Updates are only reflected on the client, i.e., after re-displaying
        the widget will show the chart specified in its spec property.

        :param Optional[str] remove:
            a JavaScript expression of items to remove. The item to test can
            be accessed as ``datum``. For example, the call
            ``update(remove="datum.t < 5")`` removes all items with the
            property ``t < 5``.

        :param Optional[List[dict]] insert:
            new items to add to the chat data.
        """
        update = dict(key=key)

        if remove is not None:
            update['remove'] = remove

        if insert is not None:
            update['insert'] = insert

        if self._displayed:
            self.send(dict(type="update", updates=[update]))

        else:
            self._pending_updates.append(update)

