Fandango Tutorial                                            
Request for Comments: FDP/1                              FSE Tutorial WG
Category: Educational                                        July 2026


              FDP: The Fandango Demo Protocol, Version 1


Abstract

   The Fandango Demo Protocol (FDP) is a tiny, text-based, stateful
   messaging protocol invented for the Fandango tutorial. It is small
   enough to specify on a few pages, yet it exercises every idea the
   tutorial teaches: structured grammars, length fields, checksums,
   semantic constraints, execution feedback, and stateful interaction.
   This document is the canonical description of FDP and of the
   reference implementation (fdp.py) that the tutorial fuzzes.

Status of This Memo

   This is a teaching artifact, not a real standard. It is deliberately
   simple and slightly contrived so that each tutorial block can add one
   concept on top of the previous one. Do not deploy it.


Table of Contents

   1. Introduction
   2. Conventions and Terminology
   3. Protocol Overview
   4. Message Format
   5. Message Types
   6. Processing Model
   7. Session State Machine
   8. Server Replies
   9. Examples
   10. Security Considerations
   Appendix A. Collected Grammar (ABNF)
   Appendix B. CRC-16 Reference


1. Introduction

   FDP is a line-oriented client/server messaging protocol. A client
   opens a connection, authenticates with a LOGIN, subscribes to one or
   more channels, sends messages to channels it has joined, and finally
   quits. The server keeps per-connection state, so the meaning of a
   message depends on what came before it on the same connection.

   FDP is text so that every input is human-readable and can be edited by
   hand. A complete message looks like this:

      FDP1 LOGIN user=alice LEN=16 CRC=339a

   The reference implementation processes each message through four
   stages -- frame, parse, validate, apply -- and rejects malformed input
   as early as possible. Later stages run only when earlier stages
   succeed, which is what makes deeper code reachable only by
   better-formed (and, ultimately, correctly sequenced) inputs.


2. Conventions and Terminology

   The key words "MUST", "MUST NOT", "SHOULD", and "MAY" are to be
   interpreted as in normal RFC usage.

   ABNF in this document follows RFC 5234. SP is a single space
   (0x20). All text is US-ASCII. "Body" means the substring
   "<TYPE> <payload>" that the LEN and CRC fields describe.


3. Protocol Overview

   FDP runs over any reliable, ordered, message-per-line transport. In
   the tutorial the transport is the standard input and output of the
   reference server (fdp_server.py): the client writes one message line,
   the server writes one reply line.

   A typical exchange:

      Client -> Server:  FDP1 LOGIN user=alice LEN=16 CRC=339a
      Server -> Client:  OK_LOGIN alice
      Client -> Server:  FDP1 SUB chan=general LEN=16 CRC=6fa6
      Server -> Client:  OK_SUB general
      Client -> Server:  FDP1 MSG to=general&body=hi LEN=22 CRC=....
      Server -> Client:  OK_MSG 1
      Client -> Server:  FDP1 QUIT LEN=4 CRC=9f54
      Server -> Client:  OK_QUIT delivered=1


4. Message Format

   A message is one line:

      FDP<version> SP <body> SP "LEN=" <length> SP "CRC=" <crc>

   with these parts, in order.

4.1. Anchor and Version

   Every message MUST begin with the anchor "FDP" immediately followed by
   a version digit and a single space. The version MUST be "1" or "2".
   A line that does not begin with the anchor is rejected as ERR_MAGIC;
   a bad or missing version is ERR_VERSION.

4.2. Body and Message Type

   The body is the substring between the anchor prefix and the trailing
   " LEN=..." field. Its first space-separated token is the message TYPE,
   one of:

      LOGIN  MSG  SUB  PING  QUIT

   An unknown type is rejected as ERR_TYPE. The remainder of the body,
   after the first space, is the payload (empty for PING and QUIT).

4.3. Payload and Records

   A payload is zero or more records joined by "&". Each record is
   "key=value": everything up to the first "=" is the key, the rest is
   the value. Keys MUST be non-empty (else ERR_EMPTY_KEY); a record with
   no "=" is ERR_RECORD. Values MAY be empty and MAY contain spaces.

      user=alice
      to=general&body=hello world

   A message MUST carry no more than 8 records (else ERR_FIELDS).

4.4. LEN

   LEN is a decimal integer equal to the number of characters in the
   body (the "<TYPE> <payload>" string, including the type token and the
   space after it). If LEN does not match, the message is rejected as
   ERR_LENGTH. The body MUST be between 1 and 64 characters; a longer
   body is ERR_TOO_LONG.

      Body "LOGIN user=alice" is 16 characters, so LEN=16.

4.5. CRC

   CRC is the CRC-16/CCITT-FALSE checksum of the ASCII bytes of the body,
   written as exactly four lowercase hexadecimal digits. The parameters
   are: polynomial 0x1021, initial value 0xFFFF, no input or output
   reflection, no final XOR. A mismatch is rejected as ERR_CRC. See
   Appendix B for a reference implementation.


5. Message Types

5.1. LOGIN

   "LOGIN user=<name>" optionally followed by "&pass=<word>". Requires a
   "user" record. Authenticates the connection. A second LOGIN on an
   already-authenticated connection is ERR_ALREADY.

5.2. SUB

   "SUB chan=<name>". Requires a "chan" record and an authenticated
   connection. Joins the named channel.

5.3. MSG

   "MSG to=<name>&body=<text>". Requires "to" and "body" records and an
   authenticated connection. The target channel MUST have been joined
   with SUB first, else ERR_NOSUB. On success the message is delivered
   and assigned an increasing sequence number.

5.4. PING

   "PING", no payload. Allowed on any open connection, before or after
   login. The server replies OK_PONG.

5.5. QUIT

   "QUIT", no payload. Requires an authenticated connection. Closes it;
   the reply reports how many messages were delivered.


6. Processing Model

   The server processes each message through four stages, and returns the
   first failure it encounters. This ordering is normative because the
   tutorial's coverage gradient depends on it.

   1. frame:    ERR_ENCODING, ERR_MAGIC, ERR_VERSION, ERR_SYNTAX,
                ERR_TYPE
   2. parse:    ERR_RECORD, ERR_EMPTY_KEY
   3. validate: ERR_LENGTH, ERR_TOO_LONG, ERR_CRC, ERR_FIELDS
   4. apply:    the OK_* replies and the state-dependent errors
                (ERR_NOAUTH, ERR_NOSUB, ERR_ALREADY, ERR_CLOSED)

   A stage runs only if every earlier stage succeeded. In particular, a
   correct LEN and CRC are required before any handler runs, and the
   handlers in stage 4 depend on connection state set by earlier
   messages.


7. Session State Machine

   A connection is in one of three states.

      START ---- LOGIN ----> AUTHENTICATED ---- QUIT ----> CLOSED

   * START: only LOGIN (-> AUTHENTICATED) and PING are meaningful. SUB,
     MSG, and QUIT return ERR_NOAUTH.
   * AUTHENTICATED: SUB joins a channel; MSG delivers to a joined channel
     (ERR_NOSUB otherwise); PING replies OK_PONG; a second LOGIN is
     ERR_ALREADY; QUIT moves to CLOSED.
   * CLOSED: every message returns ERR_CLOSED.

   The set of joined channels is part of AUTHENTICATED state, which is why
   "SUB then MSG" reaches delivery but a lone MSG never can.


8. Server Replies

   The server writes one reply line per message: a status code, optionally
   followed by a space and a detail.

      OK_LOGIN <user>          OK_SUB <chan>
      OK_MSG <seq>             OK_QUIT delivered=<n>
      OK_PONG
      ERR_ENCODING  ERR_MAGIC  ERR_VERSION  ERR_SYNTAX  ERR_TYPE
      ERR_RECORD    ERR_EMPTY_KEY
      ERR_LENGTH    ERR_TOO_LONG  ERR_CRC   ERR_FIELDS
      ERR_NOAUTH    ERR_NOSUB     ERR_ALREADY  ERR_CLOSED


9. Examples

   Accepted login:

      -> FDP1 LOGIN user=alice LEN=16 CRC=339a
      <- OK_LOGIN alice

   Same message with a wrong checksum:

      -> FDP1 LOGIN user=alice LEN=16 CRC=0000
      <- ERR_CRC

   Message before login (state error, not a format error):

      -> FDP1 MSG to=general&body=hi LEN=22 CRC=....
      <- ERR_NOAUTH


10. Security Considerations

   FDP has none worth the name. "Authentication" sets a username with no
   verification, the optional password is not checked, and the CRC is an
   integrity check against accidental corruption, not a security
   mechanism. FDP exists to be fuzzed in a classroom, not to protect
   anything.


Appendix A. Collected Grammar (ABNF)

   message  = "FDP" version SP body SP "LEN=" length SP "CRC=" crc
   version  = "1" / "2"
   body     = login / msg / sub / "PING" / "QUIT"
   login    = "LOGIN" SP "user=" name [ "&pass=" word ]
   msg      = "MSG" SP "to=" name "&body=" text
   sub      = "SUB" SP "chan=" name
   length   = 1*DIGIT
   crc      = 4HEXDIG
   name     = 1*%x61-7A                  ; one or more lowercase letters
   word     = 1*(%x61-7A / DIGIT)
   text     = 1*(%x61-7A / DIGIT / SP)

   Note: LEN and CRC describe <body>. In a well-formed message,
   length = number of characters in body, and crc = CRC-16 of body.


Appendix B. CRC-16 Reference

   CRC-16/CCITT-FALSE over the ASCII bytes of the body, as four lowercase
   hex digits:

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
