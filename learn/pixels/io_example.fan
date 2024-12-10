<start> ::= <ping>;
<ping> ::= <ping_req> <ping_resp>;
<ping_req> ::= <req_header> <req_body>;
<req_header> ::= 'header1' | 'header2' | 'header3';
<req_body> ::= 'body1' | 'body2' | 'body3';
<ping_resp> ::= 'pong';

# ==============================
# === fandango is responding ===

def first():
    print("test 2")
    set_partial_solution('<ping_req>', 'header2body3')
    # write(server_fp, '<ping> . <ping_resp>'

def second():
    print("test 1")
    # server_fp = open('https://lorem-ipsum.example')
    # set_tree({
    #      '<ping_req>': read(server_fp)
    #  })

on_lifecycle(FandangoLifecycle.PRE_EVOLVE, first)
on_lifecycle(FandangoLifecycle.POST_EVOLVE, second)
print(get_solutions())

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