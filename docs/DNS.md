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

(sec:dns)=
# Case Study: DNS

This Fandango specification allows testing FTP clients and servers.
It demonstrates

* how a nontrivial protocol with bit-level _binary_ commands is implemented;
* how to use constraints to _validate_ responses; and
* how to embed _compression_ and _decompression_ functions.

The [`dns.fan`](.fan) Fandango DNS spec is available for download.
To test it with Fandango as client querying the public Cloudflare DNS server 1.1.1.1 on the default DNS port 53, invoke Fandango as

```shell
$ fandango -v talk -n 1 -f dns.fan --client udp://1.1.1.1:53
```

```{versionadded} 1.1
These features are available in Fandango 1.1 and later.
```

## A DNS Exchange

At an abstract level, the DNS _protocol_ is pretty simple.
A _Client_ sends a DNS request to the server (via UDP, by default on port 53), and gets a DNS response.
For instance, as of January 2026, the host `example.com` had the IP address `104.18.27.120`:

```{mermaid}
sequenceDiagram
Client ->> Server: example.com
Server ->> Client: 104.18.27.120
```

This is also how the exchange is modeled in `dns.fan`:

```python
<start> ::= <exchange>
<exchange> ::= <Client:dns_req> <Server:dns_resp>
```

Alas, the devil is in the details.
Let's dig a bit deeper.


## DNS Requests

A DNS request consists of a _header_ and a number of _questions_.
The actual number of questions is transmitted in a header field `<req_qd_count>`.

```python
<dns_req> ::= <header_req> <question>{byte_to_int(<req_qd_count>)}
```

We decode `<req_qd_count>` using a function `byte_to_int()`:

```python
# Convert a 2-byte byte array to an integer
def byte_to_int(byte_val):
    return int(unpack('>H', bytes(byte_val))[0])
```

```{note}
We do not model DNSSEC and other DNS extensions.
```



### Request Headers

The header consists of a number of fields as defined below.
Note the mix of bits and bytes, which is common in DNS messages.

```python
<header_req> ::= <h_id> 0 <h_opcode_standard> 0 0 <h_rd> 0 0 <bit> 0 <h_rcode_noerror> <req_qd_count> 0{16} 0{16} 0{16}
```

The ID is an identifier of two bytes.
When sending the request, we choose a random value:

```python
<h_id> ::= <byte><byte>
```

The remaining fields are set to fixed values:

```python
<h_opcode_standard> ::= 0 0 0 0
<h_rd> ::= 1 # 0 causes server failure with cname
<req_qd_count> ::= <byte>{2} := pack(">H", 1)
```


### Request Questions

Now for the actual DNS questions.

```python
<question> ::= <q_name> <q_type> <rr_class>
```

```{note}
`<q_name>` is where the host name (say, `example.com`) is sent to the DNS server.
```


#### Request Names

A request name is terminated by 8 zero bits (i.e., a NUL byte).

```python
<q_name> ::= <q_name_written> 0{8}
```

The name is encoded as

* an octet specifying the _length_ of the name,
* followed by a sequence of bytes holding the actual name.

```python
<q_name_written> ::= (<label_len_octet> <byte>{byte_to_int(b'\x00' + bytes(<label_len_octet>))})+ := gen_q_name()
<label_len_octet> ::= <byte>
```

To generate domain names to query, we either 

* use the Faker library to obtain a random host name (which likely is not known to the DNS server),
* or we use 'github.com' or 'cispa.de', which should be known to a DNS server.

The individual parts (say, `github` and `com`) are also length-encoded, i.e. there is a leading byte telling the length of the part, followed by the part.

```{code-cell}
from random import randint
from faker import Faker
fake = Faker()

def gen_q_name():
    result = b''
    rand = randint(0, 2)
    if rand == 0:
        domain_name = 'github.com'
    elif rand == 1:
        domain_name = 'cispa.de'
    else:
        domain_name = fake.domain_name()

    domain_parts = domain_name.split('.')
    for part in domain_parts:
        result += len(part).to_bytes(1, 'big')
        result += part.encode('iso8859-1')

    return result
```

Here are some examples of `gen_q_name()`:

```{code-cell}
[gen_q_name() for _ in range(5)]
```



#### Request Types

We can request the following records from the DNS server:

* `CNAME` - return an "official" host name (or a redirect);
* `A` - return the IP address (the typical use of a DNS server); and
* `NS` - return the name server (a DNS server) for the given domain.

These are encoded using bit sequences as follows:

```python
<q_type> ::= <type_id_cname> | <type_id_a> | <type_id_ns>
<type_id_cname> ::= 0{13} 1 0 1
<type_id_a> ::= 0{15} 1
<type_id_ns> ::= 0{14} 1 0
```

#### Request Class

All our DNS requests refer to the class `IN` (Internet).

```python
<rr_class> ::= 0{15} 1 # Class IN (Internet)
```

With that, the definition of our requests are complete.


## DNS Responses

Now for the responses of the DNS server.

```python
<dns_resp> ::= <header_resp> <question_section> <answer_an_section> <answer_au_section> <answer_opt_section>
```

### DNS Response Headers

First, let us have a look at the response header.

```python
<header_resp> ::= <h_id> 1 <h_opcode_standard> <bit> 0 <h_rd> <h_ra> 0 <h_aa> 0 (<h_rcode_noerror> | <h_rcode_nxdomain>) <resp_qd_count> <resp_an_count> <resp_ns_count> <resp_ar_count>
```

Most of these fields have been defined above already, except for these:

```python
<h_aa> ::= <bit>  # 1 if authoritative answer
<h_ra> ::= <bit>  # 1 if recursion is available
```

The most interesting part is the return code, telling success (or non-success) of the query:

```python
<h_rcode> ::= <h_rcode_noerror> | <h_rcode_formerr> | <h_rcode_servfail> | <h_rcode_nxdomain> | <h_rcode_notimp> | <h_rcode_refused> | <h_rcode_other>
<h_rcode_noerror>  ::= 0 0 0 0  # NOERROR - no error
<h_rcode_formerr>  ::= 0 0 0 1  # FORMERR - format error
<h_rcode_servfail> ::= 0 0 1 0  # SERVFAIL - server failure
<h_rcode_nxdomain> ::= 0 0 1 1  # NXDOMAIN - non existent domain
<h_rcode_notimp>   ::= 0 1 0 0  # NOTIMP - not implemented
<h_rcode_refused>  ::= 0 1 0 1  # REFUSED - query refused
<h_rcode_other> ::= (1 <bit>{3, 3}) | (0 1 1 <bit>)
```

This is followed by four fields denoting the number of fields that follow.

```python
<resp_qd_count> ::= <bit>{16} := pack(">H", 1)
<resp_an_count> ::= <bit>{16} := pack(">H", randint(1, 2))
<resp_ns_count> ::= <bit>{16} := pack(">H", randint(0, 2))
<resp_ar_count> ::= <bit>{16} := pack(">H", randint(0, 2))
```


### DNS Response Question Section

The DNS server _replicates_ the original request in its response.
This is necessary as the UDP protocol can drop packets, so the response must clearly specify which request it refers to.
This has the same format as the original response.

```python
<question_section> ::= <question>{byte_to_int(<header_req>.<req_qd_count>)}
```

Note that we refer to the _original_ number of questions from the `<header_req>` request, not the number of questions stated in the response (which is equal anyway).
This is for efficiency reasons: The original number of questions is already defined, so we do not have to retrieve it from the server response.

The following constraint ensures that for each request/response pair,

* The recursion desired flag (RD) (`<h_rd>`) match;
* The DNS message identifier (ID) (`<h_id>`) match;
* The question that the response aims to answer is the same as the question in the request (`<question>`); and
* The question count in the response matches the question count in the request (`<req_qd_count>`).

Note that our constraint uses [old-style quantifiers](sec:old-quantifiers) for compatibility with previous Fandango versions.

% FIXME: Convert to new all()/any() quantifier syntax
```python
where forall <ex> in <start>.<exchange>:
    <ex>.<dns_resp>.<header_resp>.<h_rd> == <ex>.<dns_req>.<header_req>.<h_rd> and \
    <ex>.<dns_resp>.<header_resp>.<h_id> == <ex>.<dns_req>.<header_req>.<h_id> and \
    <ex>.<dns_resp>.<question_section>.<question> == <ex>.<dns_req>.<question> and \
    bytes(<ex>.<dns_resp>.<header_resp>.<resp_qd_count>) == bytes(<ex>.<dns_req>.<header_req>.<req_qd_count>)
```


### DNS Response Answer Section

The actual response is contained in these answers:

```python
<answer_an_section> ::= <answer_an>{byte_to_int(<resp_an_count>)}
<answer_au_section> ::= <answer_au>{byte_to_int(<resp_ns_count>)}
<answer_opt_section> ::= <answer_opt>{byte_to_int(<resp_ar_count>)}
```

#### AN Answers

The `AN` answer field `<answer_an>` contains the answer to the DNS question.
It can return an `A` record, a `CNAME` record, or an `NS` record (see above).

```python
<answer_an> ::= <q_name_optional> <answer_an_type>
<q_name_optional> ::= <q_name_written>? 0{8}
<answer_an_type> ::= (<type_a> |<type_cname> | <type_ns>)
```

##### Type A Answers

This is the answer to an `A` request querying the IP address of a hostname.

A `<type_a>` answer holds the `A` record of the requested domain.
The `<ip_address>` field (finally!) holds the requested IP address, as a sequence of four bytes.

```python
<type_a> ::= <type_id_a> <rr_class> <a_ttl> 0{13} 1 0 0 <ip_address>
<type_id_a> ::= 0{15} 1
<a_ttl> ::= 0 <bit>{7} <byte>{3}
<ip_address> ::= <byte>{4}
```

```{note}
`<ip_address>` is the place where the IP address (e.g. 104.18.27.120) is sent back.
```

```{note}
Our DNS server only supports IP version 4.
```


##### Type CNAME Answers

This is the answer to a `CNAME` request, asking for an "official" host name. `<q_name>` is the host name returned.

```python
<type_cname> ::= <type_id_cname> <rr_class> <a_ttl> <a_rd_length> <q_name>
<a_rd_length> ::= <byte>{2} := pack(">H", randint(0, 0))
```

`<type_cname>` responses must have the correct length in the `<a_rd_length>` field (r data length), which corresponds to the following `<q_name>` field.

Our constraint uses [old-style quantifiers](sec:old-quantifiers) for compatibility with previous Fandango versions.

```python
where forall <t> in <type_cname>:
    bytes(<t>.<a_rd_length>) == pack('>H', len(bytes(<t>.<q_name>)))
```

##### Type NS Answers

Finally, `<type_ns>` is the answer to an `NS` request, returning the name server for the given domain.

```python
<type_ns> ::= <type_id_ns> <rr_class> <a_ttl> <a_rd_length> <a_rdata>{int(unpack('>H', bytes(<a_rd_length>))[0])}
<a_rdata> ::= <byte>  # We don't go into further details here.
```

#### AU Answers

An `AU` answer returns the name server for a domain. We don't go into details here.

```python
<answer_au> ::= <q_name_optional> <type_soa>
<type_soa> ::= <type_id_soa> <rr_class> <a_ttl> <a_rd_length> <a_rdata>{int(unpack('>H', bytes(<a_rd_length>))[0])}
<type_id_soa> ::= 0{13} 1 1 0
```

#### OPT Answers

An `OPT` answer returns optional additional details. We don't go into details here.

```python
<answer_opt> ::= <q_name_optional> (<type_opt>|<type_a>)
<type_opt> ::= <type_id_opt> <udp_payload_size> <a_ttl> <a_rd_length> <a_rdata>{int(unpack('>H', bytes(<a_rd_length>))[0])}
<type_id_opt> ::= 0{10} 1 0 1 0 0 1
<udp_payload_size> ::= <bit>{16}
```


#### Consistency in Responses

We check if a DNS response answers the corresponding DNS question using the `verify_transitive()` function.

The second part of the `or` clause `bytes(<a>.<answer_an_type>)[0:2]...` also checks this, but only for direct answers without allowing transitive response chains.
This allows Fandango optimizations to be used to generate a valid answer more efficiently.

Our constraint uses [old-style quantifiers](sec:old-quantifiers) for compatibility with previous Fandango versions.

% FIXME: Convert to new all()/any() quantifier syntax
```python
where forall <ex> in <start>.<exchange>:
    forall <a> in <ex>.<dns_resp>.<answer_an_section>.<answer_an>:
        exists <q> in <ex>.<dns_req>.<question>:
            verify_transitive(<q>, <ex>.<dns_resp>) or \
            (bytes(<a>.<answer_an_type>)[0:2] == bytes(<q>.<q_type>) and 
             bytes(<a>.<q_name_optional>) == bytes(<q>.<q_name>))
```

The `verify_transitive()` function gets a question and the response section of a DNS response and verifies if the response does answer the question.
This also handles responses that are transitive.
If, for example the question is

* for a type `A` record for `example.com` and
* the response contains a `CNAME` record pointing `example.com` to `alias.com` and then an `A` record for `alias.com`,

then `verify_transitive()` will verify that the response correctly answers the original question through the `CNAME` redirection.

```python
def verify_transitive(question, response):
    type_byte = bytes(question.find_direct_trees(NonTerminal("<q_type>"))[0])
    allowed_names = [bytes(question.find_direct_trees(NonTerminal("<q_name>"))[0])]

    for ans in response.find_all_trees(NonTerminal("<answer_an>")):
        if (bytes(ans.children[1])[0:2] == pack('>H', 5) and
            bytes(ans.find_direct_trees(NonTerminal("<q_name_optional>"))[0]) in allowed_names):
            allowed_names.append(bytes(ans.children[1].children[0].children[4])) # <type_cname>.<q_name>

    for ans in response.find_all_trees(NonTerminal("<answer_an>")):
        if (bytes(ans.children[1])[0:2] == type_byte and
            bytes(ans.find_direct_trees(NonTerminal("<q_name_optional>"))[0]) in allowed_names):
            return True

    return False
```

## Compression and Decompression

The DNS protocol maintains a complex system for compressing requests.
We implement this by overriding the `NetworkParty` `send()` and `receive()` functions such that

* all sent messages are compressed (`compress_msg()`), and
* all received messages are decompressed (`decompress_msg()`).

```{margin}
We give the new class the same name `NetworkParty` so we can stick to original party names.
```

```python
class NetworkParty(NetworkParty):
    def receive(self, message: str | bytes, sender: Optional[str]) -> None:
        super().receive(decompress_msg(message), sender)

    def send(self, message: str | bytes, recipient: Optional[str]) -> None:
        super().send(compress_msg(message.to_bytes(encoding="utf-8")), recipient)
```



### Compression

When receiving a DNS package, some domain names may occur multiple times.
To reduce traffic, DNS allows encoding domain names suffixes such that they _refer_ to _suffixes_ of earlier messages.
For instance, if the first answer contains `host.example.com`, then a subsequent `example.com` can be replaced by a pointer into this answer.
Such pointers are represented by _offsets_ starting from the first answer.

We use the function `msg_suffix()` to identify such compressions.
`msg_suffix()` takes an (encoded) domain name in `<q_name>` format and returns a list of tuples (offset, suffix) for a DNS name.
Here,

* `suffix` is a possible suffix of `name`
* `offset` is the number of characters into `name` where `suffix` begins

```{code-cell}
def msg_suffix(name):
    suffixes = []
    len_idx = 0
    prefix_len = name[len_idx]
    while prefix_len != 0:
        suffixes.append((len_idx, name[len_idx:]))
        len_idx = len_idx + prefix_len + 1
        prefix_len = name[len_idx]

    return suffixes
```

Here is an example of `msg_suffix()`:

```{code-cell}
name = b'\x07example\x03com\x00'
msg_suffix(name)
```

The returned suffix `(8, b'\x03com\x00')` starts 8 bytes into the passed `name`.

```{code-cell}
name[8:]
```



We apply the DNS name compression algorithm to a DNS name starting at `curr_idx` within the uncompressed message.
`suffix_dict` is a dictionary mapping a known DNS suffix names to their offsets within the already analyzed compressed part of the message.

% FIXME: Add types
% FIXME: Add full docstrings, with :param: and :return:

```python
def compress_name(uncompressed: bytes, curr_idx: int,
                  len_reduction: int, suffix_dict: dict[bytes, int]) -> tuple[bytes, int, int]:
    """
    Compress a single name in a DNS message.
    :param: uncompressed - the message before compression
    :param: curr_idx - the current index in `compress_msg()` (see below)
    :param: len_reduction - how many bytes we already have compressed
    :param: suffix_dict - the suffixes encoded so far
    :return: a tuple (new_name, length, len_reduction) - the compressed name, its length, the new length reduction
    """
    name_len = 0
    while uncompressed[curr_idx + name_len] != 0:
        name_len += uncompressed[curr_idx + name_len] + 1
    name_len += 1
    b_name = uncompressed[curr_idx:(curr_idx+name_len)]

    if name_len == 1:
        return b_name, name_len, len_reduction

    for n_offset, suffix in msg_suffix(b_name):
        if suffix in suffix_dict:
            cpr_ptr = suffix_dict[suffix]
            bin_ptr = pack('>H', (192 << 8) | cpr_ptr)
            new_name = b_name[:n_offset] + bin_ptr
            len_reduction += len(b_name) - len(new_name)
            return new_name, name_len, len_reduction
        else:
            offset_name_start = curr_idx
            suffix_dict[suffix] = offset_name_start + n_offset - len_reduction
            return b_name, name_len, len_reduction
```

Now for the actual compression.
`compress_msg()` compresses a full DNS message applying the DNS name compression algorithm to all names present in the message.

```python
def compress_msg(uncompressed: bytes) -> bytes:
    """
    Compress a single DNS message.
    """
    qd_count = byte_to_int(uncompressed[4:6])
    an_count = byte_to_int(uncompressed[6:8])
    ns_count = byte_to_int(uncompressed[8:10])
    ar_count = byte_to_int(uncompressed[10:12])
    compressed = uncompressed[0:12]
    curr_idx = 12

    suffix_dict = dict()
    len_reduction = 0
    for i in range(qd_count):
        name, decompressed_len, len_reduction = compress_name(uncompressed, curr_idx, len_reduction, suffix_dict)
        compressed = compressed + name
        curr_idx += decompressed_len
        compressed += uncompressed[curr_idx:curr_idx+4]
        curr_idx += 4

    for i in range(an_count + ns_count + ar_count):
        name, decompressed_len, len_reduction = compress_name(uncompressed, curr_idx, len_reduction, suffix_dict)
        compressed = compressed + name
        curr_idx += decompressed_len
        rr_type = uncompressed[curr_idx:curr_idx+2]
        compressed += rr_type
        rr_type = byte_to_int(rr_type)
        curr_idx += 2
        compressed += uncompressed[curr_idx:curr_idx+6]
        curr_idx += 6
        r_data_len = byte_to_int(uncompressed[curr_idx:curr_idx+2])
        curr_idx += 2

        if rr_type == 5: # If CNAME entry
            name, decompressed_len, len_reduction = compress_name(uncompressed, curr_idx, len_reduction, suffix_dict)
            compressed += pack('>H', len(name))
            compressed = compressed + name
            curr_idx += decompressed_len
        else:
            compressed += uncompressed[curr_idx-2:curr_idx]
            compressed += uncompressed[curr_idx:curr_idx+r_data_len]
            curr_idx += r_data_len

    return compressed
```

### Decompression

`decompress_name()` decompresses a DNS name starting at `name_idx` within the compressed message.

```python
def decompress_name(compressed: bytes, name_idx: int) -> tuple[bytes, int]:
    """
    Decompress the package `compressed` at the current index `name_idx` of a name.
    :param: compressed - the package to be decompressed
    :param: name_idx - the index of a name in `compressed`
    :returns: a pair (decompressed, length) - the decompressed package and its length increase
    """
    segment_len = compressed[name_idx]
    compressed_len = 0
    decompressed = b''

    while segment_len != 0:
        # If first two bits are 1
        if (segment_len & 192) == 192:
            name_ptr = (segment_len & 63) << 8
            name_ptr += compressed[name_idx+1]
            decompressed = decompressed + decompress_name(compressed, name_ptr)[0]
            return decompressed, compressed_len + 2
        decompressed = decompressed + bytes([segment_len])
        decompressed = decompressed + compressed[name_idx + 1 : name_idx + 1 + segment_len]
        compressed_len = compressed_len + segment_len + 1
        name_idx = name_idx + segment_len + 1
        segment_len = compressed[name_idx]

    decompressed = decompressed + bytes([0])
    return decompressed, compressed_len + 1
```

Conversely, `decompress_msg()` decompresses a full DNS message applying the DNS name decompression algorithm to all names present in the message.

```python
def decompress_msg(compressed: bytes) -> bytes:
    """
    Decompress the DNS message `compressed`.
    :param: compressed - the compressed DNS message
    :returns: the decompressed DNS message.
    """
    count_header = compressed[4:12]
    qd_count = byte_to_int(count_header[:2])
    an_count = byte_to_int(count_header[2:4])
    ns_count = byte_to_int(count_header[4:6])
    ar_count = byte_to_int(count_header[6:8])
    decompressed = compressed[0:12]
    curr_idx = 12

    for i in range(qd_count):
        name, compressed_len = decompress_name(compressed, curr_idx)
        decompressed = decompressed + name
        curr_idx += compressed_len
        decompressed += compressed[curr_idx:curr_idx+4]
        curr_idx += 4

    for i in range(an_count + ns_count + ar_count):
        name, compressed_len = decompress_name(compressed, curr_idx)
        decompressed = decompressed + name
        curr_idx += compressed_len
        rr_type = compressed[curr_idx:curr_idx+2]
        decompressed += rr_type
        rr_type = byte_to_int(rr_type)
        curr_idx += 2
        decompressed += compressed[curr_idx:curr_idx+6]
        curr_idx += 6
        r_data_len = byte_to_int(compressed[curr_idx:curr_idx+2])
        curr_idx += 2
        if rr_type == 5: #If CNAME entry
            c_name, compressed_len = decompress_name(compressed, curr_idx)
            decompressed += pack('>H', len(c_name))
            decompressed += c_name
            curr_idx += compressed_len
        else:
            decompressed += compressed[curr_idx-2:curr_idx]
            decompressed += compressed[curr_idx:curr_idx+r_data_len]
            curr_idx += r_data_len

    return decompressed
```

That's all! Now enjoy testing DNS servers :-)