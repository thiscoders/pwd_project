# -*- coding: utf-8 -*-


def deco_time(func):
    def inner(*args, **kw):
        print('what')
        return func(*args, **kw)

    return inner


@deco_time
def mnow():
    print('hello')


mnow()
