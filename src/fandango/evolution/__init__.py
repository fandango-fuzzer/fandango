from typing import Generator, Optional, TypeVar

# Define type variables for generator type and return type
GT = TypeVar("GT")  # Generator Type
RT = TypeVar("RT")  # Return Type


class GeneratorWithReturn[GT, RT]:
    def __init__(self, generator: Generator[GT, None, RT]):
        self.generator = generator
        self._return_value: Optional[RT] = None

    def __iter__(self):
        self._return_value = yield from self.generator

    @property
    def return_value(self) -> RT:
        """Get the return value of the generator.

        Raises:
            RuntimeError: If the generator hasn't been fully executed yet.
        """
        if self._return_value is None:
            raise RuntimeError(
                "Generator hasn't been fully executed yet. The return value is only available after complete iteration."
            )
        return self._return_value
