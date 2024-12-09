<start> ::= <ping>
<ping> ::= <ping_req> <ping_resp>
<ping_req> ::= 'ping'
<ping_resp> ::= 'pong'

# ==============================
# === fandango is responding ===

def send_response():
    write(server_fp, '<ping> . <ping_resp>'

def get_request():
    server_fp = open('https://lorem-ipsum.example')
    set_tree({
        '<ping_req>': read(server_fp)
    })

on_lifecycle(PRE_EVOLVE, get_request)
on_lifecycle(FINALLY, send_response)

# ===========================================
# === alternative, fandango is requesting ===

def send_request():
    request = get_str('<ping> . <ping_req>')
    server_fp = write('https://lorem-ipsum.example', request)
    response = read(server_fp)
    set_tree({
        '<ping_res>': response
    })

on_lifecycle(POST_EVOLVE, send_request)