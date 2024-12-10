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
        self._data = dict({
            "solutions": list[str](),
            "partial_solution": dict[str, str]()
        })
        self.lifecycle_events = dict()
        FandangoIO.__instance = self

    def get_solutions(self) -> list[str]:
        return self._data["solutions"]

    def set_partial_solution(self, path: str, value: str):
        self._data["partial_solution"][path] = value

    def get_partial_solutions(self) -> dict[str, str]:
        return self._data["partial_solution"].copy()

    def on_lifecycle(self, lifecycle: FandangoLifecycle, function):
        self.lifecycle_events[lifecycle] = function

    def get_lifecycle_events(self):
        return self.lifecycle_events.copy()

    def dispatch_lifecycle(self, lifecycle: FandangoLifecycle):
        if lifecycle in self.lifecycle_events.keys():
            self.lifecycle_events[lifecycle]()