from typing import Any

_global_vars : dict[str,Any]= {}

def make_global(name : str, val : Any) -> None:
    _global_vars[name] = val

def hide_global(name : str) -> Any:
    val = _global_vars[name]
    _global_vars.pop(name)
    return val

def get_var(name : str) -> Any:
    if name in _global_vars:
        return _global_vars[name]

def set_var(name : str, val : any) -> None:
    _global_vars[name] = val