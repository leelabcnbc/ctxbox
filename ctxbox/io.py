"""module for converting back and forth cortex files."""

from struct import unpack, pack
import numpy as np

_header_format = '<10s4H'


def _check_ctx_header(width, height, nframe_m_1, depth=8):
    assert depth == 8, 'depth must be 8 bits'
    assert width >= 1 and height >= 1
    assert nframe_m_1 == 0 or nframe_m_1 >= 2


def loadcx(bytes_or_filename, return_notes=False, keep_dims=False):
    """load cortex file.

    Parameters
    ----------
    keep_dims: bool
        keep frame number when there's only one frame.
    return_notes: bool
        whether return the notes as second argument. default to false.
    bytes_or_filename: bytes or str
        all the bytes of a valid CTX file or the path of it.

    Returns
    -------
    a uint8 2d or 3d array, value from 128 to 255
    optionally, it can return a tuple, with second element being the notes
    """
    # get the bytes
    bytes_header = 18
    if not isinstance(bytes_or_filename, bytes):
        assert isinstance(bytes_or_filename, str)
        with open(bytes_or_filename, mode='rb') as f:
            bytes_or_filename = f.read()
    assert len(bytes_or_filename) >= bytes_header, 'at least 18 bytes in the file!'

    # get header and decode notes.
    notes, depth, width, height, nframe_m_1 = unpack(_header_format, bytes_or_filename[:18])
    notes = notes.decode().rstrip('\x00')  # strip off NULL chars.

    _check_ctx_header(width, height, nframe_m_1, depth)

    nframe = nframe_m_1 + 1
    bytes_per_frame = (bytes_header + width * height)
    total_bytes = nframe * bytes_per_frame
    total_bytes_actual = len(bytes_or_filename)
    assert total_bytes_actual == total_bytes, 'size should be {} bytes, but is {}'.format(total_bytes,
                                                                                          total_bytes_actual)

    result = []
    for start_idx in range(0, total_bytes_actual, bytes_per_frame):
        buffer_this = bytes_or_filename[(start_idx + bytes_header):(start_idx + bytes_per_frame)]
        result.append(np.frombuffer(buffer_this, dtype=np.uint8).reshape(height, width))
    result = np.array(result)
    assert result.shape == (nframe, height, width)
    if nframe == 1 and not keep_dims:
        result = result[0]
    if return_notes:
        return result, notes
    else:
        return result


def savecx(frames, filename=None, notes=''):
    """save CTX file to a bytes or to a file

    Parameters
    ----------
    frames: np.ndarray
        a 2 or 3-D array. will be converted to np.float64 and then rounded.
        must have range between 128 - 255 after rounding.
    filename: str
    notes: str
        notes. will be truncated to at most 10 characters.

    Returns
    -------
    None if `filename` is not None, and a bytes if it's None.

    """
    assert frames.ndim == 3 or frames.ndim == 2
    if frames.ndim == 2:
        frames = frames[np.newaxis, :, :]
    frames = frames.astype(np.float64).round()
    assert np.all(frames >= 128) and np.all(frames <= 255), 'invalid data range!'
    frames = frames.astype(np.uint8)
    nframe, height, width = frames.shape
    _check_ctx_header(width, height, nframe - 1)
    depth = 8
    header_normal = pack(_header_format, notes.encode(), depth, width, height, nframe - 1)
    header_suc = pack(_header_format, notes.encode(), depth, width, height, 0)

    result = bytes()
    for idx, data in frames:
        if idx == 0:
            result += header_normal
        else:
            result += header_suc
        result += data.tobytes('C')

    if filename is None:
        return result
    else:
        with open(filename, 'wb') as f:
            f.write(result)
