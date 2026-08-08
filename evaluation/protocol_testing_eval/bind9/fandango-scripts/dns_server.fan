include('dns.fan')

# If used as a client interact with a command like this:
# dig @127.0.0.1 -p 25565 A fandango.io +noedns +time=100 +tries=1

# Fandango plays the server
fandango_is_client = False

