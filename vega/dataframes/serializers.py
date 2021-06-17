import numpy as np
import lz4.frame
import json
from .. import SourceAdapter


def array_to_json(value):
    """
    numpy to JSON serializer.
    """
    assert isinstance(value, np.ndarray)
    if value.dtype.name in ('int64', 'uint64'):
        value = value.astype('uint32' if value.dtype.kind=='u' else 'int32', order='C')
    elif not value.flags['C_CONTIGUOUS'] and(np.issubsctype(value.dtype, np.integer) or
                                             np.issubsctype(value.dtype, np.floating)):
        value = np.ascontiguousarray(value)
    elif np.issubsctype(value.dtype, str):
        value = value.tolist()
    elif np.issubsctype(value.dtype, object):
        value = value.astype('str').tolist()
    #else:
    #    import pdb;pdb.set_trace()
    #    raise ValueError(f"Not implemented dtype {value.dtype}")
    if isinstance(value, list):
        return {
            'shape': (len(value),),
            'dtype': 'str',
            'buffer': value
        }
    return {
        'shape': value.shape,
        'dtype': str(value.dtype),
        'buffer': memoryview(value)
    }


def col_to_json(value, compression):
    assert isinstance(value, np.ndarray)
    json_ = array_to_json(value)
    if compression is None:
        return json_
    arr = json_.get('buffer')
    if value.dtype == object or value.dtype == str:
        arr = json.dumps(arr).encode()
    json_['buffer'] = compression.compress(arr)
    json_['compression'] = compression.name
    return json_

def table_to_json(value, widget):
    if value is None:
        return None
    _ = widget
    assert isinstance(value, SourceAdapter)
    compression = value._compression or widget.compression
    if isinstance(compression, dict): # column specific compressors
        data = {cn: col_to_json(value.to_array(cn),
                                compression[cn])
                for cn in value.columns}
    else:
        # unique compression for all columns
        data = {cn: col_to_json(value.to_array(cn),
                                compression) for cn in value.columns}
    return dict(columns=list(value.columns), data=data)

def table_from_json(value, widget):
    return {} # not yet implemented

serialization = dict(to_json=table_to_json,
                     from_json=table_from_json)
