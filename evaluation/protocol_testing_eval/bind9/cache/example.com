$TTL    604800
@       IN      SOA     ns1.example.com. admin.example.com. (
                              2         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL
;
@       IN      NS      ns1.example.com.
@       IN      MX      10 mail.example.com.
@       IN      A       127.0.0.1
@       IN      AAAA    ::1
@       IN      TXT     "v=spf1 -all"
ns1     IN      A       127.0.0.1
mail    IN      A       127.0.0.1
mail    IN      AAAA    ::1
www     IN      A       127.0.0.1
ipv6    IN      AAAA    ::1
txt     IN      TXT     "hello world"
test    IN      CNAME   example.com.
; SRV record for a SIP service over TCP.
_sip._tcp       IN      SRV     10 60 5060 mail.example.com.
