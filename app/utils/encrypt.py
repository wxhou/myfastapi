from time import time
from random import randint


def make_code_sn(obj_id):
    """生成唯一sn码"""
    left_str = round(time() * 1000)
    right_str = randint(1, 1000)
    return "%d%.5d%.3d" % (left_str, obj_id, right_str)