def to_bytes(bytes_or_str):
    """
    Converts supplied data into bytes if the data is of type str.
    :param bytes_or_str: Data to be converted.
    :return: UTF-8 encoded bytes if the data was of type str. Otherwise it returns the supplied data as is.
    """
    if isinstance(bytes_or_str, str):
        return bytes_or_str.encode()
    return bytes_or_str


def to_str(bytes_or_str):
    """
    Converts supplied data into a UTF-8 encoded string if the data is of type bytes.
    :param bytes_or_str: Data to be converted.
    :return: UTF-8 encoded string if the data was of type bytes.  Otherwise it returns the supplied data as is.
    """
    if isinstance(bytes_or_str, bytes):
        return bytes_or_str.decode()
    return bytes_or_str
