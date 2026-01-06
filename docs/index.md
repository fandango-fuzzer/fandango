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
sd_hide_title: true
---

# Fuzzing with Fandango

::::{grid}
:reverse:
:gutter: 3 4 4 4
:margin: 1 2 1 2

:::{grid-item}
:columns: 12 4 4 4

```{image} Icon-reverse.png
:width: 200px
:class: sd-m-auto
```

:::

:::{grid-item}
:columns: 12 8 8 8
:child-align: justify
:class: sd-fs-5

```{rubric} Fuzzing with Fandango
```

Fandango produces myriads of _high-quality random inputs_ to test programs, giving users unprecedented control over format and shape of the inputs.

```{button-ref} Tutorial
:ref-type: doc
:color: primary
:class: sd-rounded-pill

Get Started
```

:::

::::

----------------

::::{grid} 1 2 2 3
:gutter: 1 1 1 2

:::{grid-item-card} <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -960 960 960" width="2em" fill="#5f6368"><path d="m787-145 28-28-75-75v-112h-40v128l87 87Zm-587 25q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h560q33 0 56.5 23.5T840-760v268q-19-9-39-15.5t-41-9.5v-243H200v560h242q3 22 9.5 42t15.5 38H200Zm0-120v40-560 243-3 280Zm80-40h163q3-21 9.5-41t14.5-39H280v80Zm0-160h244q32-30 71.5-50t84.5-27v-3H280v80Zm0-160h400v-80H280v80ZM720-40q-83 0-141.5-58.5T520-240q0-83 58.5-141.5T720-440q83 0 141.5 58.5T920-240q0 83-58.5 141.5T720-40Z"/></svg> At a Glance
% icons from https://fonts.google.com/icons
% overview icon

Specify the format of your input data in a single file, combining [_grammars_](sec:first-spec) (for input syntax) and [_constraints_](sec:constraints) (for arbitrary input features).
Constraints come as _Python code_, so there are no limits to what you can specify.

+++
[About Fandango »](sec:about)
:::




:::{grid-item-card} <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -960 960 960" width="2em" fill="#5f6368"><path d="M200-120q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h560q33 0 56.5 23.5T840-760v560q0 33-23.5 56.5T760-120H200Zm0-640v560h560v-560h-80v280l-100-60-100 60v-280H200Zm0 560v-560 560Z"/></svg> Tutorial
% developer_guide icon

Produce valid inputs at high speeds, quickly covering the entire input space.
Test with [_extreme_ and _uncommon_ values](sec:strategies), uncovering bugs before your users do.
Tie in [Python data generators and fakers](sec:generators) to obtain realistic inputs.


+++
[Tutorial »](sec:tutorial)
:::



:::{grid-item-card} <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -960 960 960" width="2em" fill="#5f6368"><path d="M480-60q-72-68-165-104t-195-36v-440q101 0 194 36.5T480-498q73-69 166-105.5T840-640v440q-103 0-195.5 36T480-60Zm0-104q63-47 134-75t146-37v-276q-73 13-143.5 52.5T480-394q-66-66-136.5-105.5T200-552v276q75 9 146 37t134 75Zm0-436q-66 0-113-47t-47-113q0-66 47-113t113-47q66 0 113 47t47 113q0 66-47 113t-113 47Zm0-80q33 0 56.5-23.5T560-760q0-33-23.5-56.5T480-840q-33 0-56.5 23.5T400-760q0 33 23.5 56.5T480-680Zm0-80Zm0 366Z"/></svg> Reference
% local_library icon; was {material-regular}`local_library;2em`

Check program [outputs](sec:outputs) for correctness.
Test and mock clients and servers using [protocol testing](sec:protocols).
Create and check _binary_ strings, using [bit fields and bit sequences](sec:binary).
Use [regular expressions](sec:regexes) for quick and easy specifications.

+++
[Reference »](sec:reference)
:::

::::

<div style="display: flex; justify-content: center;">
<iframe style="aspect-ratio: 16 / 9; width: 100% !important;" src="https://www.youtube.com/embed/JXMk-XhuKPY"></iframe>
</div>


----------------

```{include} Footer.md
