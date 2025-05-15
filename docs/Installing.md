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

(sec:installing)=
# Installing Fandango

## Installing Fandango for Normal Usage

% ```{warning}
% While Fandango is in beta, only development versions can be installed.
% ```

Fandango comes as a Python package. To install Fandango, run the following command:

```shell
$ pip install fandango-fuzzer
```

To test if everything worked well, try

```shell
$ fandango --help
```

which should give you a list of options:

```{code-cell}
:tags: ["remove-input"]
!fandango --help
assert _exit_code == 0
```

% If this did not work, try
% 
% ```
% $ python -m fandango --help
% ```
% 
% instead, and replace `fandango` with `python -m fandango` to invoke fandango.


## Installing Fandango for Development

```{caution}
This will get you the very latest version of Fandango, which may be unstable. Use at your own risk.
```

Refer to the [Getting Started with Development Guide](sec:getting-started-with-development) for instructions on how to prepare an environment to work on Fandango.