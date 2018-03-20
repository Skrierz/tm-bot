chat_id = None
route = None
values = []


def collector(*args):
    for arg in args:
        values.append(arg)
    return values
