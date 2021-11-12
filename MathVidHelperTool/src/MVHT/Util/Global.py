from typing import Any

_global_vars : dict[str,Any]= {}

def make_global(name : str, val : Any, **tags) -> None:
    _global_vars[name] = [val,tags]

def hide_global(name : str) -> Any:
    val = _global_vars[name][0]
    _global_vars.pop(name)
    return val

def get_var(name : str) -> Any:
    if name in _global_vars:
        return _global_vars[name][0]

def set_var(name : str, val : any) -> None:
    _global_vars[name][0] = val
    if 'on_change' in _global_vars[name][1]:
        _global_vars[name][1]['on_change']()
    if 'const' in _global_vars[name][1]:
        raise "Value Error: Can't Change Value of Constant"

def print_all() -> None:
    for key in _global_vars:
        print(key, _global_vars[key])
