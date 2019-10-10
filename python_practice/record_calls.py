from functools import wraps
from dataclasses import dataclass
from typing import Callable, TypeVar, Sequence, Mapping, Optional, Any

T = TypeVar('T')


@dataclass
class Call(object):
    args: Sequence[Any]
    kwargs: Mapping[str, Any]
    exception: Optional[Exception] = None


def record_calls(fn: Callable[..., T]) -> Callable[..., T]:
    """
    Decorator that maintains the call information of a function during execution.
    """
    fn.calls = []

    @wraps(fn)
    def wrapper(*args: Sequence[Any], **kwargs: Optional[Mapping[str, Any]]):
        current_call = Call(args=args, kwargs=kwargs)
        try:
            return_value = fn(*args, **kwargs)
            current_call.return_value = return_value
        except Exception as exc:
            current_call.exception = exc
            current_call.return_value = None
            raise
        finally:
            fn.calls.append(current_call)

        return return_value

    return wrapper

