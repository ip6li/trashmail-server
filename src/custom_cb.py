# -*- coding: utf-8 -*-

from logger import Logger
from pymongo import errors


def retry(num_tries, exceptions):

    def decorator(func):

        def f_retry(*args, **kwargs):
            for i in range(num_tries):
                try:
                    return func(*args, **kwargs)
                except exceptions as err:
                    log = Logger(__name__)
                    log.warn("Connection failure [retry " + str(i) + "]: " + str(err))
                    continue
            raise IOError("cannot connect MongoDB after " + str(num_tries) + " tries.")

        return f_retry

    return decorator


retry_auto_reconnect = retry(3, (errors.ConnectionFailure,))
