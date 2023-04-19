import os

import qrcode


def qr_generate(data, name):
    qrcode.make(data).save(name)

    with open(name, "rb") as f:
        result = f.read()

    os.remove(name)

    return result