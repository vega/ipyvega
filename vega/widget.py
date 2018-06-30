import json

from ipywidgets import DOMWidget
from traitlets import Unicode, Dict

__all__ = ['VegaWidget']


class VegaWidget(DOMWidget):
    """An IPython widget display a vega chart.

    Specifying the spec directly::

        widget = VegaWidget({...})
        widget.update(remove='datum.t < 5', insert=[{...}, {...}])

    Usage with ``altair``::

        widget = VegaWidget.from_cart(chart)

    The chart can be updated by setting the spec properties. Changing keys
    of the spec will not be reflected.

    For streaming data, setting the whole spec may be imperformant. For this
    use case, ``VegaWidget`` offers the ``update`` method. It sends the data
    to the client without persisting it on the Python side.
    """
    _view_name = Unicode('VegaWidget').tag(sync=True)
    _view_module = Unicode('nbextensions/jupyter-vega/index').tag(sync=True)
    _view_module_version = Unicode('0.1.0').tag(sync=True)
    _spec_source = Unicode('null').tag(sync=True)

    @classmethod
    def from_chart(cls, chart):
        return cls(spec=chart.to_dict())

    def __init__(self, spec=None, **kwargs):
        super().__init__(**kwargs)
        self._spec_source = json.dumps(spec)

    @property
    def spec(self):
        return json.loads(self._spec_source)

    @spec.setter
    def spec(self, value):
        self._spec_source = json.dumps(value)

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
        data = dict(type='update', key=key)

        if remove is not None:
            data['remove'] = remove

        if insert is not None:
            data['insert'] = insert

        self.send(data)
