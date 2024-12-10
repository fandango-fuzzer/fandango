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

```{code-cell}
!grep -v '^<byte>' binary.fan
```

```{code-cell}
!fandango fuzz -n 10 -f binary.fan
```

% This is how I got the `<byte>` definition -- AZ
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

## Checksums

Adapted from the [Faker library](https://github.com/joke2k/faker/blob/master/faker/providers/credit_card/__init__.py#L99).

```{code-cell}
def credit_card_checksum(number: str):
    luhn_lookup = {
        "0": 0,
        "1": 2,
        "2": 4,
        "3": 6,
        "4": 8,
        "5": 1,
        "6": 3,
        "7": 5,
        "8": 7,
        "9": 9,
    }

    # Calculate sum
    length = len(number)
    reverse = number[::-1]
    tot = 0
    pos = 0
    while pos < length - 1:
        tot += luhn_lookup[reverse[pos]]
        if pos != (length - 2):
            tot += int(reverse[pos + 1])
        pos += 2
    # Calculate check digit
    check_digit = (10 - (tot % 10)) % 10
    return str(check_digit)

credit_card_checksum("123")  # Not correct yet
```



## Length Encodings


