from abc import ABC, abstractmethod


class FandangoConverter(ABC):
    """Abstract superclass for converting a given grammar spec to Fandango format."""

    def __init__(self, filename: str):
        """Initialize with given grammar file"""
        self.filename = filename

    @abstractmethod
    def to_fan(self) -> str:
        """Convert the grammar spec to Fandango format"""
        raise NotImplementedError("Subclasses must implement this method")
