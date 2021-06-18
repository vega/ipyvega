from traitlets import Undefined
from traittypes import SciType
from . import SourceAdapter

class TableType(SciType):

    """
    A SourceAdapter instance trait type.
    """

    info_text = 'a sourceAdapter instance trait type'

    klass = SourceAdapter

    def validate(self, obj, value):
        if value is None or value is Undefined:
            return super().validate(obj, value)
        #if not isinstance(default_value, self.klass):
        #    self.error(obj, value)
        return super().validate(obj, value)

    def set(self, obj, value):
        #print("@set", obj, value)
        new_value = self._validate(obj, value)
        old_value = obj._trait_values.get(self.name, self.default_value)
        obj._trait_values[self.name] = new_value
        if ((old_value is None and new_value is not None) or
                (old_value is Undefined and new_value is not Undefined) or
                not old_value.equals(new_value)):
            obj._notify_trait(self.name, old_value, new_value)

    def __init__(self, default_value=Undefined, **kwargs):
        if default_value is not None and default_value is not Undefined:
            assert isinstance(default_value, self.klass)
        super().__init__(default_value=default_value, **kwargs)

