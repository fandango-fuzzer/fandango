<start> ::= <ping>
<ping> ::= <ping_req> <ping_resp>
<ping_req> ::= 'ping'
<ping_resp> ::= 'pong'

# ==============================
# === fandango is responding ===

def send_response():
    pass
    # write(server_fp, '<ping> . <ping_resp>'

def get_request():
    pass
    # server_fp = open('https://lorem-ipsum.example')
    # set_tree({
    #      '<ping_req>': read(server_fp)
    #  })

on_lifecycle(FandangoLifecycle.PRE_EVOLVE, get_request)
on_lifecycle(FandangoLifecycle.FINALLY, send_response)

# ===========================================
# === alternative, fandango is requesting ===

# def send_request():
#     request = get_str('<ping> . <ping_req>')
#     server_fp = write('https://lorem-ipsum.example', request)
#     response = read(server_fp)
#     set_tree({
#         '<ping_res>': response
#     })
#
# on_lifecycle(FandangoLifecycle.POST_EVOLVE, send_request)


# Note to myself. Solve locals/globals problem by using a dict that passes fuzzing results to .fan environment and accepts string to populate tree with