import unittest

from fandango.io.navigation.coverage_goal import CoverageGoal
from fandango.language.grammar import FuzzingMode
from fandango.language.parse.parse import parse
from fandango.evolution.algorithm import Fandango, LoggerLevel
import socket
import time

from tests.utils import EVALUATION_ROOT


import asyncio
import threading
from aiosmtpd.smtp import SMTP
from aiosmtpd.handlers import Debugging
from aiosmtpd.smtp import AuthResult, LoginPassword


class SMTPServer:
    def __init__(self, host="127.0.0.1", port=0):
        self.host = host
        self.port = port
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.server = None

    def _run_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def authenticator_func(self, server, session, envelope, mechanism, auth_data):
        if mechanism not in ("LOGIN", "PLAIN"):
            return AuthResult(success=False, handled=False)

        if not isinstance(auth_data, LoginPassword):
            return AuthResult(success=False, handled=False)

        if auth_data.login == b"the_user" and auth_data.password == b"the_password":
            return AuthResult(success=True, handled=True)

        return AuthResult(
            success=False,
            handled=False,
            message="535 5.7.8 Authentication credentials invalid",
        )

    def start(self):
        self.thread.start()

        async def start_server():
            self.server = await self.loop.create_server(
                lambda: SMTP(
                    Debugging(),
                    authenticator=self.authenticator_func,
                    require_starttls=False,
                    auth_require_tls=False,
                ),
                host=self.host,
                port=self.port,
            )
            self.port = self.server.sockets[0].getsockname()[1]

        fut = asyncio.run_coroutine_threadsafe(start_server(), self.loop)
        fut.result(timeout=10)

    def stop(self):
        async def shutdown_server():
            assert self.server is not None
            self.server.close()
            await self.server.wait_closed()

        fut = asyncio.run_coroutine_threadsafe(shutdown_server(), self.loop)
        fut.result(timeout=10)

        self.loop.call_soon_threadsafe(lambda: self.loop.stop())
        self.thread.join(timeout=10)


def wait_for_port(host, port, timeout=5.0):
    end = time.time() + timeout
    while time.time() < end:
        try:
            with socket.create_connection((host, port), timeout=0.5):
                return
        except OSError:
            time.sleep(0.1)
    raise RuntimeError("SMTP server did not become ready")


class GrammarCoverageTest(unittest.TestCase):
    @staticmethod
    def gen_fandango(coverage_goal: CoverageGoal, port: int) -> Fandango:
        client_def = f"""
class Client(NetworkParty):
    def __init__(self):
        super().__init__(
            connection_mode=ConnectionMode.CONNECT,
            uri="tcp://127.0.0.1:{port}"
        )
        self.start()

class Server(NetworkParty):
    def __init__(self):
        super().__init__(
            connection_mode=ConnectionMode.EXTERNAL,
            uri="tcp://127.0.0.1:{port}"
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

    def test_io_smtp_inputs(self):
        server = SMTPServer()
        server.start()
        wait_for_port("127.0.0.1", server.port)

        try:
            fandango = GrammarCoverageTest.gen_fandango(
                CoverageGoal.STATE_INPUTS_OUTPUTS, port=server.port
            )
            for solution in fandango.generate(mode=FuzzingMode.IO):
                pass
        finally:
            server.stop()


if __name__ == "__main__":
    unittest.main()
