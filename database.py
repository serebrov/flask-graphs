data = {}


def get_hash(player, ts):
    return player + '|' + str(ts)


def get_item_hash(item):
    return get_hash(item['player'], item['ts'])


def get(player, ts):
    global data
    return data[get_hash(player, ts)]


def put(item):
    global data
    data[get_item_hash(item)] = item


def delete(item):
    global data
    del data[get_item_hash(item)]


def find_if(if_fn):
    global data
    result = []
    for item_hash in data:
        item = data[item_hash]
        if if_fn(item):
            result.append(item)
    return result


def query(**kwargs):
    global data
    result = []
    for item_hash in data:
        item = data[item_hash]
        if matches(item, **kwargs):
            result.append(item)
    return result


def matches(item, **kwargs):
    for key in kwargs:
        if item[key] != kwargs[key]:
            return False
    return True


def reset():
    global data
    data = {}
