$TTL    604800
@       IN      SOA     ns1.cispa.de. admin.cispa.de. (
                              2         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL
;
@       IN      NS      ns1.cispa.de.
ns1     IN      A       127.0.0.1
@       IN      A       127.0.0.1
test    IN      CNAME   cispa.de.