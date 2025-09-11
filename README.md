# FANDANGO for IO grammars: Evolving Language-Based Testing for Protocols

This project extends FANDANGO that is a language-based fuzzer that leverages formal input specifications (grammars) combined with constraints to generate diverse sets of valid inputs for programs under test.
This project adds support for IO grammars, which allow specifying the input and output of a protocol in a single grammar.
With this addition, FANDANGO gains the ability to participate in a protocol as one or more participants. 
It can now generate syntactically and semantically valid inputs as those participants and also receive, parse and validate received messages from other participants against a specification. 

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Evaluation subjects](#evaluation-subjects)
- [License](#license)

## Introduction

Generating software tests faces two fundamental problems.
First, one needs to _generate inputs_ that are syntactically and semantically correct, yet sufficiently diverse to cover behavior.
Second, one needs an _oracle_ to _check outputs_ whether a test case is correct or not.
Both problems become apparent in _protocol testing_, where inputs are messages exchanged between parties, and outputs are the responses of these parties.

We propose a novel approach to protocol testing that combines input generation and output checking in a single framework. We introduce _IO grammars_ as the first means to completely specify the syntax and semantics of protocols, including messages, states, and interactions.
Our implementation, based on the FANDANGO framework, takes a single \IO grammar, and can act as a _test generator,_ as a _mock object,_ and as an _oracle_ for a _client,_ a _server,_ or both (or actually any number of parties), a versatility not found in any existing tool or formalism.
User-defined _constraints_ can have the generator focus on arbitrary protocol features; _$k$-path guidance_ systematically covers states, messages, responses, and value alternatives in a unified fashion.


## Installation
To install FANDANGO, you can use the provided makefile. This will install the package and its dependencies.

```bash
make install
```
Please check the original README at /README_ORIGINAL.md for further information about the original FANDANGO framework.


## Evaluation subjects
See our evaluation subjects at
```
evaluation/experiments ...
    .../chatgpt
    .../dns
    .../ftp
    .../smtp
    .../dune
```
for examples on how to use FANDANGO for different protocols and on how to define an IO grammar.

## License

This project is licensed under the European Union Public Licence V. 1.2. See the [LICENSE](LICENSE.md) file for details.