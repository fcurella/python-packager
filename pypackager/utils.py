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
            ret[k] = clean_dict(v)
            continue

        ret[k] = v

    for k, v in ret.items():
        if v == {}:
            del ret[k]
    return ret
