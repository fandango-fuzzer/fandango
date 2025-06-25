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

(sec:converters)=
# Converting ANTLR and Other Input Specs

Often, you may already have an input format specification available, but not (yet) in Fandango `.fan` format.
Fandango's `convert` command allows you automatically translate common input specifications into `.fan` files - at least most of it.

```{margin}
For instance, _executable code_ in ANTLR and 010 specs can only be partially converted at best.
```

```{important}
All these converters are _lossy_ - that is, some features of the original specifications may not be converted into Fandango.
Hence, the idea is that you use converted formats as a base for further manual editing and checking.
```

```{note}
All these formats define the _syntax_ of input files, typically for the purpose of _parsing_.
To _produce_ inputs that are also _semantically_ valid, you will often have to augment the `.fan` files with [constraints](sec:constraints) to make them semantically valid, too.
```

```{admonition} Under Construction
:class: attention
All these converters are experimental at this point.
```

(sec:antlr2fan)=
## Converting ANTLR Specs

Fandango allows you to automatically convert ANTLR grammar specifications (`.g4`, `.antlr`) into Fandango `.fan` files.
ANTLR is a very popular parser generator; a [wide large collections of ANTLR grammars](https://github.com/antlr/grammars-v4) is available.

Simply use the command `fandango convert`, followed by the ANTLR file to be converted.

As an example, consider this simple [`Calculator.g4`](../src/fandango/converters/antlr/Calculator.g4) ANTLR file:

```{code-cell}
:tags: ["remove-input"]
!expand -t4 ../src/fandango/converters/antlr/Calculator.g4
```

Invoking `fandango convert` produces an (almost) equivalent Fandango `.fan` file:

```{margin}
The `fandango convert` command determines the spec language from the file extension:

* `.antlr` and `.g4` - ANTLR
* `.bt` and `.010` - 010 Binary Templates
* `.dtd` - DTDs
* `.fan` - `.fan` files

If your file has another file name, you can use the `--from` option (say, `--from=antlr`) to specify a specific format.
```

```shell
$ fandango convert Calculator.g4
```

```{code-cell}
:tags: ["remove-input"]
!fandango convert ../src/fandango/converters/antlr/Calculator.g4
```

Note the `NOTE` comment at the bottom: The ANTLR lexer action `skip` has no equivalent in Fandango; hence `WS` elements will neither be skipped nor generated.

Still, we can use this grammar to produce expressions.
Note the usage of the `-o` option to specify an output file and the `--start` option to specify a start symbol.

```shell
$ fandango convert -o Calculator.fan Calculator.g4
$ fandango fuzz -f Calculator.fan --start='<expression>' -n 10
```

```{code-cell}
:tags: ["remove-input"]
!fandango convert -o Calculator.fan ../src/fandango/converters/antlr/Calculator.g4
!fandango fuzz -f Calculator.fan --start='<expression>' -n 10
assert _exit_code == 0
```

```{note}
Most features of ANTLR that cannot be represented in Fandango will be marked by `NOTE` comments.
These include

* Actions
* Modifiers
* Clauses such as `return` or `throws`
* Exceptions
* Predicate options
* Element options
* Negations (`~`) over complex expressions
```


(sec:bt2fan)=
## Converting 010 Binary Templates

Fandango provides some basic support for converting Binary Templates (`.bt`, `.010`) for the 010 Editor.
A [large collection of binary templates for various binary formats](https://www.sweetscape.com/010editor/repository/templates/) is available.

Again, simply use the command `fandango convert`, followed by the binary template file to be converted.

Our [GIF example](sec:gif) is automatically created from a GIF binary template.

```{note}
010 Binary Templates can contain _arbitrary code_ that will be executed during parsing.
Fandango will recognize a number of common patterns; features that will require manual work include

* Checksums
* Complex length encodings
```

```{note}
The `fandango convert` command provides two options to specify _bit orderings_, should the `.bt` file not already do so.

* `--endianness=(little|big)` and
* `--bitfield-order=(left-to-right|right-to-left)` 
```

(sec:dtd2fan)=
## Converting DTDs

A Document Type Definition (DTD, `.dtd`) specifies the format of an XML file.
Fandango can convert these into `.fan` files, enabling the production of XML files that conform to the DTD.

Again, simply use the command `fandango convert`, followed by the binary template file to be converted.

```{note}
As with Binary Templates, Fandango will recognize a number of common patterns, but not all.
```

In the generated `.fan` file, you can customize every single element in its context.
As an example, consider this [`svg11.fan`](../src/fandango/converters/dtd/svg11.fan) file which specializes individual elements of a [`svg.fan`](../src/fandango/converters/dtd/svg11.fan) file generated from an [SVG DTD](../src/fandango/converters/dtd/svg11-flat-20110816.dtd).
The DTD by itself does not specify types of individual fields, so we do this here:

```{margin}
If you find that this is long, consider that SVG is actually a very complex format.
```

```{code-cell}
:tags: ["remove-input"]
!expand -t4 ../src/fandango/converters/dtd/svg11.fan
```

Once this is all set, we can use this to test SVGs with extreme values, as in this [`svgextreme.fan`](../src/fandango/converters/dtd/svgextreme.fan) example:

```{code-cell}
:tags: ["remove-input"]
!expand -t4 ../src/fandango/converters/dtd/svgextreme.fan
```

(sec:fan2fan)=
## Converting `.fan` files

With `fandango convert`, you can also "convert" `.fan` files.
This results in a "normalized" format, where all comments and blank lines have been removed.
If we send this input to `fandango convert`:

```{code-cell}
:tags: ["remove-input"]
!echo '# A fine file to produce person names'; cat persons-faker.fan
```

then we get

```shell
$ fandango convert persons-faker.fan
```

```{code-cell}
:tags: ["remove-input"]
!fandango convert persons-faker.fan
```

```{note}
This feature can be useful to detect semantic changes in `.fan` files.
```