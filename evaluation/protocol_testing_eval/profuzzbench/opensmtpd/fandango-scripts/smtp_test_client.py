#!/usr/bin/env python3
import argparse
import base64
import smtplib
from datetime import datetime, timezone
from email.utils import format_datetime

MAIL_FROM = "theuser@example.de"
RCPT_TO = "regreg@example.de"
USER = "the_user"
PASSWORD = "the_password"
EHLO_NAME = "io.fandango.local"


def build_message():
    date = format_datetime(datetime.now(timezone.utc))  # RFC5322, English, +0000
    body_b64 = base64.b64encode(b"TestmailFandango\r\n").decode("ascii")
    return (
        "subject: TestmailFandango\r\n"
        f"from: {MAIL_FROM}\r\n"
        f"to: {RCPT_TO}\r\n"
        f"date: {date}\r\n"
        "x-mailer: smtplib\r\n"
        "mime-version: 1.0\r\n"
        "content-type: text/plain; charset=utf-8\r\n"
        "content-transfer-encoding: base64\r\n"
        "\r\n"
        f"{body_b64}\r\n\r\n"
    )


def main():
    ap = argparse.ArgumentParser(description="smtplib client for the Fandango SMTP server")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8025)
    ap.add_argument("--timeout", type=float, default=15.0)
    ap.add_argument("--debug", action="store_true", help="print the full SMTP dialogue")
    args = ap.parse_args()

    with smtplib.SMTP(
        host=args.host, port=args.port,
        local_hostname=EHLO_NAME, timeout=args.timeout,
    ) as smtp:
        smtp.set_debuglevel(1 if args.debug else 0)
        smtp.ehlo(EHLO_NAME)
        smtp.login(USER, PASSWORD)
        smtp.sendmail(MAIL_FROM, [RCPT_TO], build_message())

    print("message sent")


if __name__ == "__main__":
    main()
