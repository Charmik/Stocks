import datetime
import os
import pathlib
import pickle
from typing import AnyStr


class Cache:

    @staticmethod
    def save_obj(obj, file_name: AnyStr):
        with open(file_name, 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load_obj(file_name: AnyStr, ttl_hours: int = 20):
        if not os.path.exists(file_name):
            return None
        if Cache.is_too_old(file_name, ttl_hours):
            return None
        with open(file_name, 'rb') as f:
            return pickle.load(f)

    @staticmethod
    def is_too_old(file_name: AnyStr, ttl_hours: int = 20) -> bool:
        path = pathlib.Path(file_name)
        now = datetime.datetime.now()

        last_modify_time = datetime.datetime.fromtimestamp(path.stat().st_mtime)
        diff_hours = (now - last_modify_time).seconds / 60 / 60

        if diff_hours > ttl_hours:
            os.remove(file_name)
            return True
        else:
            return False
