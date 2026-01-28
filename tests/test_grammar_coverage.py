import os
import sys
import time
import unittest
from asyncio import Server

from aiosmtpd.handlers import Debugging

from fandango.io.navigation.coverage_goal import CoverageGoal
from fandango.language.grammar import FuzzingMode
from fandango.language.parse.parse import parse
from fandango.evolution.algorithm import Fandango, LoggerLevel
from aiosmtpd.controller import Controller
from aiosmtpd.smtp import AuthResult, LoginPassword

from tests.utils import EVALUATION_ROOT


class SMTPServer:
    def __init__(self, host="localhost", port=8025):
        self.controller = Controller(
            handler=Debugging(),
            authenticator=self.authenticator_func,
            hostname=host,
            port=port,
            require_starttls=False,
            auth_require_tls=False,
            ready_timeout=60.0,
        )

    def authenticator_func(self, server, session, envelope, mechanism, auth_data):
        if mechanism not in ("LOGIN", "PLAIN"):
            return AuthResult(success=False, handled=False)

        if not isinstance(auth_data, LoginPassword):
            return AuthResult(success=False, handled=False)

        if auth_data.login == b"the_user" and auth_data.password == b"the_password":
            return AuthResult(success=True, handled=True)

        # Wrong credentials, connection stays open
        return AuthResult(
            success=False,
            handled=False,
            message="535 5.7.8 Authentication credentials invalid",
        )

    def start(self):
        self.controller.start()

    def stop(self):
        self.controller.stop()

    @property
    def port(self):
        assert self.controller.server is not None
        assert isinstance(self.controller.server, Server)
        return self.controller.server.sockets[0].getsockname()[1]


class GrammarCoverageTest(unittest.TestCase):
    @staticmethod
    def gen_fandango(coverage_goal: CoverageGoal, host: str, port: int) -> Fandango:

        client_def = f"""
class Client(NetworkParty):
    def __init__(self):
        super().__init__(
            connection_mode=ConnectionMode.CONNECT,
            uri="tcp://{host}:{port}"
        )
        self.start()

class Server(NetworkParty):
    def __init__(self):
        super().__init__(
            connection_mode=ConnectionMode.EXTERNAL,
            uri="tcp://{host}:{port}"
        )
        self.start()
        """

        with open(EVALUATION_ROOT / "experiments/smtp/smtp.fan") as f:
            grammar, constraints = parse(
                [f, client_def],
                use_stdlib=False,
            )
        assert grammar is not None
        return Fandango(
            grammar=grammar,
            constraints=constraints,
            logger_level=LoggerLevel.INFO,
            coverage_goal=coverage_goal,
        )

    @unittest.skipIf(
        sys.platform == "darwin" and os.getenv("CI") == "true",
        "Skipping IO SMTP inputs grammar coverage test on macos.",
    )
    def test_io_smtp_inputs(self):
        import socket

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", 0))
            free_port = s.getsockname()[1]

        server = SMTPServer(host="127.0.0.1", port=free_port)
        server.start()
        time.sleep(2)

        try:
            fandango = GrammarCoverageTest.gen_fandango(
                CoverageGoal.STATE_INPUTS_OUTPUTS, host="127.0.0.1", port=server.port
            )
            for solution in fandango.generate(mode=FuzzingMode.IO):
                pass
        finally:
            server.stop()


if __name__ == "__main__":
    unittest.main()
