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
To test it with Fandango as client querying the DNS server 1.1.1.1 on port 53, invoke Fandango as

```shell
$ fandango -v talk -n 1 -f dns.fan --client udp:1.1.1.1:53
```

```{versionadded} 1.1
These features are available in Fandango 1.1 and later.
```

## A DNS Exchange

In principle, the DNS _protocol_ is pretty simple.
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

All straight-forward so far.
Let's dig a bit deeper.


## DNS Requests

A DNS request consists of a header and a number of questions and answers as specified in the header.

```python
<dns_req> ::= <header_req> <question>{byte_to_int(<req_qd_count>)}
```

The actual number of questions is set in the `<req_qd_count>` field of the `<header_req>`. We decode it as

```python
# Convert a 2-byte byte array to an integer
def byte_to_int(byte_val):
    return int(unpack('>H', bytes(byte_val))[0])
```

### Request Headers

The header consists of a number of fields as defined below:

```python
<header_req> ::= <h_id> 0 <h_opcode_standard> 0 0 <h_rd> 0 0 <bit> 0 <h_rcode_none> <req_qd_count> 0{16} 0{16} 0{16}
```

The ID is an identifier of two bytes.
When sending the request, we choose random values:

```python
<h_id> ::= <byte><byte>
```

The remaining fields are set to fixed values:

```python
<h_opcode_standard> ::= 0 0 0 0
<h_rd> ::= 1 # 0 causes server failure with cname
<h_rcode_none> ::= 0 0 0 0
<req_qd_count> ::= <byte>{2} := pack(">H", 1)
```


### Request Questions

Now for the actual DNS questions.
This is where a host name (say, `example.com`) to be looked up is transmitted.

```python
<question> ::= <q_name> <q_type> <rr_class>
```

#### Request Names

A request name is terminated by 8 zero-bits.

```python
<q_name> ::= <q_name_written> 0{8}
```

The name is encoded as an octet telling the length, and then a sequence of bytes representing the actual name.

```python
<q_name_written> ::= (<label_len_octet> <byte>{byte_to_int(b'\x00' + bytes(<label_len_octet>))})+ := gen_q_name()
<label_len_octet> ::= <byte>
```

To generate domain names to query, we either generate a domain name using the Faker library, which likely is not known to the DNS server,
or we use 'github.com' or 'cispa.de', which are known to the DNS server.

The individual parts (say, `github` and `com`) are also length-encoded, i.e. there is a leading byte telling the length of the part, followed by the part.

```python
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

#### Request Types

We can request CNAME, A, and NS records from the DNS server.
These are encoded using bit sequences as follows:

```python
<q_type> ::= <type_id_cname> | <type_id_a> | <type_id_ns>
<type_id_cname> ::= 0{13} 1 0 1
<type_id_a> ::= 0{15} 1
<type_id_ns> ::= 0{14} 1 0
```

#### Request Class

Our DNS request refers to class `IN` (Internet).

```python
<rr_class> ::= 0{15} 1 # Equals class IN (Internet)
```

With that, the definition of our requests are complete.


## DNS Responses

Now for the responses of the DNS server.

```python
<dns_resp> ::= <header_resp> <question_section> <answer_an_section> <answer_au_section> <answer_opt_section>
```

### DNS Response Headers

First, let us have a look at the header.

```python
<header_resp> ::= <h_id> 1 <h_opcode_standard> <bit> 0 <h_rd> <h_ra> 0 <h_aa> 0 (<h_rcode_none> | <h_rcode_name>) <resp_qd_count> <resp_an_count> <resp_ns_count> <resp_ar_count>
```

Most of these fields have been defined above already.
These are new:

```python
<h_aa> ::= <bit>
<h_ra> ::= <bit>
```

The interesting part is the return code, telling success (or non-success) of the query:

% FIXME: What is the meaning of the return codes? NXDOMAIN? NXERROR?

```python
<h_rcode> ::= <h_rcode_none> | <h_rcode_format> | <h_rcode_server> | <h_rcode_name> | <h_rcode_ni> | <h_rcode_refused> | <h_rcode_other>
<h_rcode_none> ::= 0 0 0 0
<h_rcode_format> ::= 0 0 0 1
<h_rcode_server> ::= 0 0 1 0
<h_rcode_name> ::= 0 0 1 1
<h_rcode_ni> ::= 0 1 0 0
<h_rcode_refused> ::= 0 1 0 1
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
This is necessary as the UDP protocol can drop packets, so the response must be clear which request it refers to.
This has the same format as the original response.

```python
<question_section> ::= <question>{byte_to_int(<header_req>.<req_qd_count>)}
```

% FIXME: The length is defined by the request, not the response? -- AZ

We ensure that for each request/response pair,

* The recursion desired flag (RD) (`<h_rd>`) match.
* The DNS message identifier (ID) (`<h_id>`) match.
* The question that the response aims to answer is the same as the question in the request (`<question>`).
* The question count in the response matches the question count in the request (`<req_qd_count>`).

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

AN answers are structured like this:  % FIXME: What is an AN answer?

```python
<answer_an> ::= <q_name_optional> <answer_an_type>
<q_name_optional> ::= <q_name_written>? 0{8}
<answer_an_type> ::= (<type_a> |<type_cname> | <type_ns>)
```

##### Type A Answers

```python
<type_a> ::= <type_id_a> <rr_class> <a_ttl> 0{13} 1 0 0 <byte>{4}
<type_id_a> ::= 0{15} 1
<a_ttl> ::= 0 <bit>{7} <byte>{3}
```

##### Type CNAME Answers

```python
<type_cname> ::= <type_id_cname> <rr_class> <a_ttl> <a_rd_length> <q_name>
```

`<type_cname>` responses must have the correct length in the `<a_rd_length>` field (r data length), which corresponds to the following `<q_name>` field.

```python
where forall <t> in <type_cname>:
    bytes(<t>.<a_rd_length>) == pack('>H', len(bytes(<t>.<q_name>)))
```

##### Type NS Answers

```python
<type_ns> ::= <type_id_ns> <rr_class> <a_ttl> <a_rd_length> <a_rdata>{int(unpack('>H', bytes(<a_rd_length>))[0])}
<a_rdata> ::= <byte>
```

#### AU Answers

AU answers are structured like this:  % FIXME: What is an AU answer?

```python
<answer_au> ::= <q_name_optional> <type_soa>
<type_soa> ::= <type_id_soa> <rr_class> <a_ttl> <a_rd_length> <a_rdata>{int(unpack('>H', bytes(<a_rd_length>))[0])}
<a_rd_length> ::= <byte>{2} := pack(">H", randint(0, 0))
<a_rdata> ::= <byte>
<type_id_soa> ::= 0{13} 1 1 0
```

#### OPT Answers

OPT answers are structured like this:  % FIXME: What is an OPT answer?

```python
<answer_opt> ::= <q_name_optional> (<type_opt>|<type_a>)
<type_opt> ::= <type_id_opt> <udp_payload_size> <a_ttl> <a_rd_length> <a_rdata>{int(unpack('>H', bytes(<a_rd_length>))[0])}
<type_id_opt> ::= 0{10} 1 0 1 0 0 1
<udp_payload_size> ::= <bit>{16}
```


#### Consistency in Responses

We check if a DNS response answers the corresponding DNS question using the `verify_transitive()` function.
The remainder of the check does the same check, but only for direct answers without allowing transitive response chains.
This second part is used to allow Fandango ``contains solving'' optimization to be used to generate a valid answer more efficiently.

% FIXME: Convert to new all()/any() quantifier syntax
```python
where forall <ex> in <start>.<exchange>:
    forall <a> in <ex>.<dns_resp>.<answer_an_section>.<answer_an>:
        exists <q> in <ex>.<dns_req>.<question>:
            verify_transitive(<q>, <ex>.<dns_resp>) or bytes(<a>.<answer_an_type>)[0:2] == bytes(<q>.<q_type>) and bytes(<a>.<q_name_optional>) == bytes(<q>.<q_name>)
```

The `verify_transitive()` function gets a question and the response section of a DNS response and verifies if the response does answer the question.
This also handles responses that are transitive.
If, for example the question is for a type A record for "example.com" and the response contains a CNAME record pointing "example.com" to "alias.com" and then an A record for "alias.com", this function will verify that the response correctly answers the original question through the CNAME redirection.

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
We implement this by overriding the `NetworkParty` `send()` and `receive()` functions such that all sent messages are compressed, and all received messages are decompressed.

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

`msg_suffix()` generates a list of tuples, for a DNS name containing an entry for each zone present in it including the offset to that zone within the DNS name.
Example: `msg_suffix(b'\x08fandango\x02io\x00')` results in `[(0, b'\x08fandango\x02io\x00'), (9, b'\x02io\x00')]`.

```python
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

We apply the DNS name compression algorithm to a DNS name starting at `curr_idx` within the uncompressed message.
`suffix_dict` is a dictionary mapping a known DNS suffix names to their offsets within the already analyzed compressed part of the message.

% FIXME: Add types
% FIXME: Add full docstrings, with :param: and :return:

```python
def compress_name(uncompressed, curr_idx, len_reduction, suffix_dict):
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
def compress_msg(uncompressed):
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

`decompress_name()` decompresses a DNS name starting at name_idx within the compressed message.

```python
def decompress_name(compressed, name_idx):
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
def decompress_msg(compressed):
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