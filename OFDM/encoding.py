import binascii as ba
import numpy as np
import math


def convert_to_hex(input):
    a_code = ba.b2a_hex(input.encode()).decode()
    output = []

    for c in a_code:
        output.append(c)

    return output


def convert_to_text(input):
    return ba.a2b_hex(''.join(input)).decode()


def sampling(info, rate):
    size = len(info)
    t = np.arange(0, size, 1 / rate)

    output = []

    for i in range(len(t)):
        output.append(info[math.floor(t[i])])

    return output


def encoding_16QAM(input):
    symbols_num = len(input)

    _map_ = dict([('0', (3, 3)), ('1', (1, 3)), ('2', (-3, 3)), ('3', (-1, 3)),
                  ('7', (-1, 1)), ('6', (-3, 1)), ('5', (1, 1)), ('4', (3, 1)),
                  ('8', (3, -3)), ('9', (1, -3)), ('a', (-3, -3)), ('b', (-1, -3)),
                  ('f', (-1, -1)), ('e', (-3, -1)), ('d', (1, -1)), ('c', (3, -1))])

    qam_encode_list = []

    for c in input:
        qam_encode_list.append(complex(_map_[c][0], _map_[c][1]))

    return np.array(qam_encode_list)
