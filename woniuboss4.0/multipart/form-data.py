# 编码
import binascii
import json
import os
import random

def encode_multipart_formdata(fields):
    boundary = binascii.hexlify("肉".encode("utf-8"))
    # binascii.b2a_hex(a.encode())

    body = (
        "".join("--%s\r\n"
                "Content-Dosposition: form-data; name=\"%s\"\r\n"
                "\r\n"
                "%s\r\n" % (boundary, field, value)
                for field, value in fields.items()) +
        "--%s--\r\n" % boundary

        )
    content_type = "multipart/form-data; boundary=%s" % boundary

    return body, content_type
encode_multipart_formdata({"foo":""})