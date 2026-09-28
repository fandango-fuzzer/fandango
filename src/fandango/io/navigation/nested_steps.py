from collections.abc import Callable, Generator
from typing import Optional, TypeVar, cast

Request = TypeVar("Request")
Result = TypeVar("Result")


def run_nested_steps(
    steps: Generator[Request, Result, Result],
    steps_for: Callable[[Request], Generator[Request, Result, Result]],
) -> Result:
    """
    Runs a recursive function without Python's recursion limit.

    Write the function as a generator: where it would call itself, it yields
    the argument instead, e.g. `size = yield child` instead of
    `size = self.size(child)`. `steps_for` creates the generator for that
    argument. This function runs it and sends its return value back to the
    `yield`, or raises its exception there, just like a real call would.

        def size_steps(tree):
            size = 1
            for child in tree.children:
                size += yield child
            return size

        run_nested_steps(size_steps(root), size_steps)
    """
    pending_steps = [steps]
    is_started = False
    nested_result: Optional[Result] = None
    nested_error: Optional[Exception] = None
    while pending_steps:
        current_steps = pending_steps[-1]
        try:
            if nested_error is not None:
                raised_error, nested_error = nested_error, None
                request = current_steps.throw(raised_error)
            elif is_started:
                request = current_steps.send(cast(Result, nested_result))
            else:
                request = next(current_steps)
        except StopIteration as finished_steps:
            pending_steps.pop()
            is_started = True
            nested_result = finished_steps.value
            continue
        except Exception as steps_error:
            pending_steps.pop()
            is_started = True
            nested_error = steps_error
            continue
        try:
            pending_steps.append(steps_for(request))
            is_started = False
        except Exception as steps_error:
            is_started = True
            nested_error = steps_error
    if nested_error is not None:
        raise nested_error
    return cast(Result, nested_result)
