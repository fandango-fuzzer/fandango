import threading
from typing import Callable, Tuple

from fandango.language.tree import DerivationTree


class FandangoAgent(object):

    def __init__(self, is_fandango: bool):
        self.class_name = type(self).__name__
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

    def on_send(
        self,
        message: DerivationTree,
        recipient: str,
        response_setter: Callable[[str, str], None],
    ):
        print(f"({self.class_name}): {message.to_string()}")

    """
    Call if a message has been received by this party.
    """

    def receive_msg(self, sender: str, message: str) -> None:
        FandangoIO.instance().add_receive(sender, self.class_name, message)


class STDOUT(FandangoAgent):

    def __init__(self):
        super().__init__(True)


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
        FandangoIO.__instance = self
        self.transmit: Tuple[str, str, DerivationTree] | None = None
        self.receive = list[(str, str, str)]()
        self.roles = dict[str, FandangoAgent]()
        self.receive_lock = threading.Lock()

    def run_com_loop(self):
        if self.transmit is not None:
            role, recipient, msg = self.transmit
            if role in self.roles.keys():
                self.roles[role].on_send(msg, recipient, self.roles[role].receive_msg)
        self.clear_transmit_msgs()

    def clear_transmit_msgs(self):
        self.transmit = None

    def add_receive(self, role: str, receiver: str, message: str) -> None:
        with self.receive_lock:
            self.receive.append((role, receiver, message))

    def received_msg(self):
        with self.receive_lock:
            return len(self.receive) != 0

    def get_received_msgs(self):
        with self.receive_lock:
            return list(self.receive)

    def clear_received_msg(self, idx: int):
        with self.receive_lock:
            del self.receive[idx]

    def clear_received_msgs(self):
        with self.receive_lock:
            self.receive.clear()

    def set_transmit(
        self, role: str, recipient: str | None, message: DerivationTree
    ) -> None:
        self.transmit = (role, recipient, message)
