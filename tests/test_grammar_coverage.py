import unittest

from aiosmtpd.handlers import Debugging

from fandango.io.navigation.coverage_goal import CoverageGoal
from fandango.language.grammar import FuzzingMode
from fandango.language.parse.parse import parse
from fandango.evolution.algorithm import Fandango, LoggerLevel
from aiosmtpd.controller import Controller
from aiosmtpd.smtp import AuthResult, LoginPassword

from tests.utils import EVALUATION_ROOT


class SMTPServer:
    def __init__(self, host="127.0.0.1", port=8025):
        self.controller = Controller(
            handler=Debugging(),
            authenticator=self.authenticator_func,
            hostname=host,
            port=port,
            require_starttls=False,
            auth_require_tls=False,
            ready_timeout=20.0,
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


class GrammarCoverageTest(unittest.TestCase):
    @staticmethod
    def gen_fandango(coverage_goal: CoverageGoal) -> Fandango:
        with open(EVALUATION_ROOT / "experiments/smtp/smtp_client.fan") as f:
            grammar, constraints = parse(
                f,
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
        server = SMTPServer(port=8025)
        server.start()

        try:
            fandango = GrammarCoverageTest.gen_fandango(
                CoverageGoal.STATE_INPUTS_OUTPUTS
            )
            for solution in fandango.generate(mode=FuzzingMode.IO):
                pass
        finally:
            server.stop()


if __name__ == "__main__":
    unittest.main()
