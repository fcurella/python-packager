import collections


def unflatten_dict(a_dict):
    resultDict = {}
    for key, value in a_dict.items():
        parts = key.split("-")
        d = resultDict
        for part in parts[:-1]:
            if part not in d:
                d[part] = {}
            d = d[part]
        d[parts[-1]] = value
    return resultDict


def clean_dict(a_dict):
    ret = {}
    for k, v in a_dict.items():
        if v is None:
            continue

        if isinstance(v, dict):
            ret[k] = clean_dict(v).copy()
            continue

        ret[k] = v

    for k, v in ret.copy().items():
        if v == {}:
            del ret[k]
    return ret


def recursive_update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            r = recursive_update(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d


def import_classpath(class_path):
    module_path, class_name = class_path.rsplit('.', 1)
    module = __import__(module_path, fromlist=[class_name])
    return getattr(module, class_name)


def instantiate_classpath(class_path, *args, **kwargs):
    return import_classpath(class_path)(*args, **kwargs)
