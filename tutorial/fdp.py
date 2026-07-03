"""FDP - Fandango Demo Protocol: reference implementation (text version).

A tiny *text* messaging protocol used as the single running target for the
whole tutorial. Text keeps every input human-readable and hand-editable, which
matters when students debug their own grammars and constraints.

It is deliberately built as a four-stage pipeline

    frame  ->  parse  ->  validate  ->  apply

where each stage consumes the *typed* result of the previous one and rejects
as soon as its input is malformed. A later stage cannot run unless every
earlier stage produced a valid value, so the coverage a fuzzer reaches grows
with the sophistication of the inputs it feeds in:

    random bytes         reach  frame()       anchor / version / syntax checks
    grammar-valid lines  reach  parse()       payload record parsing
    constraint-valid     reach  apply()       handlers + state-precondition guards
    valid *sequences*    reach  apply() deep   handlers gated on prior session state

The gradient is a property of real data dependencies, not of coverage-milking
branches: parse() needs a Frame, apply() needs a Valid message, and some
apply() branches need session state that only a *previous* message can set.

One message is one line:

    FDP<ver> <TYPE> <payload> LEN=<len> CRC=<crc>

* ``<ver>``     is ``1`` or ``2`` (``FDP1``/``FDP2`` is the anchor)
* ``<TYPE>``    is LOGIN | MSG | SUB | PING | QUIT
* ``<payload>`` is ``key=value`` records joined by ``&`` (empty for PING/QUIT)
* ``LEN``       is the decimal length of the body ``"<TYPE> <payload>"``
* ``CRC``       is the CRC-16/CCITT (4 hex digits) of that same body

Example:  ``FDP1 MSG to=general&body=hello world LEN=31 CRC=1b7c``
"""

import re
from dataclasses import dataclass, field
from typing import Optional

# ---------------------------------------------------------------------------
# Protocol constants
# ---------------------------------------------------------------------------

PROTO = "FDP"
VERSIONS = ("1", "2")
TYPES = ("LOGIN", "MSG", "SUB", "PING", "QUIT")
MAX_BODY = 64
MAX_RECORDS = 8

# a well-framed line ends in " LEN=<digits> CRC=<hex>"; the body is everything
# between the "FDP<ver> " prefix and that trailer.
_TRAILER = re.compile(r"^(?P<body>.*) LEN=(?P<len>\d+) CRC=(?P<crc>[0-9a-f]+)$")


# ---------------------------------------------------------------------------
# Typed values passed between pipeline stages
# ---------------------------------------------------------------------------

@dataclass
class Frame:
    version: str
    msgtype: str
    body: str             # "<TYPE> <payload>" - the bytes LEN and CRC describe
    payload: str          # body without the leading type token
    length: int           # claimed body length (from the LEN field)
    crc: str              # claimed checksum (from the CRC field, 4 hex digits)


@dataclass
class Message:
    frame: Frame
    fields: dict          # parsed key -> value


@dataclass
class Valid:
    message: Message


@dataclass
class Response:
    stage: str            # deepest stage reached: frame|parse|validate|apply
    code: str             # ERR_* on rejection, OK_* on acceptance
    detail: str = ""
    trace: tuple = ()     # branch labels this input drove through (cheap coverage)


@dataclass
class Session:
    user: Optional[str] = None
    subs: set = field(default_factory=set)
    seq: int = 0
    closed: bool = False
    log: list = field(default_factory=list)


# ---------------------------------------------------------------------------
# Checksum (CRC-16/CCITT-FALSE) over a text body
# ---------------------------------------------------------------------------

def crc16(data: bytes) -> int:
    crc = 0xFFFF
    for b in data:
        crc ^= b << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return crc


def crc16hex(text: str) -> str:
    return format(crc16(text.encode("ascii")), "04x")


# ---------------------------------------------------------------------------
# Cheap self-instrumentation.
#   Each gate an input clears appends a label; fdp_cover reads the number of
#   distinct labels as a fast per-input coverage signal. This avoids
#   sys.settrace (too slow inside a search loop) and mirrors how real
#   coverage-guided fuzzers work: the target reports its own coverage.
# ---------------------------------------------------------------------------

_TRACE: list = []


def _mark(label: str) -> None:
    _TRACE.append(label)


# ---------------------------------------------------------------------------
# Stage 1: framing.  Reachable by ANY bytes.
# ---------------------------------------------------------------------------

def frame(data: bytes):
    try:
        line = data.decode("ascii")
    except UnicodeDecodeError:
        return Response("frame", "ERR_ENCODING")
    line = line.rstrip("\n")
    if not line.startswith(PROTO):
        return Response("frame", "ERR_MAGIC")
    _mark("frame:anchor")
    if len(line) < 5 or line[3] not in VERSIONS or line[4] != " ":
        return Response("frame", "ERR_VERSION")
    _mark("frame:version")
    version = line[3]
    rest = line[5:]
    m = _TRAILER.match(rest)
    if m is None:
        return Response("frame", "ERR_SYNTAX")
    _mark("frame:syntax")
    body = m.group("body")
    length = int(m.group("len"))
    crc = m.group("crc")
    if " " in body:
        msgtype, payload = body.split(" ", 1)
    else:
        msgtype, payload = body, ""
    if msgtype not in TYPES:
        return Response("frame", "ERR_TYPE")
    _mark("frame:type:" + msgtype)
    return Frame(version, msgtype, body, payload, length, crc)


# ---------------------------------------------------------------------------
# Stage 2: parsing.  Reachable only once framing holds.
# ---------------------------------------------------------------------------

def parse(fr: Frame):
    fields: dict = {}
    records = [] if fr.payload == "" else fr.payload.split("&")
    for rec in records:
        if "=" not in rec:
            return Response("parse", "ERR_RECORD", detail=rec)
        key, value = rec.split("=", 1)
        if key == "":
            return Response("parse", "ERR_EMPTY_KEY")
        fields[key] = value
    _mark("parse:ok")
    return Message(fr, fields)


# ---------------------------------------------------------------------------
# Stage 3: validation.  Reachable only once parsing holds.
#   This is the semantic gate: length encoding, checksum, field invariants.
# ---------------------------------------------------------------------------

def validate(msg: Message):
    fr = msg.frame
    if fr.length != len(fr.body):
        return Response("validate", "ERR_LENGTH")
    _mark("validate:length")
    if len(fr.body) > MAX_BODY:
        return Response("validate", "ERR_TOO_LONG")
    _mark("validate:size")
    if fr.crc != crc16hex(fr.body):
        return Response("validate", "ERR_CRC")
    _mark("validate:crc")

    t = fr.msgtype
    f = msg.fields
    if t == "LOGIN" and "user" not in f:
        return Response("validate", "ERR_FIELDS", detail="login needs user")
    elif t == "MSG" and ("to" not in f or "body" not in f):
        return Response("validate", "ERR_FIELDS", detail="msg needs to/body")
    elif t == "SUB" and "chan" not in f:
        return Response("validate", "ERR_FIELDS", detail="sub needs chan")
    if len(f) > MAX_RECORDS:
        return Response("validate", "ERR_FIELDS", detail="too many records")
    _mark("validate:fields")
    return Valid(msg)


# ---------------------------------------------------------------------------
# Stage 4: application.  Reachable only once validation holds.
#   Deep branches here require session STATE that only a prior message can set.
# ---------------------------------------------------------------------------

def apply(session: Session, vm: Valid):
    msg = vm.message
    fr = msg.frame
    t = fr.msgtype
    f = msg.fields
    _mark("apply:enter")
    if session.closed:
        return Response("apply", "ERR_CLOSED")

    if t == "PING":
        _mark("apply:pong")
        return Response("apply", "OK_PONG")

    if t == "LOGIN":
        if session.user is not None:
            return Response("apply", "ERR_ALREADY")
        session.user = f["user"]
        _mark("apply:login")
        return Response("apply", "OK_LOGIN", detail=session.user)

    # everything below requires an authenticated session -> the protocol gate
    if session.user is None:
        return Response("apply", "ERR_NOAUTH")
    _mark("apply:authed")

    if t == "SUB":
        session.subs.add(f["chan"])
        _mark("apply:sub")
        return Response("apply", "OK_SUB", detail=f["chan"])

    if t == "MSG":
        if f["to"] not in session.subs:
            return Response("apply", "ERR_NOSUB")
        session.seq += 1
        session.log.append((session.seq, f["to"], f["body"]))
        _mark("apply:msg")
        return Response("apply", "OK_MSG", detail=str(session.seq))

    if t == "QUIT":
        session.closed = True
        _mark("apply:quit")
        return Response("apply", "OK_QUIT", detail=f"delivered={len(session.log)}")

    return Response("apply", "ERR_UNHANDLED")


# ---------------------------------------------------------------------------
# The pipeline entry point.  One line in, one Response out.
# ---------------------------------------------------------------------------

def process(data: bytes, session: Optional[Session] = None) -> Response:
    if session is None:
        session = Session()
    _TRACE.clear()
    fr = frame(data)
    if isinstance(fr, Response):
        return _attach(fr)
    msg = parse(fr)
    if isinstance(msg, Response):
        return _attach(msg)
    vm = validate(msg)
    if isinstance(vm, Response):
        return _attach(vm)
    return _attach(apply(session, vm))


def _attach(resp: Response) -> Response:
    resp.trace = tuple(_TRACE)
    return resp


def build_message(version: str, msgtype: str, payload: str = "") -> str:
    """Helper: assemble a fully valid message line (tests and the server)."""
    body = msgtype if payload == "" else f"{msgtype} {payload}"
    return f"{PROTO}{version} {body} LEN={len(body)} CRC={crc16hex(body)}"
