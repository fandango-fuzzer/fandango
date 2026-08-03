# Security Policy

## Supported Versions

Security fixes are made against the latest released version of Fandango. If you
are reporting a vulnerability, please check first that it still reproduces on
the current release.

## Reporting a Vulnerability

**Please report vulnerabilities privately, through GitHub, not as a public
issue.**

Use the repository's private reporting form:

**<https://github.com/fandango-fuzzer/fandango/security/advisories/new>**

You can also reach it from the repository's **Security** tab, under **Report a
vulnerability**. You need a GitHub account, and the report is visible only to
you and the maintainers.

We prefer this over email because it keeps the report, our questions, the fix,
and the eventual advisory together in one private thread, and because it lets us
request a CVE and credit you directly from that thread when the time comes.

Please include:

- a description of the vulnerability and why you believe it is one,
- steps to reproduce it, ideally with the smallest `.fan` spec or command that
  triggers it,
- the version of Fandango affected (`fandango --version`), plus your Python
  version and operating system,
- the impact you think it has, and any conditions required to exploit it.

If you cannot use GitHub's form for any reason, contact
[fandango-fuzzer@protonmail.com](mailto:fandango-fuzzer@protonmail.com) instead.
Please do not include exploit details in a first email; just say that you have
something to report and we will arrange a private channel.

### What to expect

- **Within 48 hours**: we acknowledge that we received your report.
- **Within 7 days**: an initial assessment, whether we consider it a
  vulnerability, and a rough timeline.
- **Ongoing**: we keep you updated in the advisory thread as we work on a fix.

Please give us a reasonable opportunity to fix the issue before disclosing it
publicly. If you plan to publish on a fixed date, tell us early so we can work
to it.

## Coordinated Disclosure

Once a vulnerability is verified and fixed, we will:

1. Publish a security advisory describing the issue and the affected versions.
2. Credit you for the report, unless you would rather stay anonymous. Tell us
   which you prefer.
3. Release a fixed version and note the advisory in the
   [release notes](https://fandango-fuzzer.github.io/ReleaseNotes.html).

## Scope

Fandango is a **testing tool**. It runs specifications you provide, and a `.fan`
specification can contain arbitrary Python by design, which it executes. Running
an untrusted specification is therefore equivalent to running untrusted code,
and that is expected behaviour rather than a vulnerability.

Reports we are interested in include, for example, Fandango being made to
execute code or access resources that the specification it was given did not
call for, a crash reachable from untrusted *input data* rather than from an
untrusted specification, or a vulnerability in how Fandango handles credentials
or network connections during protocol testing.

If you are unsure whether something is in scope, report it anyway and say what
you are unsure about. We would rather see it.

## Security Measures

To help keep this project secure, we:

- keep dependencies current, with automated updates via Dependabot,
- run CodeQL analysis on the codebase,
- run the full test suite across supported Python versions on every pull
  request.

Thank you for helping keep Fandango secure.
