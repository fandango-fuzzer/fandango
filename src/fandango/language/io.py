from typing import Callable


class IoParty(object):

    def __init__(self, is_fandango: bool):
        self.class_name = type(self).__name__.lower()
        self._is_fandango = is_fandango
        FandangoIO.instance().roles[self.class_name] = self

    """
    :return: True, if the party is substituted by fandango.
    """
    def is_fandango(self):
        return self._is_fandango

    """
    Called when fandango wants to send a message as this party.
    
    :message: The message to send.
    :response_setter: If the recipient of the message answers during the function call, this method can be called to set the response.
        First parameter of response_setter if the role of the other party. The second is the message, that it answered with.
    """
    def on_transmit_msg(self, message: str, response_setter: Callable[[str, str], None]):
        pass

    """
    Call if a message has been received from this party.
    """
    def receive_msg(self, message: str) -> None:
        FandangoIO.instance().set_receive(self.class_name, message)


class FandangoIO:
    __instance = None

    @classmethod
    def instance(cls) -> "FandangoIO":
        if cls.__instance is None:
            FandangoIO()
        return cls.__instance

    def __init__(self):
        if FandangoIO.__instance is not None:
            raise Exception("Singleton already created!")
        self._data = dict(
            {
                "transmit": dict[str, str](),
                "receive": list[(str, str)](),
            }
        )
        FandangoIO.__instance = self
        self.roles = dict[str, IoParty]()

    def run_com_loop(self):
        for role, msg in self._data["transmit"].items():
            if role in self.roles.keys():
                self.roles[role].on_transmit_msg(msg, self.set_receive)
        self._data["transmit"].clear()

    def set_receive(self, role: str, message: str) -> None:
        self._data["receive"].append((role, message))
