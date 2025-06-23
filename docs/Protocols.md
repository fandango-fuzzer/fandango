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
---

(sec:protocols)=
# Testing Protocols

```{admonition} Under Construction
:class: attention
This chapter is still under construction.
```

```shell
$ pip install aiosmtpd
```

```shell
$ python -m aiosmtpd -d -n
```

```shell
$ telnet localhost 8025                                                                             2025-06-21 17:41
Trying ::1...
Connected to localhost.
Escape character is '^]'.
220 localhost.example.com Python SMTP 1.4.6
QUIT
221 Bye
Connection closed by foreign host.
```

% Start the server
```{code-cell}
!python -m aiosmtpd -d -n & echo $! > aiosmtpd.pid
```

% We should now be able to connect to the server
```{code-cell}
!fandango talk -f smtp.fan --client=8025
```

% Stop the server
```{code-cell}
!kill $(cat aiosmtpd.pid)
!rm aiosmtpd.pid
```

