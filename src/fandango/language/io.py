from typing import final


class IoParty(object):
    roles = dict[str, "IoParty"]()

    def __init__(self):
        self.class_name = type(self).__name__.lower()
        IoParty.roles[self.class_name] = self

    def on_fandango_msg(self, message: str):
        pass

    @final
    def receive(self, message: str) -> None:
        FandangoIO.instance().set_remote_response(self.class_name, message)

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
        self._data = dict(
            {
                "local_response": dict[str, str](),
                "remote_response": dict[str, str](),
            }
        )
        FandangoIO.__instance = self

    def run_com_loop(self):
        for role, msg in self._data["local_response"].items():
            if role in IoParty.roles.keys():
                IoParty.roles[role].on_fandango_msg(msg)
        self._data["local_response"].clear()

    def set_remote_response(self, role: str, message: str) -> None:
        self._data["remote_response"][role] = message
