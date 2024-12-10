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

(sec:binary)=
# Generating Binary Inputs

```{error}
This chapter is under construction.
```


## Checksums

```{code-cell}
:tags: ["remove-input"]
# show grammar except '<byte>'
!grep '::=' credit_card.fan | grep -v '^<byte>'
```


Luhn's algorithm, adapted from the [Faker library](https://github.com/joke2k/faker/blob/master/faker/providers/credit_card/__init__.py#L99).

```{code-cell}
:tags: ["remove-input"]
# show code
!grep -v ';' credit_card.fan
```

% ```{code-cell}
% from faker import Faker
% from faker.providers import credit_card
%
% fake = Faker()
% for _ in range(100):
%     num = fake.credit_card_number()
%     check_digit = credit_card_check_digit(num[:-1])
%     assert check_digit == num[-1], f"got check digit {check_digit} for {num}, expected {num[-1]}"
% ```

```{code-cell}
:tags: ["remove-input"]
# show constraints
!grep ';$' credit_card.fan | grep -v '::='
```

```shell
$ fandango fuzz -n 10 -f credit_card.fan
```

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -n 10 -f credit_card.fan
```


## Length Encodings

% This is how I got the `<byte>` definition in `binary.fan` -- AZ
```{code-cell}
:tags: ["remove-input", "remove-output"]
import string
for i in range(0, 256):
    c = chr(i)
    if c in string.printable:
        print(repr(c), end=" | ")
    else:
        print(f"'\\x{i:02x}'", end=" | ")
```

```{code-cell}
:tags: ["remove-input"]
# show grammar except '<byte>'
!grep '::=' binary.fan | grep -v '^<byte>'
```

```{code-cell}
:tags: ["remove-input"]
# show code
!grep -v ';' binary.fan
```

```{code-cell}
:tags: ["remove-input"]
# show constraints
!grep ';$' binary.fan | grep -v '::='
```

```shell
$ fandango fuzz -n 1 -f binary.fan | od -c
```

```{code-cell}
:tags: ["remove-input"]
! fandango fuzz -n 1 -f binary.fan | od -c
```

:::{tip}
Try to have a single symbol on the left-hand side of an equality sign.
:::
