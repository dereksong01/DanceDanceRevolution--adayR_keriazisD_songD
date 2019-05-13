from json import loads
from enum import Enum, auto, unique
from typing import Union, List, Dict, Optional

@unique
class OnError(Enum):
    SET_FIELDS_NONE = auto()
    RETURN_NONE = auto()
    IGNORE = auto()
    RAISE_EXCEPTION = auto()

InType = Union[int, float, str, bool, List['InType'], Dict[str, 'InType']]
OutType = Union[type, List['OutType'], Dict[str, 'OutType']]
ReturnType = Union[None, int, float, str, bool, List['ReturnType'], Dict[str, 'ReturnType']]

def coerce_type(
        d: InType, t: OutType, on_error: OnError = OnError.RETURN_NONE,
    ) -> ReturnType:
    """
    Known issues:
    - Exception messages can be very wrong about what the actual error was
    - Because `bool` is a subclass of `int`, booleans are allowed to pass
    as integers in our coercion. This is currently WONTFIX since booleans
    are allowed to be used in all circumstances integers are allowed to be
    used in, so this isn't seen as a problem worth adding extra complication
    to fix.
    """
    if isinstance(t, list):
        if not isinstance(d, list):
            if on_error is OnError.SET_FIELDS_NONE:
                return None
            elif on_error is OnError.RETURN_NONE:
                return None
            elif on_error is OnError.IGNORE:
                return None
            elif on_error is OnError.RAISE_EXCEPTION:
                raise TypeError(f'Expected list but got `{d}` of type {type(d)}')
            # We raise an exception to assure static checkers
            # that our enumeration was exhaustive
            assert False
        result_list: List[ReturnType] = []
        for i in d:
            found_matching_type = False
            for try_type in t:
                v = coerce_type(i, try_type, OnError.RETURN_NONE)
                if v is None:
                    continue
                result_list.append(v)
                found_matching_type = True
            if not found_matching_type:
                if on_error is OnError.SET_FIELDS_NONE:
                    result_list.append(None)
                    continue
                elif on_error is OnError.RETURN_NONE:
                    return None
                elif on_error is OnError.IGNORE:
                    continue
                elif on_error is OnError.RAISE_EXCEPTION:
                    raise TypeError(f'Expected dict but got `{d}` of type {type(d)}')
                # We raise an exception to assure static checkers
                # that our enumeration was exhaustive
                assert False
        return result_list
    elif isinstance(t, dict):
        if not isinstance(d, dict):
            if on_error is OnError.SET_FIELDS_NONE:
                return None
            elif on_error is OnError.RETURN_NONE:
                return None
            elif on_error is OnError.IGNORE:
                return None
            elif on_error is OnError.RAISE_EXCEPTION:
                raise TypeError(f'Expected dict but got `{d}` of type {type(d)}')
            # We raise an exception to assure static checkers
            # that our enumeration was exhaustive
            assert False
        result_dict: Dict[str, ReturnType] = {}
        for k in d:
            if k in t:
                v = coerce_type(d[k], t[k], on_error)
                if v is None:
                    if on_error is OnError.RETURN_NONE:
                        return None
                    elif on_error is OnError.IGNORE:
                        continue
                result_dict[k] = v
            else:
                if on_error is OnError.SET_FIELDS_NONE:
                    result_dict[k] = None
                    continue
                elif on_error is OnError.RETURN_NONE:
                    return None
                elif on_error is OnError.IGNORE:
                    continue
                elif on_error is OnError.RAISE_EXCEPTION:
                    raise TypeError(f'Expected {t} but got `{d}` of type {type(d)}')
                # We raise an exception to assure static checkers
                # that our enumeration was exhaustive
                assert False
        if len(result_dict) < len(t):
            if on_error is OnError.RETURN_NONE:
                return None
            elif on_error is OnError.SET_FIELDS_NONE:
                for k in t:
                    if k not in result_dict:
                        result_dict[k] = None
            elif on_error is OnError.RAISE_EXCEPTION:
                raise TypeError(
                    f'Expected {len(t)} keys but got ' \
                    f'{len(result_dict)} keys'
                )
            else:
                pass  # Explicit 'do nothing'
        return result_dict
    else:
        if isinstance(d, t):
            return d
        else:
            if on_error is OnError.SET_FIELDS_NONE:
                return None
            elif on_error is OnError.RETURN_NONE:
                return None
            elif on_error is OnError.IGNORE:
                return None
            elif on_error is OnError.RAISE_EXCEPTION:
                raise TypeError(f'Expected {t} but got `{d}` of type {type(d)}')
            # We raise an exception to assure static checkers
            # that our enumeration was exhaustive
            assert False

def safe_loads(
        s: str, t: OutType, on_error: OnError = OnError.RETURN_NONE,
    ) -> ReturnType:
    try:
        j = loads(s)
    except:
        if on_error is OnError.SET_FIELDS_NONE:
            return None
        elif on_error is OnError.RETURN_NONE:
            return None
        elif on_error is OnError.IGNORE:
            return None
        elif on_error is OnError.RAISE_EXCEPTION:
            raise TypeError('Malformed JSON')
        # We raise an exception to assure static checkers
        # that our enumeration was exhaustive
        assert False
    return coerce_type(j, t, on_error)

