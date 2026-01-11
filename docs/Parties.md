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

(sec:parties)=
# Defining Network Parties

In the [previous chapter](sec:protocols), we have seen how to define and test protocol interactions with Fandango.
In this chapter, we describe additional ways to control communication behavior.

## Party Classes

All the communication between Fandango and its parties takes place via dedicated _classes_.
In fact, prefixes like `Server` and `Client` in [protocol testing](sec:protocols) or `In` and `Out` when [checking outputs](sec:outputs) all stand for predefined `FandangoParty` classes that implement a set of methods to establish communication.

The `FandangoParty` class supports the following methods, detailed in the [`FandangoParty` reference](FandangoParty.md):




