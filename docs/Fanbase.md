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

(sec:fanbase)=
# Fandango and Fanbase

[Fanbase](https://github.com/fandango-fuzzer/fanbase) is a collection of ready-made Fandango specs for many file formats. Instead of writing a spec for PNG, GIF, or TIFF yourself, you name the format and Fandango fetches the spec and produces inputs.

```{versionadded} 1.3
The `-F` option and the `fanbase` command require Fandango 1.3 or later.
```

## Producing Inputs from a Fanbase Spec

The `-F` option works like `-f`, but its argument is the name of a Fanbase spec rather than a file:

```shell
$ fandango fuzz -F png -n 10
```

This

1. looks up the default PNG spec, `png`, in the Fanbase registry;
2. installs it in Fandango's standard library location, unless the installed copy is already up to date; and
3. produces 10 PNG files, `png-inputs/fandango-0000.png` to `png-inputs/fandango-0009.png`.

Because the format is known, you do not need `-x` for the file name extension, and you do not need `-o` or `-d` to say where the files go. If you give neither, Fandango writes into a fresh directory named after the spec (`png-inputs`, then `png-inputs-2`, and so on).

Everything else works as it does with `-f`. You can set the population size or a random seed, write to one file, or hand each input to a program to test (which then gets a file with the right extension):

```shell
$ fandango fuzz -F png -n 1000 -d pngs --population-size=50
$ fandango fuzz -F gif --random-seed=42 -n 1 -o one-gif.gif
$ fandango fuzz -F png -n 100 file
```

## Choosing a Spec

Every format has a default spec, named after the format. Other specs for the same format are named `<format>-<what makes it different>`. Use `fanbase list` to see what is available:

```shell
$ fanbase list
  bmp   3 specs
  gif   3 specs
  jpeg  3 specs
  png   6 specs
  tiff  4 specs
  webp  3 specs

$ fanbase list png
 *png             Valid PNGs of every colour type with all the standard chunks
  png-32x32       32x32 RGB PNG with lengths and CRCs written as constraints
  png-apng        Animated PNG (APNG) with the usual ancillary chunks
  png-boundary    Same as png, with values taken from the edges of what the format allows
  png-container   PNG chunk structure only; image data is arbitrary bytes, so most files do not decode
  png-extensions  1x1 PNGs with the registered extension chunks, APNG included

* installed
```

A spec other than the default is requested by its name:

```shell
$ fandango fuzz -F png-apng -n 10 -d apngs
```

`fanbase show` tells you more about a spec: its description, version, file name extensions, and the Python packages it needs.

```shell
$ fanbase show png-apng
```

## Customizing a Fanbase Spec

To change a Fanbase spec, write a spec of your own that _includes_ the Fanbase spec and _redefines_ the rules you want to change. Installed specs are found by `include()` under `<format>/<name>.fan`. For instance, the default PNG spec chooses between five colour types in a rule `<image>`. To produce only RGB images, create `rgb.fan`:

```
include("png/png.fan")

<image> ::= <png_truecolor>
```

and combine it with the Fanbase spec:

```shell
$ fandango fuzz -F png -f rgb.fan -n 10
```

Fanbase specs come first, so rules in files given with `-f` override them. If the spec is already installed, `fandango fuzz -f rgb.fan -x .png -n 10` works as well.

## Where Specs Are Installed

Specs are installed in the first of these directories, which are also the ones Fandango searches for `include()`:

1. the first directory in `$FANDANGO_PATH`;
2. `$XDG_DATA_HOME/fandango`; or, if that is not set,
3. `~/Library/Fandango` (macOS) or `~/.local/share/fandango` (other systems).

An installed spec is `<format>/<name>.fan` in that directory, together with a copy of its metadata, `<format>/<name>.yml`.

Each time you use `-F`, Fandango asks the registry whether the installed copy is still current, and fetches the spec again if it has changed. Only the spec you ask for is downloaded. If the registry cannot be reached, Fandango uses the installed copy and warns you, so test runs do not depend on the network.

A few specs import third-party Python packages, which `fanbase list` and `fanbase show` list for each spec. When you use such a spec with `-F`, or install it with `fanbase install`, the packages that are missing are installed for you, with `pip` (or `uv pip`, in an environment that has no `pip`), into the environment Fandango runs in. Packages that are already installed are left alone, so if you prefer to manage packages yourself, install them beforehand. If the installation fails, Fandango stops and says which package it could not install. Most specs only need the Python standard library.

## Using Another Registry

By default, specs come from the public registry at `https://github.com/fandango-fuzzer/fanbase`. To use a different one, a local checkout or a URL, set `FANBASE_REGISTRY`:

```shell
$ export FANBASE_REGISTRY=~/code/my-registry
$ fandango fuzz -F png -n 10
```

## Command Reference

### `fandango -F`

`-F NAME`, `--fanbase-file NAME`
: Use the Fanbase spec `NAME` (such as `png` or `png-apng`). Can be given multiple times. Available with all commands that take `-f`. Unless given, `-x` is set to the format's file name extension.

### `fanbase`

The `fanbase` command is installed together with Fandango.

`fanbase list [FORMAT]`
: List the formats, or the specs of a format. Installed specs are marked with `*`.

`fanbase show NAME`
: Show a spec's metadata.

`fanbase install NAME...`
: Install specs without using them, together with the Python packages they need. `--into DIR` installs into another directory. `--no-requirements` leaves the Python packages to you and only prints what the specs need. Installing a spec that is up to date does nothing.

`fanbase install --all`
: Install every spec in the registry, which is handy for a machine that should work without network access later.

`fanbase update [NAME...]`
: Update the given specs, or all installed specs, to the registry's latest versions, and install any Python packages the new versions need. Takes `--no-requirements` as well.

`fanbase reindex [--check]`
: For registry maintainers: refresh the `metadata.yml` files and `index.yml` of a local registry. With `--check`, only report what is out of date.

`fanbase --registry PATH-OR-URL COMMAND`
: Use a registry other than the default, for this command.
