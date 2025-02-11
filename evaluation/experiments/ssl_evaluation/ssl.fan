# THIS GRAMMAR FILE WAS PRODUCED ENTIRELY BY Tim Scheckenbach
# IT IS BASED ON THE X.509 DER ENCODING STANDARD
# THE GRAMMAR IS NOT COMPLETE AND MIGHT CONTAIN ERRORS

# Basic Structure
<start> ::= <sequence_tag><sequence_length><cert_value> 
<cert_value> ::= <certificate><signature><bit_string_signature> 
<certificate_v1_value> ::= <v1_tag><serialNumber><signature><issuer><validity><subject><subjectPublicKeyInfo> 
<certificate_v1> ::= <sequence_tag><sequence_length><certificate_v1_value> 
<certificate_v2_value> ::= <v2_tag><serialNumber><signature><issuer><validity><subject><subjectPublicKeyInfo><issuerUniqueIdentifier><subjectUniqueIdentifier> 
<certificate_v2> ::= <sequence_tag><sequence_length><certificate_v2_value> 
<certificate_v3_value> ::= <v3_tag><serialNumber><signature><issuer><validity><subject><subjectPublicKeyInfo><issuerUniqueIdentifier><subjectUniqueIdentifier><extension> 
<certificate_v3> ::= <sequence_tag><sequence_length><certificate_v3_value> 
<certificate> ::= <certificate_v3> #| <certificate_v1> | <certificate_v2>

## Version Field
<v1_tag> ::= <version_tag><sequence_length><v1_value> 
<v1_value> ::= <integer_tag><integer_length>'\x00' 
<v2_tag> ::= <version_tag><sequence_length><v2_value> 
<v2_value> ::= <integer_tag><integer_length>'\x01' 
<v3_tag> ::= <version_tag><sequence_length><v3_value> 
<v3_value> ::= <integer_tag><integer_length>'\x02'
<version_tag> ::= <constructed><context>'\xa0' 

## Serial Number
<serialNumber> ::= <integer> 

## Signature
<signature> ::= <sha256_signature> # Add more here
### SHA256 
<sha256_signature_key> ::= <object_tag><object_length><sha256_signature_object_id>  
<sha256_signature_pair> ::= <sha256_signature_key><sha256_signature_value> 
<sha256_signature_value> ::= <null> 
<sha256_signature> ::= <sequence_tag><sequence_length><sha256_signature_pair> 
### ECDSA 
<ecdsa_signature_key> ::= <object_tag><object_length><ecdsa_signature_object_id> 
<ecdsa_signature_pair> ::= <ecdsa_signature_key><ecdsa_signature_value> 
<ecdsa_signature_value> ::= <null> 
<ecdsa_signature> ::= <sequence_tag><sequence_length><ecdsa_signature_pair> 

## Issuer 
<issuer_common_set> ::= <sequence_tag><sequence_length><common_pair> 
<issuer_common> ::= <set_tag><set_length><issuer_common_set> 
<issuer_value> ::= <issuer_common> 
<issuer> ::= <sequence_tag><sequence_length><issuer_value> 
<common_pair> ::= <common_key><common_value> 
<common_string_value> ::= 'Tim Scheckenbach CA' 
<common_string> ::= <utf8string_tag><utf8string_length><common_string_value> 
<common_value> ::= <common_string>

## Validity 
<validity_value> ::= <notBefore><notAfter> 
<validity> ::= <sequence_tag><sequence_length><validity_value> 
<notBefore> ::= <time_1> 
<notAfter> ::= <time_1> 
<time_1> ::= <utctime> | <generalized_time> 
<zone> ::= 'Z' 
### UTC 
<utctime_length> ::= <length> 
<utctime_tag> ::= '\x17'<primitive><universal> 
<utctime_value> ::= <utime> 
<utctime> ::= <utctime_tag><utctime_length><utctime_value> 
<utime> ::= <uyear><month_day><hour><minute><second><zone> 
<uyear> ::= <digit><digit> 
### Generalized Time 
<generalized_time_length> ::= <length> 
<generalized_time_tag> ::= '\x18'<primitive><universal> 
<generalized_time_value> ::= <gtime> 
<generalized_time> ::= <generalized_time_tag><generalized_time_length><generalized_time_value>
<gtime> ::= <gyear><month_day><hour><minute><second><zone> 
<gyear> ::= <digit><digit><digit><digit>

## Subject 
<subject> ::= <sequence_tag><sequence_length><identity> 
<identity> ::= <common_names><identity_field>* 
<identity_field> ::= <country_names> | <state_or_province_names> | <locality_names> | <street_addresses> | <organization_names> | <organizational_unit_names> | <surnames> | <titles> | <given_names> | <descriptions> 
### Common Name
<common_key> ::= <object_tag><object_length><common_name_object_id> 
<common_name_key> ::= <object_tag><object_length><common_name_object_id> 
<common_name_pair> ::= <common_name_key><common_name_value> 
<common_name_set> ::= <sequence_tag><sequence_length><common_name_pair> 
<common_name_value> ::= <string> 
<common_names> ::= <set_tag><set_length><common_name_set>
### Country 
<country_name_key> ::= <object_tag><object_length><country_name_object_id> 
<country_name_pair> ::= <country_name_key><country_name_value> 
<country_name_set> ::= <sequence_tag><sequence_length><country_name_pair> 
<country_name_value> ::= <string> 
<country_names> ::= <set_tag><set_length><country_name_set> 
### State 
<state_or_province_name_key> ::= <object_tag><object_length><state_or_province_name_object_id>  
<state_or_province_name_pair> ::= <state_or_province_name_key><state_or_province_name_value> 
<state_or_province_name_set> ::= <sequence_tag><sequence_length><state_or_province_name_pair> 
<state_or_province_name_value> ::= <string> 
<state_or_province_names> ::= <set_tag><set_length><state_or_province_name_set> 
### Locality 
<locality_name_key> ::= <object_tag><object_length><locality_name_object_id> 
<locality_name_pair> ::= <locality_name_key><locality_name_value> 
<locality_name_set> ::= <sequence_tag><sequence_length><locality_name_pair> 
<locality_name_value> ::= <string> 
<locality_names> ::= <set_tag><set_length><locality_name_set> 
### Street 
<street_address_key> ::= <object_tag><object_length><street_address_object_id> 
<street_address_pair> ::= <street_address_key><street_address_value> 
<street_address_set> ::= <sequence_tag><sequence_length><street_address_pair> 
<street_address_value> ::= <string> 
<street_addresses> ::= <set_tag><set_length><street_address_set> 
### Organization 
<organization_name_key> ::= <object_tag><object_length><organization_name_object_id> 
<organization_name_pair> ::= <organization_name_key><organization_name_value> 
<organization_name_set> ::= <sequence_tag><sequence_length><organization_name_pair> 
<organization_name_value> ::= <string> 
<organization_names> ::= <set_tag><set_length><organization_name_set> 
### Organizational Unit 
<organizational_unit_name_key> ::= <object_tag><object_length><organizational_unit_name_object_id> 
<organizational_unit_name_pair> ::= <organizational_unit_name_key><organizational_unit_name_value> 
<organizational_unit_name_set> ::= <sequence_tag><sequence_length><organizational_unit_name_pair> 
<organizational_unit_name_value> ::= <string> 
<organizational_unit_names> ::= <set_tag><set_length><organizational_unit_name_set> 
### Surname
<surname_key> ::= <object_tag><object_length><surname_object_id> 
<surname_pair> ::= <surname_key><surname_value> 
<surname_set> ::= <sequence_tag><sequence_length><surname_pair> 
<surname_value> ::= <string> 
<surnames> ::= <set_tag><set_length><surname_set> 
### Title
<title_key> ::= <object_tag><object_length><title_object_id> 
<title_pair> ::= <title_key><title_value> 
<title_set> ::= <sequence_tag><sequence_length><title_pair> 
<title_value> ::= <string> 
<titles> ::= <set_tag><set_length><title_set> 
### Given Name 
<given_name_key> ::= <object_tag><object_length><given_name_object_id> 
<given_name_pair> ::= <given_name_key><given_name_value> 
<given_name_set> ::= <sequence_tag><sequence_length><given_name_pair> 
<given_name_value> ::= <string> 
<given_names> ::= <set_tag><set_length><given_name_set> 
### Description 
<description_key> ::= <object_tag><object_length><description_object_id> 
<description_pair> ::= <description_key><description_value> 
<description_set> ::= <sequence_tag><sequence_length><description_pair> 
<description_value> ::= <string> 
<descriptions> ::= <set_tag><set_length><description_set>  

## Subject Public Key Info 
<subjectPublicKeyInfo> ::= <sequence_tag><sequence_length><subjectPublicKeyInfo_value> 
<subjectPublicKeyInfo_value> ::= <publicKey_algorithm><bit_string_pubkey> 
<bit_string_pubkey> ::= <bit_string_tag><bit_string_length><bit_string_value_pubkey> 
<bit_string_value_pubkey> ::= <any_value>
<publicKey_algorithm> ::= <rsa_signature> # Maybe add more 
### RSA 
<rsa_signature_key> ::= <object_tag><object_length><rsa_signature_object_id> 
<rsa_signature_pair> ::= <rsa_signature_key><rsa_signature_value> 
<rsa_signature_value> ::= <null> 
<rsa_signature> ::= <sequence_tag><sequence_length><rsa_signature_pair> 

## Issuer Unique Identifier (Deprecated)
<issuerUniqueIdentifier> ::= '' 

## Subject Unique Identifier (Deprecated)
<subjectUniqueIdentifier> ::= "" 

## Extensions 
<extension> ::= <extension_tag><sequence_length><extension_value>
<extension_tag> ::='\xa3'<constructed><context>
<extension_value> ::= <sequence_tag><sequence_length><extension_value_fields>
<extension_value_fields> ::= <fields>
<fields> ::= <basic_constraint>?<key_usage>?<ext_key_usage>?<subject_alt_name>?<issuer_alt_name>?
<critical> ::= <boolean>
### Basic Constraint 
<basic_constraint> ::= <sequence_tag><sequence_length><basic_constraint_value>
<basic_constraint_value> ::= <basic_constraint_pair><critical><octet_string_basic_constraint>
<octet_string_basic_constraint> ::= <octet_string_tag><octet_string_length><octet_string_basic_constraint_value>
<octet_string_basic_constraint_value> ::= <sequence_tag><sequence_length><octet_string_basic_constraint_value_sequence>
<octet_string_basic_constraint_value_sequence> ::= <boolean>?<integer>?
<basic_constraint_pair> ::= <object_tag><object_length><basic_constraint_iod>
### Key Usage 
<key_usage> ::= <sequence_tag><sequence_length><key_usage_value>
<key_usage_value> ::= <key_usage_pair><critical><octet_string_key_usage>
<key_usage_pair> ::= <object_tag><object_length><key_usage_oid>
<octet_string_key_usage> ::= <octet_string_tag><octet_string_length><octet_string_key_usage_value>
<octet_string_key_usage_value> ::= <bit_string_tag><bit_string_length><key_usage_bit_string_value>
<key_usage_bit_string_value> ::= "\x00"<byte>
### Extended Key Usage 
<ext_key_usage> ::= <sequence_tag><sequence_length><ext_key_usage_val>
<ext_key_usage_val> ::= <ext_key_usage_pair><critical><octet_string_ext_key_usage>
<ext_key_usage_pair> ::= <object_tag><object_length><ext_key_usage_oid>
<octet_string_ext_key_usage> ::= <octet_string_tag><octet_string_length><octet_string_ext_key_usage_val>
<octet_string_ext_key_usage_val> ::= <sequence_tag><sequence_length><ext_key_usage_oid_pairs>
<ext_key_usage_oid_pairs> ::= <ext_key_usage_oid_pair>+
<ext_key_usage_oid_pair> ::= <object_tag><object_length><ext_key_usage_oid_usable>
### Subject Alternative Name 
<subject_alt_name> ::= <sequence_tag><sequence_length><subject_alt_name_val>
<subject_alt_name_val> ::= <subject_alt_name_pair><octet_string_subject_alt_name> #must not be critical
<subject_alt_name_pair> ::= <object_tag><object_length><subject_alt_name_oid>
<octet_string_subject_alt_name> ::= <octet_string_tag><octet_string_length><octet_string_subject_alt_name_val>
<octet_string_subject_alt_name_val> ::= <sequence_tag><sequence_length><subject_alt_name_mult>
<subject_alt_name_mult> ::= <octet_string_subject_alt_name_val_seq>+
<octet_string_subject_alt_name_val_seq> ::= <rfc_tag><sequence_length><subject_alt_name_val_bytes> | <dns_tag><sequence_length><subject_alt_name_val_bytes> | <uri_tag><sequence_length><subject_alt_name_val_bytes> | <ip_tag><sequence_length><subject_alt_name_val_bytes>{16}
<rfc_tag> ::= "\x81"
<dns_tag> ::= "\x82"
<uri_tag> ::= "\x86"
<ip_tag> ::= "\x87"
<subject_alt_name_val_bytes> ::= <byte>+
### Issuer Alternative Name
<issuer_alt_name> ::= <sequence_tag><sequence_length><issuer_alt_name_val>
<issuer_alt_name_val> ::= <issuer_alt_name_pair><octet_string_subject_alt_name> # must not be critical 
<issuer_alt_name_pair> ::= <object_tag><object_length><issuer_alt_name_oid>

# DER Encoding
## Length
<length> ::= <short_length> | <long_length>
<long_length> ::= <byte128_255><byte>+ 
<short_length> ::= <byte0_127> 

## Tag 
<private> ::= '' 
<primitive> ::= '' 
<constructed> ::= '' 
<context> ::= '' 
<universal> ::= '' 
<application> ::= '' 

## Datastructures 
### Sequence 
<sequence_length> ::= <length> 
<sequence_tag> ::= '0'<constructed><universal> 
<sequence_value> ::= <value>* 
<sequence> ::= <sequence_tag><sequence_length><sequence_value> 
### Set 
<set_length> ::= <length> 
<set_tag> ::= '1'<constructed><universal> 
<set_value> ::= <value>* 
<set> ::= <set_tag><set_length><set_value> 
### Object 
<object_length> ::= <length> 
<object_tag> ::= '\x06'<primitive><universal> 
<object_value> ::= <any_value> 
<object> ::= <object_tag><object_length><object_value> 
### Enumerated (Not used)
<enumerated_length> ::= <length> 
<enumerated_tag> ::= '\n'<primitive><universal> | 'J'<primitive><application> | '\x8a'<primitive><context> | 'Ê'<primitive><private> 
<enumerated_value> ::= <any_value> 
<enumerated> ::= <enumerated_tag><enumerated_length><enumerated_value> 
### Other (Not used)
<other_high_tag> ::= <high_tag><byte>+ 
<other_length> ::= <length> 
<other_low_tag> ::= '\x1b' | '\t' | '\x00' | '\x07' | '\x1d' | '\x12' | '\x0e' | '\x19' | '\r' | '\x1a' | '\x08' | '\x0b' | '\x0f' | '\x15' 
<high_tag> ::= '?'<constructed><universal> | '\x7f'<constructed><application> | '¿'<constructed><context> | 'ÿ'<constructed><private> | '\x1f'<primitive><universal> | '_'<primitive><application> | '\x9f'<primitive><context> | 'ß'<primitive><private> 
<other_tag> ::= <other_low_tag> | <other_high_tag> 
<other_value> ::= <byte>* 
<other> ::= <other_tag><other_length><other_value> 

## Data Types
### Strings 
<string> ::= <utf8string> | <printablestring> #| <bmpstring> | <teletexstring> | <universalstring> #Anything but utf8 and printable is deprecated
#### UTF8 
<utf8string_length> ::= <length> 
<utf8string_tag> ::= '\x0c'<primitive><universal> 
<utf8string_value> ::= <byte0_127>+ 
<utf8string> ::= <utf8string_tag><utf8string_length><utf8string_value> 
#### Printable 
<printablestring_length> ::= <length> 
<printablestring_tag> ::= '\x13'<primitive><universal> 
<printablestring_value> ::= <any_value> 
<printablestring> ::= <printablestring_tag><printablestring_length><printablestring_value> 
#### BMP 
<bmpstring_length> ::= <length> 
<bmpstring_tag> ::= '\x1e'<primitive><universal> 
<bmpstring_value> ::= <any_value> 
<bmpstring> ::= <bmpstring_tag><bmpstring_length><bmpstring_value>
#### Teletex 
<teletexstring_length> ::= <length> 
<teletexstring_tag> ::= '\x14'<primitive><universal> 
<teletexstring_value> ::= <any_value> 
<teletexstring> ::= <teletexstring_tag><teletexstring_length><teletexstring_value> 
#### Universal 
<universalstring_length> ::= <length> 
<universalstring_tag> ::= '\x1c'<primitive><universal> 
<universalstring_value> ::= <any_value> 
<universalstring> ::= <universalstring_tag><universalstring_length><universalstring_value> 

### Boolean 
<boolean_length> ::= '\x01' 
<boolean_tag> ::= '\x01'<primitive><universal> 
<boolean_value> ::= '\x00' | 'ÿ' 
<boolean> ::= <boolean_tag><boolean_length><boolean_value>  

### Bit String 
<bit_string_length> ::= <length> 
<bit_string_tag> ::= '\x03'<primitive><universal> 
<bit_string_value> ::= <any_value>
<bit_string> ::= <bit_string_tag><bit_string_length><bit_string_value> 
<bit_string_signature> ::= <bit_string_tag><bit_string_length><bit_string_value_signature> 
<bit_string_value_signature> ::= <any_value>

### Integer
<integer_length> ::= '\x01' | '\x02' 
<integer_tag> ::= '\x02'<primitive><universal> 
<integer_value> ::= <byte><byte>+
<integer> ::= <integer_tag><integer_length><integer_value> 

### Null 
<null_length> ::= '\x00' 
<null_tag> ::= '\x05'<primitive><universal> 
<null_value> ::= '' 
<null> ::= <null_tag><null_length><null_value> 

### Octet String
<octet_string_length> ::= <length> 
<octet_string_tag> ::= '\x04'<primitive><universal> #| 'D'<primitive><application> | '\x84'<primitive><context> | 'Ä'<primitive><private> 
<octet_string_value> ::= <any_value> 
<octet_string> ::= <octet_string_tag><octet_string_length><octet_string_value> 


# OIDs
<common_name_object_id> ::= 'U\x04\x03' 
<country_name_object_id> ::= 'U\x04\x06' 
<description_object_id> ::= 'U\x04\r' 
<ecdsa_signature_object_id> ::= '*\x86HÎ=\x04\x03\x02' 
<basic_constraint_iod> ::= "U\x1d\x13"
<key_usage_oid> ::= "U\x1d\x0f"
<ext_key_usage_oid> ::= "\x55\x1d\x25"
<ext_key_usage_oid_usable> ::= "\x2b\x06\x01\x05\x05\x07\x03"<oid_byte>
<oid_byte> ::= "\x01" | "\x02" | "\x03" | "\x04" | "\x08" | "\x09"
<subject_alt_name_oid> ::= "\x55\x1d\x11"
<issuer_alt_name_oid> ::= "\x55\x1d\x12"
<given_name_object_id> ::= 'U\x04*' 
<locality_name_object_id> ::= 'U\x04\x07' 
<organization_name_object_id> ::= 'U\x04\n' 
<organizational_unit_name_object_id> ::= 'U\x04\x0b' 
<rsa_signature_object_id> ::= '*\x86H\x86÷\r\x01\x01\x01' 
<sha256_signature_object_id> ::= '*\x86H\x86÷\r\x01\x01\x0b'
<state_or_province_name_object_id> ::= 'U\x04\x08' 
<street_address_object_id> ::= 'U\x04\t' 
<surname_object_id> ::= 'U\x04\x04' 
<title_object_id> ::= 'U\x04\x0c' 

# Numbers, Bytes etc.
<month29> ::= '02' 
<month30> ::= '04' | '06' | '09' | '11' 
<month31> ::= '01' | '03' | '05' | '07' | '08' | '10' | '12' 
<minute> ::= <digit0_5><digit> 
<month_day> ::= <month31><day1_31> | <month30><day1_30> | <month29><day1_29>  
<day1_29> ::= '01' | '02' | '03' | '04' | '05' | '06' | '07' | '08' | '09' | '10' | '11' | '12' | '13' | '14' | '15' | '16' | '17' | '18' | '19' | '20' | '21' | '22' | '23' | '24' | '25' | '26' | '27' | '28' 
<day1_30> ::= '01' | '02' | '03' | '04' | '05' | '06' | '07' | '08' | '09' | '10' | '11' | '12' | '13' | '14' | '15' | '16' | '17' | '18' | '19' | '20' | '21' | '22' | '23' | '24' | '25' | '26' | '27' | '28' | '29' | '30' 
<day1_31> ::= '01' | '02' | '03' | '04' | '05' | '06' | '07' | '08' | '09' | '10' | '11' | '12' | '13' | '14' | '15' | '16' | '17' | '18' | '19' | '20' | '21' | '22' | '23' | '24' | '25' | '26' | '27' | '28' | '29' | '30' | '31' 
<hour> ::= <digit0_1><digit> | '20' | '21' | '22' | '23' 
<second> ::= <digit0_5><digit> 
<digit0_1> ::= '0' | '1' 
<digit0_5> ::= '0' | '1' | '2' | '3' | '4' | '5'
<byte0_127> ::= '\x00' | '\x01' | '\x02' | '\x03' | '\x04' | '\x05' | '\x06' | '\x07' | '\x08' | '\t' | '\n' | '\x0b' | '\x0c' | '\r' | '\x0e' | '\x0f' | '\x10' | '\x11' | '\x12' | '\x13' | '\x14' | '\x15' | '\x16' | '\x17' | '\x18' | '\x19' | '\x1a' | '\x1b' | '\x1c' | '\x1d' | '\x1e' | '\x1f' | '' | '!' | '"' | '#' | '$' | '%' | '&' | "'" | '(' | ')' | '*' | '+' | '' | '' | '_' | '.' | '/' | '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | ':' | '' | '<' | '=' | '>' | '?' | '@' | 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'H' | 'I' | 'J' | 'K' | 'L' | 'M' | 'N' | 'O' | 'P' | 'Q' | 'R' | 'S' | 'T' | 'U' | 'V' | 'W' | 'X' | 'Y' | 'Z' | '' | '\\' | '' | '^' | '_' | '`' | 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | '{' | '|' | '}' | '~' | '\x7f' 
<byte128_255> ::= '' | '' | '' | '' | '' | '' | '' | '' | '' | '' | '' | '' | '' | '' | '' | '' | '' | '' | '' | '' | '' | '' | '' | '' | '' | '' | '' | '' | '' | '' | '' | '' | ' ' | '¡' | '¢' | '£' | '¤' | '¥' | '¦' | '§' | '¨' | '©' | 'ª' | '«' | '¬' | '­' | '®' | '¯' | '°' | '±' | '²' | '³' | '´' | 'µ' | '¶' | '·' | '¸' | '¹' | 'º' | '»' | '¼' | '½' | '¾' | '¿' | 'À' | 'Á' | 'Â' | 'Ã' | 'Ä' | 'Å' | 'Æ' | 'Ç' | 'È' | 'É' | 'Ê' | 'Ë' | 'Ì' | 'Í' | 'Î' | 'Ï' | 'Ð' | 'Ñ' | 'Ò' | 'Ó' | 'Ô' | 'Õ' | 'Ö' | '×' | 'Ø' | 'Ù' | 'Ú' | 'Û' | 'Ü' | 'Ý' | 'Þ' | 'ß' | 'à' | 'á' | 'â' | 'ã' | 'ä' | 'å' | 'æ' | 'ç' | 'è' | 'é' | 'ê' | 'ë' | 'ì' | 'í' | 'î' | 'ï' | 'ð' | 'ñ' | 'ò' | 'ó' | 'ô' | 'õ' | 'ö' | '÷' | 'ø' | 'ù' | 'ú' | 'û' | 'ü' | 'ý' | 'þ' | 'ÿ' 
<value> ::= <boolean> | <sequence> | <set> | <integer> | <null> | <bit_string> | <octet_string> | <object> | <enumerated> | <utf8string> | <printablestring> | <bmpstring> | <teletexstring> | <universalstring> | <utctime> | <generalized_time> | <other> 
<any_value> ::= <byte>* 


# CONSTRAINTS 
## Producing only positive serialnumbers
where bytes(str(<serialNumber>.<integer>.<integer_value>), "utf-8")[0] < 128

## <signature> should always extend to the same nonterminal

def get_child(tree):
    return tree._children[0].symbol.symbol

forall <sig1> in <signature>:
    forall <sig2> in <signature>:
        get_child(<sig1>) == get_child(<sig2>);

## Basic Constraint only positive Integers
def check_existence(tree):
    if len(tree._children) == 0:
        return False
    if len(tree._children) == 1 and tree._children[0].symbol.symbol == "<integer>":
        return False 
    else:
        return True

where (not check_existence(<octet_string_basic_constraint_value_sequence>)) or (bytes(str(<octet_string_basic_constraint_value_sequence>.<integer>.<integer_value>), "utf-8")[0] < 128)

## We could write the grammar closer to the specification of the DER encoding, but doing this for every data type would lead to a huge overhead

#<sequence_tag> ::= <class><prim><type>
#<class> ::= <bit>{2}
#<prim> ::= <bit>
#<type> ::= <bit>{5}

#where ord(str(<sequence_tag>.<type>)) == 16
#where ord(str(<sequence_tag>.<prim>)) == 1
#where ord(str(<sequence_tag>.<class>)) == 0