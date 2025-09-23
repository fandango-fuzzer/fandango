from typing import Optional, TypeVar, Generic
from collections.abc import Generator, Iterator

# Define type variables for generator type and return type
GT = TypeVar("GT")  # Generator Type
RT = TypeVar("RT")  # Return Type


class GeneratorNotFullyEvaluated:
    pass


class GeneratorWithReturn(Generic[GT, RT]):
    def __init__(self, generator: Generator[GT, None, RT]):
        self.generator = generator
        # use GeneratorNotFullyEvaluated instead of None because the generator may actually return None
        self._return_value: RT | GeneratorNotFullyEvaluated = (
            GeneratorNotFullyEvaluated()
        )

    def __iter__(self) -> Iterator[GT]:
        self._return_value = yield from self.generator

    @property
    def return_value(self) -> RT:
        """Get the return value of the generator.

        Raises:
            RuntimeError: If the generator hasn't been fully executed yet.
        """
        if isinstance(self._return_value, GeneratorNotFullyEvaluated):
            raise RuntimeError(
                "Generator hasn't been fully executed yet. The return value is only available after complete iteration."
            )
        return self._return_value

    def collect(self) -> tuple[list[GT], RT]:
        """
        :return: A tuple containing the list of yielded values and the return value.
        """
        return list(self), self.return_value
