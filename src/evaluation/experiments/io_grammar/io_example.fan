<start> ::= <ping>;
<ping> ::= <server:ping_req> <ping_resp>;
<ping_req> ::= <req_header> <req_body>;
<req_header> ::= 'header1' | 'header2' | 'header3';
<req_body> ::= 'body1' | 'body2' | 'body3';
<ping_resp> ::= 'pong';

# ==============================
# === fandango is responding ===

def get_request():
    set_partial_solution('<ping_req>', 'header2body3')
    # pass
    # server_fp = open('https://lorem-ipsum.example')
    # set_partial_solution('<ping_req>', read(server_fp))

def send_answer():
    pass
    # write(server_fp, '<ping> . <ping_resp>'

on_lifecycle(FandangoLifecycle.PRE_EVOLVE, get_request)
on_lifecycle(FandangoLifecycle.POST_EVOLVE, send_answer)


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
