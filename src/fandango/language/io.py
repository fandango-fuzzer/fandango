from enum import Enum


class FandangoLifecycle(Enum):
    PRE_EVOLVE = 1
    POST_EVOLVE = 2
    FINALLY = 3


class FandangoIO:
    __instance = None

    @classmethod
    def instance(cls):
        if cls.__instance is None:
            FandangoIO()
        return cls.__instance

    def __init__(self):
        if FandangoIO.__instance is not None:
            raise Exception("Singleton already created!")
        self.data = dict(
            {"solutions": list[str](), "partial_solution": dict[str, str]()}
        )
        self.lifecycle_events = dict()
        FandangoIO.__instance = self

    def get_solutions(self) -> list[str]:
        return self.data["solutions"]

    def set_partial_solution(self, path: str, value: str):
        self.data["partial_solution"][path] = value

    def on_lifecycle(self, lifecycle: FandangoLifecycle, function):
        self.lifecycle_events[lifecycle] = function
