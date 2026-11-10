---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
mystnb:
  merge_streams: true
---

(sec:timers)=
# Timers

Many protocols react to time passing:
a client sends a request again if no reply arrives within a few seconds,
a peer sends a keepalive after a period of silence,
and a session expires after some minutes.
To test such interactions, a Fandango spec can _start_ and _cancel_ timers and react to them _expiring_.

```{versionadded} 1.2
Timers are available in Fandango 1.2 and later.
```


## Timer Parties

Fandango models timers as two predefined [parties](sec:parties):

* `TimerControl` receives the commands from Fandango to start and cancel timers.
* `TimerEvent` reports that a timer has expired. Like a remote party, it is not controlled by Fandango; its messages arrive on their own.

Both classes are predefined within `.fan` files; they need not be imported.

The messages are defined in the [standard library](sec:stdlib):

| Message | Party | Symbol | Format |
|---------|-------|--------|--------|
| Start a timer | `TimerControl` | `<timer_start>` | `start: ID (SECONDS)\n` |
| Cancel a timer | `TimerControl` | `<timer_cancel>` | `cancel: ID\n` |
| A timer expired | `TimerEvent` | `<timer_expired>` | `expired: ID\n` |

`ID` (`<timer_id>`) is a number that identifies the timer.
`SECONDS` (`<timer_timeout>`) is the duration of the timer in seconds, such as `5` or `0.25`.


## A First Timer

Here is a spec that starts a timer, waits for it to expire, and then prints a message:

```{code-cell}
:tags: ["remove-input"]
!cat timer.fan
```

The rules `<wait_start>` and `<wait_expired>` give the timer messages names of their own, so that the constraints can set them to timer `1` and half a second.
Running this spec with the `talk` command prints the message after half a second:

```shell
$ fandango talk -f timer.fan -n 1
```

```{code-cell}
:tags: ["remove-input"]
!fandango talk -f timer.fan -n 1
assert _exit_code == 0
```


## Waiting for a Reply

The typical use of a timer is to limit how long to wait for a reply.
The following spec sends `PING` to a program and starts a timer of one second.
If the program answers in time, Fandango cancels the timer; otherwise, the timer expires:

```{code-cell}
:tags: ["remove-input"]
!cat timer-reply.fan
```

The constraints use `all(...)` since a symbol such as `<reply_cancel>` need not occur in a run, or may occur several times.

Against `cat`, which echoes its input, the reply arrives and the timer is cancelled.
With `-v`, Fandango logs the messages exchanged:

```shell
$ fandango -v talk -f timer-reply.fan -n 1 cat
```

```{code-cell}
:tags: ["remove-input"]
!fandango -v talk -f timer-reply.fan -n 1 cat 2>&1 | grep 'INFO: [A-Za-z]*: <'
```

Against a program that never answers, the timer expires:

```shell
$ fandango -v talk -f timer-reply.fan -n 1 sh -c 'sleep 3'
```

```{code-cell}
:tags: ["remove-input"]
!fandango -v talk -f timer-reply.fan -n 1 sh -c 'sleep 3' 2>&1 | grep 'INFO: [A-Za-z]*: <'
```

To try again after a timeout, let the expiry lead back to the request, as in

```
<exchange> ::= <In:request> <TimerControl:reply_start> <reply>
<reply> ::= <Out:response> <TimerControl:reply_cancel> | <TimerEvent:reply_expired> <exchange>
```


## How Timers Behave

* Starting a timer whose `ID` is running restarts it with the new duration.
* A cancelled timer does not expire. If it has already expired but its expiry has not been handled yet, cancelling drops the expiry.
* An expiry is handled only where the grammar allows a `TimerEvent` message next. Until then, it waits.
* While Fandango waits for a message and the grammar allows an expiry next, there is no time limit. Hence, a spec should only expect expiries of timers it has started.
* At the end of a run, all timers are stopped.

```{tip}
Use one `ID` per timer of the protocol, and constants in the spec for the IDs and durations.
The [WireGuard spec](https://github.com/fandango-fuzzer/fandango/blob/main/evaluation/protocol_testing_eval/wireguard/wireguard.fan) runs six timers this way, for handshakes, keepalives, and rekeying.
```
