#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import base64


def encode_base64(data):
    if isinstance(data, bytes):
        return base64.b64encode(data).decode('utf-8')
    elif isinstance(data, str):
        return base64.b64encode(data.encode('utf-8')).decode('utf-8')


def decode_base64(data):
    return base64.b64decode(data).decode('utf-8')


if __name__ == "__main__":
    text = 'abcabca'
    etext = encode_base64(text)
    dtext = decode_base64(etext)
    print((etext, dtext))
