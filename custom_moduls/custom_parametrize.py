import pytest


def custom_parametrize(data, arguments=(), skip=None, skip_reason='Skipped', **kwargs):
    if skip is None:
        skip = {}

    args = [key for key in list(data.values())[0].keys() if key in arguments]
    ids = list(data.keys())

    formatted_data = []
    for key, item in data.items():

        if key in skip:
            mark = getattr(pytest.mark, skip[key]['method'])(True, reason=skip[key].get('msg', skip_reason))
        else:
            mark = ()

        formatted_data.append(pytest.param(*[item[a] for a in args], marks=mark))

    return pytest.mark.parametrize(args, formatted_data, ids=ids, **kwargs)