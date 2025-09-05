/Users/alexander/PycharmProjects/fandango/.venv/bin/python /Users/alexander/PycharmProjects/fandango/evaluation/experiments/ftp/ftp.py 
fandango:WARNING: Symbol <open_port_param> defined, but not used
fandango:WARNING: Symbol <client_name> defined, but not used
fandango:INFO: ---------- Initializing FANDANGO algorithm ---------- 
fandango:INFO: Generating (additional) initial population (size: 100)...
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Initial population generated in 0.00 seconds
fandango:INFO: Current coverage: 0.00%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.01%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.02%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.03%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.04%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.05%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.06%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.07%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.08%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.10%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.11%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50012|)\r\n'
fandango:INFO: Current coverage: 0.12%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.13%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.15%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.28%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.29%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.29%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.29%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.30%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.30%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.30%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.30%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.30%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.30%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 5.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.30%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.30%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.31%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50027|)\r\n'
fandango:INFO: Current coverage: 0.31%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.31%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.33%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.33%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.33%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.33%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.33%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.33%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.33%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.33%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.34%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50026|)\r\n'
fandango:INFO: Current coverage: 0.34%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.35%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.35%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.36%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.36%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.37%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.37%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.37%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.37%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.38%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50091|)\r\n'
fandango:INFO: Current coverage: 0.38%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.38%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.38%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.39%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.39%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.39%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.39%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.39%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.39%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.39%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.39%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50018|)\r\n'
fandango:INFO: Current coverage: 0.39%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.39%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.39%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.39%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.39%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 4.
fandango:INFO: ClientControl -> ServerControl: <request_feat> 'FEAT\r\n'
fandango:INFO: Current coverage: 0.40%
fandango:INFO: ServerControl -> ClientControl: <response_feat> '211-Features:\r\n EPRT\r\n EPSV\r\n MDTM\r\n PASV\r\n REST STREAM\r\n SIZE\r\n TVFS\r\n UTF8\r\n211 End\r\n'
fandango:INFO: Current coverage: 0.41%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.42%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.42%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.42%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.42%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.42%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_auth_tls> 'AUTH TLS\r\n'
fandango:INFO: Current coverage: 0.43%
fandango:INFO: ServerControl -> ClientControl: <response_auth_tls> '530 Please login with USER and PASS.\r\n'
fandango:INFO: Current coverage: 0.45%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_auth_tls> 'AUTH TLS\r\n'
fandango:INFO: Current coverage: 0.45%
fandango:INFO: ServerControl -> ClientControl: <response_auth_tls> '530 Please login with USER and PASS.\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.47%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_fail> 'PASS x9_GEihi_Q8zpD0_9h\r\n'
fandango:INFO: Current coverage: 0.49%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_fail> '530 Login incorrect.\r\n'
fandango:INFO: Current coverage: 0.50%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.50%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.50%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.50%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.51%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.51%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.51%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.52%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50000|)\r\n'
fandango:INFO: Current coverage: 0.52%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.52%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.52%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.52%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.52%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.52%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50012|)\r\n'
fandango:INFO: Current coverage: 0.53%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.53%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.53%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.53%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.53%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.53%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.53%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.53%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.53%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.53%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.53%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50037|)\r\n'
fandango:INFO: Current coverage: 0.53%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 4.
fandango:INFO: ClientControl -> ServerControl: <request_syst> 'SYST\r\n'
fandango:INFO: Current coverage: 0.54%
fandango:INFO: ServerControl -> ClientControl: <response_syst> '215 UNIX Type: L8\r\n'
fandango:INFO: Current coverage: 0.55%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.55%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.56%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.56%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.56%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.57%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.57%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.57%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.57%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.57%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.57%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.57%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.57%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.58%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.58%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50078|)\r\n'
fandango:INFO: Current coverage: 0.58%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.59%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.59%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 5.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.59%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.59%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.59%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.59%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.59%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.59%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.59%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.59%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.59%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.59%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.59%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.59%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.59%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.60%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.60%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_feat> 'FEAT\r\n'
fandango:INFO: Current coverage: 0.61%
fandango:INFO: ServerControl -> ClientControl: <response_feat> '211-Features:\r\n EPRT\r\n EPSV\r\n MDTM\r\n PASV\r\n REST STREAM\r\n SIZE\r\n TVFS\r\n UTF8\r\n211 End\r\n'
fandango:INFO: Current coverage: 0.61%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.61%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50023|)\r\n'
fandango:INFO: Current coverage: 0.61%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.61%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.61%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.61%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.61%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.61%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.61%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.61%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.61%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.61%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.61%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50035|)\r\n'
fandango:INFO: Current coverage: 0.61%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.61%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.61%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.61%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.62%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.62%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.62%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.62%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50078|)\r\n'
fandango:INFO: Current coverage: 0.62%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.62%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.62%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.62%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.62%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.62%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.62%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.62%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.62%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.62%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_feat> 'FEAT\r\n'
fandango:INFO: Current coverage: 0.63%
fandango:INFO: ServerControl -> ClientControl: <response_feat> '211-Features:\r\n EPRT\r\n EPSV\r\n MDTM\r\n PASV\r\n REST STREAM\r\n SIZE\r\n TVFS\r\n UTF8\r\n211 End\r\n'
fandango:INFO: Current coverage: 0.63%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.63%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.63%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.63%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50090|)\r\n'
fandango:INFO: Current coverage: 0.63%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.63%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.63%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.63%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.63%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.63%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50071|)\r\n'
fandango:INFO: Current coverage: 0.63%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_utf8> 'OPTS UTF8 ON\r\n'
fandango:INFO: Current coverage: 0.64%
fandango:INFO: ServerControl -> ClientControl: <response_set_utf8> '200 Always in UTF8 mode.\r\n'
fandango:INFO: Current coverage: 0.65%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.66%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.66%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.66%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.66%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.66%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.66%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.66%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.66%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.66%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.66%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50038|)\r\n'
fandango:INFO: Current coverage: 0.66%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.66%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.66%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.66%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.66%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.67%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.67%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.67%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.67%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.67%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.67%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.67%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.67%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.67%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.67%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.67%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.67%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.67%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.67%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50040|)\r\n'
fandango:INFO: Current coverage: 0.67%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_syst> 'SYST\r\n'
fandango:INFO: Current coverage: 0.67%
fandango:INFO: ServerControl -> ClientControl: <response_syst> '215 UNIX Type: L8\r\n'
fandango:INFO: Current coverage: 0.68%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.68%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.68%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.68%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.68%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.69%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.69%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.69%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50061|)\r\n'
fandango:INFO: Current coverage: 0.69%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.69%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.69%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.69%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.69%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.69%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.69%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.69%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50000|)\r\n'
fandango:INFO: Current coverage: 0.69%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.70%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.70%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.70%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.70%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.70%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.70%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.70%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.70%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.70%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.70%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50084|)\r\n'
fandango:INFO: Current coverage: 0.70%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.70%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.70%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_syst> 'SYST\r\n'
fandango:INFO: Current coverage: 0.70%
fandango:INFO: ServerControl -> ClientControl: <response_syst> '215 UNIX Type: L8\r\n'
fandango:INFO: Current coverage: 0.70%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.70%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.70%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.70%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.70%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.70%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.70%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.70%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.70%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_utf8> 'OPTS UTF8 ON\r\n'
fandango:INFO: Current coverage: 0.71%
fandango:INFO: ServerControl -> ClientControl: <response_set_utf8> '200 Always in UTF8 mode.\r\n'
fandango:INFO: Current coverage: 0.71%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.71%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50096|)\r\n'
fandango:INFO: Current coverage: 0.71%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.71%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.71%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.71%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.71%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.71%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_auth_tls> 'AUTH TLS\r\n'
fandango:INFO: Current coverage: 0.71%
fandango:INFO: ServerControl -> ClientControl: <response_auth_tls> '530 Please login with USER and PASS.\r\n'
fandango:INFO: Current coverage: 0.71%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_auth_ssl> 'AUTH SSL\r\n'
fandango:INFO: Current coverage: 0.72%
fandango:INFO: ServerControl -> ClientControl: <response_auth_ssl> '530 Please login with USER and PASS.\r\n'
fandango:INFO: Current coverage: 0.74%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.74%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.74%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.74%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.74%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.74%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50007|)\r\n'
fandango:INFO: Current coverage: 0.74%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.74%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.74%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.74%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.74%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.74%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.74%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 4.
fandango:INFO: ClientControl -> ServerControl: <request_syst> 'SYST\r\n'
fandango:INFO: Current coverage: 0.75%
fandango:INFO: ServerControl -> ClientControl: <response_syst> '215 UNIX Type: L8\r\n'
fandango:INFO: Current coverage: 0.75%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.75%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.75%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.75%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.75%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.75%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.75%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.75%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.75%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.75%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.75%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.75%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 4.
fandango:INFO: ClientControl -> ServerControl: <request_set_utf8> 'OPTS UTF8 ON\r\n'
fandango:INFO: Current coverage: 0.75%
fandango:INFO: ServerControl -> ClientControl: <response_set_utf8> '200 Always in UTF8 mode.\r\n'
fandango:INFO: Current coverage: 0.75%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.76%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.76%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.76%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50044|)\r\n'
fandango:INFO: Current coverage: 0.76%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.76%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.76%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.76%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.76%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.76%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_auth_tls> 'AUTH TLS\r\n'
fandango:INFO: Current coverage: 0.76%
fandango:INFO: ServerControl -> ClientControl: <response_auth_tls> '530 Please login with USER and PASS.\r\n'
fandango:INFO: Current coverage: 0.76%
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.77%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.77%
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_fail> 'PASS jITz6fbgOY9m0QCcD\r\n'
fandango:INFO: Current coverage: 0.77%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_fail> '530 Login incorrect.\r\n'
fandango:INFO: Current coverage: 0.77%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.77%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.77%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.77%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.77%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.77%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.77%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.77%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50004|)\r\n'
fandango:INFO: Current coverage: 0.77%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_feat> 'FEAT\r\n'
fandango:INFO: Current coverage: 0.77%
fandango:INFO: ServerControl -> ClientControl: <response_feat> '211-Features:\r\n EPRT\r\n EPSV\r\n MDTM\r\n PASV\r\n REST STREAM\r\n SIZE\r\n TVFS\r\n UTF8\r\n211 End\r\n'
fandango:INFO: Current coverage: 0.77%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.77%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.77%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.77%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.77%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.77%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_auth_tls> 'AUTH TLS\r\n'
fandango:INFO: Current coverage: 0.77%
fandango:INFO: ServerControl -> ClientControl: <response_auth_tls> '530 Please login with USER and PASS.\r\n'
fandango:INFO: Current coverage: 0.77%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.77%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.77%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.77%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.77%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_utf8> 'OPTS UTF8 ON\r\n'
fandango:INFO: Current coverage: 0.78%
fandango:INFO: ServerControl -> ClientControl: <response_set_utf8> '200 Always in UTF8 mode.\r\n'
fandango:INFO: Current coverage: 0.78%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.78%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.78%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.78%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50033|)\r\n'
fandango:INFO: Current coverage: 0.78%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.78%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.78%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.78%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.78%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.78%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_auth_ssl> 'AUTH SSL\r\n'
fandango:INFO: Current coverage: 0.78%
fandango:INFO: ServerControl -> ClientControl: <response_auth_ssl> '530 Please login with USER and PASS.\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50003|)\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50002|)\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.79%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.79%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50056|)\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 4.
fandango:INFO: ClientControl -> ServerControl: <request_feat> 'FEAT\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:INFO: ServerControl -> ClientControl: <response_feat> '211-Features:\r\n EPRT\r\n EPSV\r\n MDTM\r\n PASV\r\n REST STREAM\r\n SIZE\r\n TVFS\r\n UTF8\r\n211 End\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.79%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.79%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50071|)\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 6.
fandango:INFO: ClientControl -> ServerControl: <request_syst> 'SYST\r\n'
fandango:INFO: Current coverage: 0.80%
fandango:INFO: ServerControl -> ClientControl: <response_syst> '215 UNIX Type: L8\r\n'
fandango:INFO: Current coverage: 0.80%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.80%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.80%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.80%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.80%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.80%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50064|)\r\n'
fandango:INFO: Current coverage: 0.80%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.80%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.80%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_feat> 'FEAT\r\n'
fandango:INFO: Current coverage: 0.80%
fandango:INFO: ServerControl -> ClientControl: <response_feat> '211-Features:\r\n EPRT\r\n EPSV\r\n MDTM\r\n PASV\r\n REST STREAM\r\n SIZE\r\n TVFS\r\n UTF8\r\n211 End\r\n'
fandango:INFO: Current coverage: 0.80%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.80%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.80%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.80%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.80%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.80%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.80%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.80%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.80%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.80%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.80%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50004|)\r\n'
fandango:INFO: Current coverage: 0.80%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.80%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.80%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.80%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.80%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.80%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.80%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.81%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.81%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.81%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.81%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.81%
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_fail> 'PASS C_cjUZu46byX7\r\n'
fandango:INFO: Current coverage: 0.81%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_fail> '530 Login incorrect.\r\n'
fandango:INFO: Current coverage: 0.82%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.82%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.82%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.82%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.82%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.82%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.82%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.82%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.82%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_feat> 'FEAT\r\n'
fandango:INFO: Current coverage: 0.82%
fandango:INFO: ServerControl -> ClientControl: <response_feat> '211-Features:\r\n EPRT\r\n EPSV\r\n MDTM\r\n PASV\r\n REST STREAM\r\n SIZE\r\n TVFS\r\n UTF8\r\n211 End\r\n'
fandango:INFO: Current coverage: 0.82%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.82%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50091|)\r\n'
fandango:INFO: Current coverage: 0.82%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.82%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.82%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.82%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.82%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.82%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.82%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.82%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.82%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.82%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.82%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50088|)\r\n'
fandango:INFO: Current coverage: 0.82%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.82%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.82%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.82%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.82%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.82%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.82%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.83%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.83%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 6.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.83%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.83%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.83%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.83%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.83%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.83%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.83%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.83%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.83%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.83%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.83%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.83%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.83%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_syst> 'SYST\r\n'
fandango:INFO: Current coverage: 0.83%
fandango:INFO: ServerControl -> ClientControl: <response_syst> '215 UNIX Type: L8\r\n'
fandango:INFO: Current coverage: 0.83%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.83%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50007|)\r\n'
fandango:INFO: Current coverage: 0.83%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.83%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.83%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.83%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.83%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.83%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.83%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.83%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.83%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.83%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.83%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50084|)\r\n'
fandango:INFO: Current coverage: 0.83%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.83%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.83%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.83%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.83%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_feat> 'FEAT\r\n'
fandango:INFO: Current coverage: 0.84%
fandango:INFO: ServerControl -> ClientControl: <response_feat> '211-Features:\r\n EPRT\r\n EPSV\r\n MDTM\r\n PASV\r\n REST STREAM\r\n SIZE\r\n TVFS\r\n UTF8\r\n211 End\r\n'
fandango:INFO: Current coverage: 0.84%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.84%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.84%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.84%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.84%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.84%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.84%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.84%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.84%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.84%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.84%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.84%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.84%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.84%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.84%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50026|)\r\n'
fandango:INFO: Current coverage: 0.84%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_utf8> 'OPTS UTF8 ON\r\n'
fandango:INFO: Current coverage: 0.84%
fandango:INFO: ServerControl -> ClientControl: <response_set_utf8> '200 Always in UTF8 mode.\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.85%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.85%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50083|)\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 4.
fandango:INFO: ClientControl -> ServerControl: <request_feat> 'FEAT\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:INFO: ServerControl -> ClientControl: <response_feat> '211-Features:\r\n EPRT\r\n EPSV\r\n MDTM\r\n PASV\r\n REST STREAM\r\n SIZE\r\n TVFS\r\n UTF8\r\n211 End\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50021|)\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.85%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.85%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_feat> 'FEAT\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:INFO: ServerControl -> ClientControl: <response_feat> '211-Features:\r\n EPRT\r\n EPSV\r\n MDTM\r\n PASV\r\n REST STREAM\r\n SIZE\r\n TVFS\r\n UTF8\r\n211 End\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50035|)\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.86%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.86%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_syst> 'SYST\r\n'
fandango:INFO: Current coverage: 0.86%
fandango:INFO: ServerControl -> ClientControl: <response_syst> '215 UNIX Type: L8\r\n'
fandango:INFO: Current coverage: 0.86%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.86%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50056|)\r\n'
fandango:INFO: Current coverage: 0.86%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.86%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.86%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.86%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.86%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.86%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.86%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.86%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.86%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.86%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.86%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50076|)\r\n'
fandango:INFO: Current coverage: 0.86%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.86%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.86%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.86%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.86%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.86%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.86%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.86%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.86%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.86%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50022|)\r\n'
fandango:INFO: Current coverage: 0.86%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.86%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.86%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.86%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.86%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50018|)\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 6.
fandango:INFO: ClientControl -> ServerControl: <request_set_utf8> 'OPTS UTF8 ON\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:INFO: ServerControl -> ClientControl: <response_set_utf8> '200 Always in UTF8 mode.\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.87%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.87%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50082|)\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_utf8> 'OPTS UTF8 ON\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:INFO: ServerControl -> ClientControl: <response_set_utf8> '200 Always in UTF8 mode.\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50055|)\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_utf8> 'OPTS UTF8 ON\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:INFO: ServerControl -> ClientControl: <response_set_utf8> '200 Always in UTF8 mode.\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50031|)\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 4.
fandango:INFO: ClientControl -> ServerControl: <request_syst> 'SYST\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerControl -> ClientControl: <response_syst> '215 UNIX Type: L8\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.88%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 4.
fandango:INFO: ClientControl -> ServerControl: <request_set_utf8> 'OPTS UTF8 ON\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerControl -> ClientControl: <response_set_utf8> '200 Always in UTF8 mode.\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50098|)\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50023|)\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.88%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50093|)\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_feat> 'FEAT\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerControl -> ClientControl: <response_feat> '211-Features:\r\n EPRT\r\n EPSV\r\n MDTM\r\n PASV\r\n REST STREAM\r\n SIZE\r\n TVFS\r\n UTF8\r\n211 End\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50089|)\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.88%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50075|)\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50002|)\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50015|)\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.88%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_utf8> 'OPTS UTF8 ON\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <response_set_utf8> '200 Always in UTF8 mode.\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50047|)\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50067|)\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50040|)\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50070|)\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.89%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_auth_tls> 'AUTH TLS\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <response_auth_tls> '530 Please login with USER and PASS.\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_auth_tls> 'AUTH TLS\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <response_auth_tls> '530 Please login with USER and PASS.\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_auth_ssl> 'AUTH SSL\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <response_auth_ssl> '530 Please login with USER and PASS.\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50022|)\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50092|)\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50010|)\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.89%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_auth_tls> 'AUTH TLS\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <response_auth_tls> '530 Please login with USER and PASS.\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_auth_tls> 'AUTH TLS\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <response_auth_tls> '530 Please login with USER and PASS.\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_auth_tls> 'AUTH TLS\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <response_auth_tls> '530 Please login with USER and PASS.\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_auth_tls> 'AUTH TLS\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <response_auth_tls> '530 Please login with USER and PASS.\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ClientControl -> ServerControl: <request_auth_tls> 'AUTH TLS\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <response_auth_tls> '530 Please login with USER and PASS.\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50011|)\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50081|)\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50009|)\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.90%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_syst> 'SYST\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: ServerControl -> ClientControl: <response_syst> '215 UNIX Type: L8\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50013|)\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50100|)\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.90%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: ClientControl -> ServerControl: <request_login_user_fail> 'USER bF_MF9ZqpvLCuKTtJs6\r\n'
fandango:INFO: Current coverage: 0.91%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.91%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_fail> '530 Login incorrect.\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50022|)\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 4.
fandango:INFO: ClientControl -> ServerControl: <request_feat> 'FEAT\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:INFO: ServerControl -> ClientControl: <response_feat> '211-Features:\r\n EPRT\r\n EPSV\r\n MDTM\r\n PASV\r\n REST STREAM\r\n SIZE\r\n TVFS\r\n UTF8\r\n211 End\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.92%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.92%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50059|)\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_utf8> 'OPTS UTF8 ON\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: ServerControl -> ClientControl: <response_set_utf8> '200 Always in UTF8 mode.\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50046|)\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.93%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.93%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50061|)\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_feat> 'FEAT\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: ServerControl -> ClientControl: <response_feat> '211-Features:\r\n EPRT\r\n EPSV\r\n MDTM\r\n PASV\r\n REST STREAM\r\n SIZE\r\n TVFS\r\n UTF8\r\n211 End\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50014|)\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.93%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.93%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50065|)\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_utf8> 'OPTS UTF8 ON\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_set_utf8> '200 Always in UTF8 mode.\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50046|)\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50086|)\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50002|)\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 5.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50015|)\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_feat> 'FEAT\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_feat> '211-Features:\r\n EPRT\r\n EPSV\r\n MDTM\r\n PASV\r\n REST STREAM\r\n SIZE\r\n TVFS\r\n UTF8\r\n211 End\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50028|)\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50037|)\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50057|)\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 5.
fandango:INFO: ClientControl -> ServerControl: <request_set_utf8> 'OPTS UTF8 ON\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_set_utf8> '200 Always in UTF8 mode.\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50096|)\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50017|)\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_feat> 'FEAT\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_feat> '211-Features:\r\n EPRT\r\n EPSV\r\n MDTM\r\n PASV\r\n REST STREAM\r\n SIZE\r\n TVFS\r\n UTF8\r\n211 End\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_feat> 'FEAT\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_feat> '211-Features:\r\n EPRT\r\n EPSV\r\n MDTM\r\n PASV\r\n REST STREAM\r\n SIZE\r\n TVFS\r\n UTF8\r\n211 End\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50003|)\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.95%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50014|)\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 5.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50088|)\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.95%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_auth_tls> 'AUTH TLS\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_auth_tls> '530 Please login with USER and PASS.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_auth_tls> 'AUTH TLS\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_auth_tls> '530 Please login with USER and PASS.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_auth_tls> 'AUTH TLS\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_auth_tls> '530 Please login with USER and PASS.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_auth_ssl> 'AUTH SSL\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_auth_ssl> '530 Please login with USER and PASS.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50047|)\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_utf8> 'OPTS UTF8 ON\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_set_utf8> '200 Always in UTF8 mode.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.95%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50094|)\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50078|)\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.95%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50080|)\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50077|)\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.95%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_syst> 'SYST\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_syst> '215 UNIX Type: L8\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50073|)\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50062|)\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.95%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50089|)\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50091|)\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.95%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50093|)\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50099|)\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.95%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_auth_tls> 'AUTH TLS\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_auth_tls> '530 Please login with USER and PASS.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_auth_tls> 'AUTH TLS\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_auth_tls> '530 Please login with USER and PASS.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_auth_tls> 'AUTH TLS\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_auth_tls> '530 Please login with USER and PASS.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_fail> 'PASS DIru\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_fail> '530 Login incorrect.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50062|)\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.95%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_auth_tls> 'AUTH TLS\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_auth_tls> '530 Please login with USER and PASS.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50058|)\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.95%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_syst> 'SYST\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_syst> '215 UNIX Type: L8\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 4.
fandango:INFO: ClientControl -> ServerControl: <request_syst> 'SYST\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_syst> '215 UNIX Type: L8\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50065|)\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_auth_tls> 'AUTH TLS\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_auth_tls> '530 Please login with USER and PASS.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 4.
fandango:INFO: ClientControl -> ServerControl: <request_feat> 'FEAT\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_feat> '211-Features:\r\n EPRT\r\n EPSV\r\n MDTM\r\n PASV\r\n REST STREAM\r\n SIZE\r\n TVFS\r\n UTF8\r\n211 End\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50013|)\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_auth_tls> 'AUTH TLS\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_auth_tls> '530 Please login with USER and PASS.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_feat> 'FEAT\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_feat> '211-Features:\r\n EPRT\r\n EPSV\r\n MDTM\r\n PASV\r\n REST STREAM\r\n SIZE\r\n TVFS\r\n UTF8\r\n211 End\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_syst> 'SYST\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_syst> '215 UNIX Type: L8\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50063|)\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50042|)\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_auth_tls> 'AUTH TLS\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_auth_tls> '530 Please login with USER and PASS.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ClientControl -> ServerControl: <request_login_user_fail> 'USER yXn_1Rh6Z\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_fail> '530 Login incorrect.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50009|)\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50045|)\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50031|)\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_syst> 'SYST\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_syst> '215 UNIX Type: L8\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50012|)\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 4.
fandango:INFO: ClientControl -> ServerControl: <request_set_utf8> 'OPTS UTF8 ON\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_set_utf8> '200 Always in UTF8 mode.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_auth_tls> 'AUTH TLS\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_auth_tls> '530 Please login with USER and PASS.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_auth_tls> 'AUTH TLS\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_auth_tls> '530 Please login with USER and PASS.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ClientControl -> ServerControl: <request_login_user_fail> 'USER bIgXE4hoHM1nfiFmYGwE\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_fail> 'PASS 3YkSZPs1fqKA\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_fail> '530 Login incorrect.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50026|)\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_utf8> 'OPTS UTF8 ON\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_set_utf8> '200 Always in UTF8 mode.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50095|)\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50064|)\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50035|)\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50006|)\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50051|)\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_feat> 'FEAT\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_feat> '211-Features:\r\n EPRT\r\n EPSV\r\n MDTM\r\n PASV\r\n REST STREAM\r\n SIZE\r\n TVFS\r\n UTF8\r\n211 End\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50004|)\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_feat> 'FEAT\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_feat> '211-Features:\r\n EPRT\r\n EPSV\r\n MDTM\r\n PASV\r\n REST STREAM\r\n SIZE\r\n TVFS\r\n UTF8\r\n211 End\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50100|)\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50014|)\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50041|)\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50091|)\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50067|)\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50056|)\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 4.
fandango:INFO: ClientControl -> ServerControl: <request_feat> 'FEAT\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_feat> '211-Features:\r\n EPRT\r\n EPSV\r\n MDTM\r\n PASV\r\n REST STREAM\r\n SIZE\r\n TVFS\r\n UTF8\r\n211 End\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50076|)\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50040|)\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_auth_tls> 'AUTH TLS\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_auth_tls> '530 Please login with USER and PASS.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_auth_tls> 'AUTH TLS\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_auth_tls> '530 Please login with USER and PASS.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ClientControl -> ServerControl: <request_login_user_fail> 'USER 0FkeYn\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_fail> '530 Login incorrect.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50081|)\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50011|)\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_utf8> 'OPTS UTF8 ON\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_set_utf8> '200 Always in UTF8 mode.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.98%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50025|)\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_utf8> 'OPTS UTF8 ON\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_set_utf8> '200 Always in UTF8 mode.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.98%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_feat> 'FEAT\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_feat> '211-Features:\r\n EPRT\r\n EPSV\r\n MDTM\r\n PASV\r\n REST STREAM\r\n SIZE\r\n TVFS\r\n UTF8\r\n211 End\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50019|)\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.98%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50036|)\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 5.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_utf8> 'OPTS UTF8 ON\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_set_utf8> '200 Always in UTF8 mode.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.98%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_utf8> 'OPTS UTF8 ON\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_set_utf8> '200 Always in UTF8 mode.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50050|)\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50061|)\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.98%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_auth_tls> 'AUTH TLS\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_auth_tls> '530 Please login with USER and PASS.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_auth_tls> 'AUTH TLS\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_auth_tls> '530 Please login with USER and PASS.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 6.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50077|)\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_syst> 'SYST\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_syst> '215 UNIX Type: L8\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50048|)\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50068|)\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.98%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50022|)\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_utf8> 'OPTS UTF8 ON\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_set_utf8> '200 Always in UTF8 mode.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.98%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_utf8> 'OPTS UTF8 ON\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_set_utf8> '200 Always in UTF8 mode.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50062|)\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_feat> 'FEAT\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_feat> '211-Features:\r\n EPRT\r\n EPSV\r\n MDTM\r\n PASV\r\n REST STREAM\r\n SIZE\r\n TVFS\r\n UTF8\r\n211 End\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50005|)\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_syst> 'SYST\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_syst> '215 UNIX Type: L8\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_utf8> 'OPTS UTF8 ON\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_set_utf8> '200 Always in UTF8 mode.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50041|)\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 4.
fandango:INFO: ClientControl -> ServerControl: <request_syst> 'SYST\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_syst> '215 UNIX Type: L8\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50015|)\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.99%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50025|)\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50021|)\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_feat> 'FEAT\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_feat> '211-Features:\r\n EPRT\r\n EPSV\r\n MDTM\r\n PASV\r\n REST STREAM\r\n SIZE\r\n TVFS\r\n UTF8\r\n211 End\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50029|)\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50083|)\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.99%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_auth_tls> 'AUTH TLS\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_auth_tls> '530 Please login with USER and PASS.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_syst> 'SYST\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_syst> '215 UNIX Type: L8\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50066|)\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_utf8> 'OPTS UTF8 ON\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_set_utf8> '200 Always in UTF8 mode.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50060|)\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.99%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50076|)\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50070|)\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.99%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50071|)\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_syst> 'SYST\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_syst> '215 UNIX Type: L8\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50043|)\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50089|)\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.99%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50007|)\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50045|)\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.99%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50017|)\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50064|)\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.99%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_syst> 'SYST\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_syst> '215 UNIX Type: L8\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50061|)\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50005|)\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 0.99%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50084|)\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_syst> 'SYST\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_syst> '215 UNIX Type: L8\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50018|)\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_feat> 'FEAT\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_feat> '211-Features:\r\n EPRT\r\n EPSV\r\n MDTM\r\n PASV\r\n REST STREAM\r\n SIZE\r\n TVFS\r\n UTF8\r\n211 End\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50049|)\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 5.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50029|)\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50050|)\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_syst> 'SYST\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_syst> '215 UNIX Type: L8\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50058|)\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50085|)\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_syst> 'SYST\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_syst> '215 UNIX Type: L8\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50047|)\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50027|)\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_syst> 'SYST\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_syst> '215 UNIX Type: L8\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50000|)\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50007|)\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50030|)\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50085|)\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_utf8> 'OPTS UTF8 ON\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_set_utf8> '200 Always in UTF8 mode.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50001|)\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50078|)\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50040|)\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50056|)\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50055|)\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50017|)\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_pwd> 'PWD\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_pwd> '257 "/ftp/the_user" is the current directory\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_feat> 'FEAT\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_feat> '211-Features:\r\n EPRT\r\n EPSV\r\n MDTM\r\n PASV\r\n REST STREAM\r\n SIZE\r\n TVFS\r\n UTF8\r\n211 End\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50055|)\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_server_info> '220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_user_ok> 'USER the_user\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_login_user> '331 Please specify the password.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_login_pass_ok> 'PASS the_password\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_login_pass_ok> '230 Login successful.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50089|)\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_type> 'TYPE I\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_set_type> '200 Switching to Binary mode.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_list> 'LIST\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <open_list> '150 Here comes the directory listing.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerData -> ClientData: <list_data> 'drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <finalize_list> '226 Directory send OK.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_feat> 'FEAT\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_feat> '211-Features:\r\n EPRT\r\n EPSV\r\n MDTM\r\n PASV\r\n REST STREAM\r\n SIZE\r\n TVFS\r\n UTF8\r\n211 End\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Full coverage reached. Guiding to end of tree.
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_set_epassive> 'EPSV\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_set_epassive> '229 Entering Extended Passive Mode (|||50007|)\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Full coverage reached. Guiding to end of tree.
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: ClientControl -> ServerControl: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: ServerControl -> ClientControl: <response_quit> '221 Goodbye.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Full coverage reached. Guiding to end of tree.
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: StdOut: <state_finished> ''
fandango:INFO: Current coverage: 1.00%
220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
TYPE I
200 Switching to Binary mode.
PWD
257 "/ftp/the_user" is the current directory
EPSV
229 Entering Extended Passive Mode (|||50012|)
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
PWD
257 "/ftp/the_user" is the current directory
PWD
257 "/ftp/the_user" is the current directory
PWD
257 "/ftp/the_user" is the current directory
PWD
257 "/ftp/the_user" is the current directory
PWD
257 "/ftp/the_user" is the current directory
EPSV
229 Entering Extended Passive Mode (|||50027|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
EPSV
229 Entering Extended Passive Mode (|||50026|)
TYPE I
200 Switching to Binary mode.
PWD
257 "/ftp/the_user" is the current directory
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50091|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
EPSV
229 Entering Extended Passive Mode (|||50018|)
TYPE I
200 Switching to Binary mode.
PWD
257 "/ftp/the_user" is the current directory
FEAT
211-Features:
 EPRT
 EPSV
 MDTM
 PASV
 REST STREAM
 SIZE
 TVFS
 UTF8
211 End
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
AUTH TLS
530 Please login with USER and PASS.
AUTH TLS
530 Please login with USER and PASS.
USER the_user
331 Please specify the password.
PASS x9_GEihi_Q8zpD0_9h
530 Login incorrect.
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
TYPE I
200 Switching to Binary mode.
EPSV
229 Entering Extended Passive Mode (|||50000|)
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50012|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
EPSV
229 Entering Extended Passive Mode (|||50037|)
SYST
215 UNIX Type: L8
TYPE I
200 Switching to Binary mode.
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
PWD
257 "/ftp/the_user" is the current directory
EPSV
229 Entering Extended Passive Mode (|||50078|)
PWD
257 "/ftp/the_user" is the current directory
TYPE I
200 Switching to Binary mode.
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
PWD
257 "/ftp/the_user" is the current directory
TYPE I
200 Switching to Binary mode.
FEAT
211-Features:
 EPRT
 EPSV
 MDTM
 PASV
 REST STREAM
 SIZE
 TVFS
 UTF8
211 End
EPSV
229 Entering Extended Passive Mode (|||50023|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
EPSV
229 Entering Extended Passive Mode (|||50035|)
TYPE I
200 Switching to Binary mode.
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50078|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
FEAT
211-Features:
 EPRT
 EPSV
 MDTM
 PASV
 REST STREAM
 SIZE
 TVFS
 UTF8
211 End
TYPE I
200 Switching to Binary mode.
EPSV
229 Entering Extended Passive Mode (|||50090|)
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50071|)
OPTS UTF8 ON
200 Always in UTF8 mode.
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
EPSV
229 Entering Extended Passive Mode (|||50038|)
PWD
257 "/ftp/the_user" is the current directory
PWD
257 "/ftp/the_user" is the current directory
TYPE I
200 Switching to Binary mode.
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
TYPE I
200 Switching to Binary mode.
EPSV
229 Entering Extended Passive Mode (|||50040|)
SYST
215 UNIX Type: L8
PWD
257 "/ftp/the_user" is the current directory
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50061|)
PWD
257 "/ftp/the_user" is the current directory
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50000|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
EPSV
229 Entering Extended Passive Mode (|||50084|)
PWD
257 "/ftp/the_user" is the current directory
SYST
215 UNIX Type: L8
TYPE I
200 Switching to Binary mode.
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
PWD
257 "/ftp/the_user" is the current directory
OPTS UTF8 ON
200 Always in UTF8 mode.
EPSV
229 Entering Extended Passive Mode (|||50096|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
AUTH TLS
530 Please login with USER and PASS.
AUTH SSL
530 Please login with USER and PASS.
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
EPSV
229 Entering Extended Passive Mode (|||50007|)
PWD
257 "/ftp/the_user" is the current directory
TYPE I
200 Switching to Binary mode.
PWD
257 "/ftp/the_user" is the current directory
SYST
215 UNIX Type: L8
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
PWD
257 "/ftp/the_user" is the current directory
OPTS UTF8 ON
200 Always in UTF8 mode.
TYPE I
200 Switching to Binary mode.
EPSV
229 Entering Extended Passive Mode (|||50044|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
AUTH TLS
530 Please login with USER and PASS.
USER the_user
331 Please specify the password.
PASS jITz6fbgOY9m0QCcD
530 Login incorrect.
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
TYPE I
200 Switching to Binary mode.
EPSV
229 Entering Extended Passive Mode (|||50004|)
FEAT
211-Features:
 EPRT
 EPSV
 MDTM
 PASV
 REST STREAM
 SIZE
 TVFS
 UTF8
211 End
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
AUTH TLS
530 Please login with USER and PASS.
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
OPTS UTF8 ON
200 Always in UTF8 mode.
TYPE I
200 Switching to Binary mode.
EPSV
229 Entering Extended Passive Mode (|||50033|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
AUTH SSL
530 Please login with USER and PASS.
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
EPSV
229 Entering Extended Passive Mode (|||50003|)
TYPE I
200 Switching to Binary mode.
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50002|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
EPSV
229 Entering Extended Passive Mode (|||50056|)
TYPE I
200 Switching to Binary mode.
PWD
257 "/ftp/the_user" is the current directory
PWD
257 "/ftp/the_user" is the current directory
FEAT
211-Features:
 EPRT
 EPSV
 MDTM
 PASV
 REST STREAM
 SIZE
 TVFS
 UTF8
211 End
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
PWD
257 "/ftp/the_user" is the current directory
EPSV
229 Entering Extended Passive Mode (|||50071|)
TYPE I
200 Switching to Binary mode.
SYST
215 UNIX Type: L8
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50064|)
PWD
257 "/ftp/the_user" is the current directory
FEAT
211-Features:
 EPRT
 EPSV
 MDTM
 PASV
 REST STREAM
 SIZE
 TVFS
 UTF8
211 End
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
EPSV
229 Entering Extended Passive Mode (|||50004|)
TYPE I
200 Switching to Binary mode.
PWD
257 "/ftp/the_user" is the current directory
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS C_cjUZu46byX7
530 Login incorrect.
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
TYPE I
200 Switching to Binary mode.
PWD
257 "/ftp/the_user" is the current directory
FEAT
211-Features:
 EPRT
 EPSV
 MDTM
 PASV
 REST STREAM
 SIZE
 TVFS
 UTF8
211 End
EPSV
229 Entering Extended Passive Mode (|||50091|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
EPSV
229 Entering Extended Passive Mode (|||50088|)
PWD
257 "/ftp/the_user" is the current directory
PWD
257 "/ftp/the_user" is the current directory
PWD
257 "/ftp/the_user" is the current directory
TYPE I
200 Switching to Binary mode.
PWD
257 "/ftp/the_user" is the current directory
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
TYPE I
200 Switching to Binary mode.
SYST
215 UNIX Type: L8
EPSV
229 Entering Extended Passive Mode (|||50007|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
EPSV
229 Entering Extended Passive Mode (|||50084|)
PWD
257 "/ftp/the_user" is the current directory
PWD
257 "/ftp/the_user" is the current directory
FEAT
211-Features:
 EPRT
 EPSV
 MDTM
 PASV
 REST STREAM
 SIZE
 TVFS
 UTF8
211 End
TYPE I
200 Switching to Binary mode.
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
PWD
257 "/ftp/the_user" is the current directory
EPSV
229 Entering Extended Passive Mode (|||50026|)
OPTS UTF8 ON
200 Always in UTF8 mode.
TYPE I
200 Switching to Binary mode.
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
TYPE I
200 Switching to Binary mode.
PWD
257 "/ftp/the_user" is the current directory
EPSV
229 Entering Extended Passive Mode (|||50083|)
FEAT
211-Features:
 EPRT
 EPSV
 MDTM
 PASV
 REST STREAM
 SIZE
 TVFS
 UTF8
211 End
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50021|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
PWD
257 "/ftp/the_user" is the current directory
FEAT
211-Features:
 EPRT
 EPSV
 MDTM
 PASV
 REST STREAM
 SIZE
 TVFS
 UTF8
211 End
TYPE I
200 Switching to Binary mode.
EPSV
229 Entering Extended Passive Mode (|||50035|)
PWD
257 "/ftp/the_user" is the current directory
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
PWD
257 "/ftp/the_user" is the current directory
SYST
215 UNIX Type: L8
EPSV
229 Entering Extended Passive Mode (|||50056|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
EPSV
229 Entering Extended Passive Mode (|||50076|)
PWD
257 "/ftp/the_user" is the current directory
TYPE I
200 Switching to Binary mode.
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50022|)
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50018|)
OPTS UTF8 ON
200 Always in UTF8 mode.
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
EPSV
229 Entering Extended Passive Mode (|||50082|)
PWD
257 "/ftp/the_user" is the current directory
OPTS UTF8 ON
200 Always in UTF8 mode.
TYPE I
200 Switching to Binary mode.
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50055|)
PWD
257 "/ftp/the_user" is the current directory
PWD
257 "/ftp/the_user" is the current directory
OPTS UTF8 ON
200 Always in UTF8 mode.
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50031|)
PWD
257 "/ftp/the_user" is the current directory
PWD
257 "/ftp/the_user" is the current directory
PWD
257 "/ftp/the_user" is the current directory
SYST
215 UNIX Type: L8
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
PWD
257 "/ftp/the_user" is the current directory
PWD
257 "/ftp/the_user" is the current directory
OPTS UTF8 ON
200 Always in UTF8 mode.
TYPE I
200 Switching to Binary mode.
EPSV
229 Entering Extended Passive Mode (|||50098|)
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50023|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
EPSV
229 Entering Extended Passive Mode (|||50093|)
TYPE I
200 Switching to Binary mode.
FEAT
211-Features:
 EPRT
 EPSV
 MDTM
 PASV
 REST STREAM
 SIZE
 TVFS
 UTF8
211 End
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50089|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
EPSV
229 Entering Extended Passive Mode (|||50075|)
TYPE I
200 Switching to Binary mode.
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50002|)
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50015|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
TYPE I
200 Switching to Binary mode.
OPTS UTF8 ON
200 Always in UTF8 mode.
EPSV
229 Entering Extended Passive Mode (|||50047|)
PWD
257 "/ftp/the_user" is the current directory
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
PWD
257 "/ftp/the_user" is the current directory
PWD
257 "/ftp/the_user" is the current directory
EPSV
229 Entering Extended Passive Mode (|||50067|)
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50040|)
PWD
257 "/ftp/the_user" is the current directory
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50070|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
AUTH TLS
530 Please login with USER and PASS.
AUTH TLS
530 Please login with USER and PASS.
AUTH SSL
530 Please login with USER and PASS.
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
TYPE I
200 Switching to Binary mode.
EPSV
229 Entering Extended Passive Mode (|||50022|)
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50092|)
PWD
257 "/ftp/the_user" is the current directory
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50010|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
AUTH TLS
530 Please login with USER and PASS.
AUTH TLS
530 Please login with USER and PASS.
AUTH TLS
530 Please login with USER and PASS.
AUTH TLS
530 Please login with USER and PASS.
AUTH TLS
530 Please login with USER and PASS.
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
TYPE I
200 Switching to Binary mode.
EPSV
229 Entering Extended Passive Mode (|||50011|)
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50081|)
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50009|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
SYST
215 UNIX Type: L8
TYPE I
200 Switching to Binary mode.
EPSV
229 Entering Extended Passive Mode (|||50013|)
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50100|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER bF_MF9ZqpvLCuKTtJs6
331 Please specify the password.
PASS the_password
530 Login incorrect.
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
TYPE I
200 Switching to Binary mode.
PWD
257 "/ftp/the_user" is the current directory
PWD
257 "/ftp/the_user" is the current directory
EPSV
229 Entering Extended Passive Mode (|||50022|)
FEAT
211-Features:
 EPRT
 EPSV
 MDTM
 PASV
 REST STREAM
 SIZE
 TVFS
 UTF8
211 End
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
PWD
257 "/ftp/the_user" is the current directory
PWD
257 "/ftp/the_user" is the current directory
EPSV
229 Entering Extended Passive Mode (|||50059|)
TYPE I
200 Switching to Binary mode.
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
OPTS UTF8 ON
200 Always in UTF8 mode.
EPSV
229 Entering Extended Passive Mode (|||50046|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
PWD
257 "/ftp/the_user" is the current directory
EPSV
229 Entering Extended Passive Mode (|||50061|)
FEAT
211-Features:
 EPRT
 EPSV
 MDTM
 PASV
 REST STREAM
 SIZE
 TVFS
 UTF8
211 End
TYPE I
200 Switching to Binary mode.
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50014|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
TYPE I
200 Switching to Binary mode.
EPSV
229 Entering Extended Passive Mode (|||50065|)
OPTS UTF8 ON
200 Always in UTF8 mode.
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
EPSV
229 Entering Extended Passive Mode (|||50046|)
TYPE I
200 Switching to Binary mode.
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50086|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
PWD
257 "/ftp/the_user" is the current directory
PWD
257 "/ftp/the_user" is the current directory
EPSV
229 Entering Extended Passive Mode (|||50002|)
PWD
257 "/ftp/the_user" is the current directory
TYPE I
200 Switching to Binary mode.
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
EPSV
229 Entering Extended Passive Mode (|||50015|)
FEAT
211-Features:
 EPRT
 EPSV
 MDTM
 PASV
 REST STREAM
 SIZE
 TVFS
 UTF8
211 End
TYPE I
200 Switching to Binary mode.
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
PWD
257 "/ftp/the_user" is the current directory
EPSV
229 Entering Extended Passive Mode (|||50028|)
TYPE I
200 Switching to Binary mode.
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
TYPE I
200 Switching to Binary mode.
EPSV
229 Entering Extended Passive Mode (|||50037|)
PWD
257 "/ftp/the_user" is the current directory
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50057|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
PWD
257 "/ftp/the_user" is the current directory
TYPE I
200 Switching to Binary mode.
PWD
257 "/ftp/the_user" is the current directory
PWD
257 "/ftp/the_user" is the current directory
OPTS UTF8 ON
200 Always in UTF8 mode.
EPSV
229 Entering Extended Passive Mode (|||50096|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
EPSV
229 Entering Extended Passive Mode (|||50017|)
PWD
257 "/ftp/the_user" is the current directory
FEAT
211-Features:
 EPRT
 EPSV
 MDTM
 PASV
 REST STREAM
 SIZE
 TVFS
 UTF8
211 End
TYPE I
200 Switching to Binary mode.
FEAT
211-Features:
 EPRT
 EPSV
 MDTM
 PASV
 REST STREAM
 SIZE
 TVFS
 UTF8
211 End
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
TYPE I
200 Switching to Binary mode.
EPSV
229 Entering Extended Passive Mode (|||50003|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
PWD
257 "/ftp/the_user" is the current directory
EPSV
229 Entering Extended Passive Mode (|||50014|)
PWD
257 "/ftp/the_user" is the current directory
PWD
257 "/ftp/the_user" is the current directory
TYPE I
200 Switching to Binary mode.
PWD
257 "/ftp/the_user" is the current directory
PWD
257 "/ftp/the_user" is the current directory
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50088|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
AUTH TLS
530 Please login with USER and PASS.
AUTH TLS
530 Please login with USER and PASS.
AUTH TLS
530 Please login with USER and PASS.
AUTH SSL
530 Please login with USER and PASS.
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
EPSV
229 Entering Extended Passive Mode (|||50047|)
TYPE I
200 Switching to Binary mode.
OPTS UTF8 ON
200 Always in UTF8 mode.
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
TYPE I
200 Switching to Binary mode.
EPSV
229 Entering Extended Passive Mode (|||50094|)
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50078|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
EPSV
229 Entering Extended Passive Mode (|||50080|)
PWD
257 "/ftp/the_user" is the current directory
TYPE I
200 Switching to Binary mode.
PWD
257 "/ftp/the_user" is the current directory
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50077|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
TYPE I
200 Switching to Binary mode.
PWD
257 "/ftp/the_user" is the current directory
SYST
215 UNIX Type: L8
EPSV
229 Entering Extended Passive Mode (|||50073|)
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50062|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
TYPE I
200 Switching to Binary mode.
EPSV
229 Entering Extended Passive Mode (|||50089|)
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50091|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
EPSV
229 Entering Extended Passive Mode (|||50093|)
TYPE I
200 Switching to Binary mode.
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50099|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
AUTH TLS
530 Please login with USER and PASS.
AUTH TLS
530 Please login with USER and PASS.
AUTH TLS
530 Please login with USER and PASS.
USER the_user
331 Please specify the password.
PASS DIru
530 Login incorrect.
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
EPSV
229 Entering Extended Passive Mode (|||50062|)
TYPE I
200 Switching to Binary mode.
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
AUTH TLS
530 Please login with USER and PASS.
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
PWD
257 "/ftp/the_user" is the current directory
EPSV
229 Entering Extended Passive Mode (|||50058|)
TYPE I
200 Switching to Binary mode.
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
PWD
257 "/ftp/the_user" is the current directory
SYST
215 UNIX Type: L8
TYPE I
200 Switching to Binary mode.
SYST
215 UNIX Type: L8
EPSV
229 Entering Extended Passive Mode (|||50065|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
AUTH TLS
530 Please login with USER and PASS.
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
PWD
257 "/ftp/the_user" is the current directory
FEAT
211-Features:
 EPRT
 EPSV
 MDTM
 PASV
 REST STREAM
 SIZE
 TVFS
 UTF8
211 End
TYPE I
200 Switching to Binary mode.
EPSV
229 Entering Extended Passive Mode (|||50013|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
AUTH TLS
530 Please login with USER and PASS.
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
FEAT
211-Features:
 EPRT
 EPSV
 MDTM
 PASV
 REST STREAM
 SIZE
 TVFS
 UTF8
211 End
TYPE I
200 Switching to Binary mode.
PWD
257 "/ftp/the_user" is the current directory
PWD
257 "/ftp/the_user" is the current directory
SYST
215 UNIX Type: L8
EPSV
229 Entering Extended Passive Mode (|||50063|)
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50042|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
AUTH TLS
530 Please login with USER and PASS.
USER yXn_1Rh6Z
331 Please specify the password.
PASS the_password
530 Login incorrect.
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
TYPE I
200 Switching to Binary mode.
EPSV
229 Entering Extended Passive Mode (|||50009|)
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50045|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
EPSV
229 Entering Extended Passive Mode (|||50031|)
PWD
257 "/ftp/the_user" is the current directory
PWD
257 "/ftp/the_user" is the current directory
SYST
215 UNIX Type: L8
TYPE I
200 Switching to Binary mode.
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
PWD
257 "/ftp/the_user" is the current directory
EPSV
229 Entering Extended Passive Mode (|||50012|)
PWD
257 "/ftp/the_user" is the current directory
OPTS UTF8 ON
200 Always in UTF8 mode.
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
AUTH TLS
530 Please login with USER and PASS.
AUTH TLS
530 Please login with USER and PASS.
USER bIgXE4hoHM1nfiFmYGwE
331 Please specify the password.
PASS 3YkSZPs1fqKA
530 Login incorrect.
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
TYPE I
200 Switching to Binary mode.
EPSV
229 Entering Extended Passive Mode (|||50026|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
OPTS UTF8 ON
200 Always in UTF8 mode.
TYPE I
200 Switching to Binary mode.
EPSV
229 Entering Extended Passive Mode (|||50095|)
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50064|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
EPSV
229 Entering Extended Passive Mode (|||50035|)
TYPE I
200 Switching to Binary mode.
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50006|)
PWD
257 "/ftp/the_user" is the current directory
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50051|)
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
PWD
257 "/ftp/the_user" is the current directory
FEAT
211-Features:
 EPRT
 EPSV
 MDTM
 PASV
 REST STREAM
 SIZE
 TVFS
 UTF8
211 End
EPSV
229 Entering Extended Passive Mode (|||50004|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
PWD
257 "/ftp/the_user" is the current directory
PWD
257 "/ftp/the_user" is the current directory
FEAT
211-Features:
 EPRT
 EPSV
 MDTM
 PASV
 REST STREAM
 SIZE
 TVFS
 UTF8
211 End
EPSV
229 Entering Extended Passive Mode (|||50100|)
TYPE I
200 Switching to Binary mode.
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50014|)
PWD
257 "/ftp/the_user" is the current directory
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50041|)
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50091|)
PWD
257 "/ftp/the_user" is the current directory
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50067|)
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50056|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
PWD
257 "/ftp/the_user" is the current directory
PWD
257 "/ftp/the_user" is the current directory
PWD
257 "/ftp/the_user" is the current directory
FEAT
211-Features:
 EPRT
 EPSV
 MDTM
 PASV
 REST STREAM
 SIZE
 TVFS
 UTF8
211 End
TYPE I
200 Switching to Binary mode.
EPSV
229 Entering Extended Passive Mode (|||50076|)
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50040|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
AUTH TLS
530 Please login with USER and PASS.
AUTH TLS
530 Please login with USER and PASS.
USER 0FkeYn
331 Please specify the password.
PASS the_password
530 Login incorrect.
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
TYPE I
200 Switching to Binary mode.
EPSV
229 Entering Extended Passive Mode (|||50081|)
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
PWD
257 "/ftp/the_user" is the current directory
EPSV
229 Entering Extended Passive Mode (|||50011|)
OPTS UTF8 ON
200 Always in UTF8 mode.
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
EPSV
229 Entering Extended Passive Mode (|||50025|)
OPTS UTF8 ON
200 Always in UTF8 mode.
TYPE I
200 Switching to Binary mode.
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
TYPE I
200 Switching to Binary mode.
FEAT
211-Features:
 EPRT
 EPSV
 MDTM
 PASV
 REST STREAM
 SIZE
 TVFS
 UTF8
211 End
EPSV
229 Entering Extended Passive Mode (|||50019|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
EPSV
229 Entering Extended Passive Mode (|||50036|)
PWD
257 "/ftp/the_user" is the current directory
PWD
257 "/ftp/the_user" is the current directory
PWD
257 "/ftp/the_user" is the current directory
PWD
257 "/ftp/the_user" is the current directory
TYPE I
200 Switching to Binary mode.
PWD
257 "/ftp/the_user" is the current directory
OPTS UTF8 ON
200 Always in UTF8 mode.
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
TYPE I
200 Switching to Binary mode.
PWD
257 "/ftp/the_user" is the current directory
OPTS UTF8 ON
200 Always in UTF8 mode.
EPSV
229 Entering Extended Passive Mode (|||50050|)
PWD
257 "/ftp/the_user" is the current directory
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50061|)
QUIT
221 Goodbye.

fandango:INFO: Full coverage reached, stopping evolution.
220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
AUTH TLS
530 Please login with USER and PASS.
AUTH TLS
530 Please login with USER and PASS.
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
PWD
257 "/ftp/the_user" is the current directory
TYPE I
200 Switching to Binary mode.
EPSV
229 Entering Extended Passive Mode (|||50077|)
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
SYST
215 UNIX Type: L8
EPSV
229 Entering Extended Passive Mode (|||50048|)
PWD
257 "/ftp/the_user" is the current directory
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50068|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
EPSV
229 Entering Extended Passive Mode (|||50022|)
PWD
257 "/ftp/the_user" is the current directory
TYPE I
200 Switching to Binary mode.
OPTS UTF8 ON
200 Always in UTF8 mode.
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
PWD
257 "/ftp/the_user" is the current directory
TYPE I
200 Switching to Binary mode.
OPTS UTF8 ON
200 Always in UTF8 mode.
EPSV
229 Entering Extended Passive Mode (|||50062|)
PWD
257 "/ftp/the_user" is the current directory
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
PWD
257 "/ftp/the_user" is the current directory
PWD
257 "/ftp/the_user" is the current directory
FEAT
211-Features:
 EPRT
 EPSV
 MDTM
 PASV
 REST STREAM
 SIZE
 TVFS
 UTF8
211 End
EPSV
229 Entering Extended Passive Mode (|||50005|)
SYST
215 UNIX Type: L8
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
OPTS UTF8 ON
200 Always in UTF8 mode.
EPSV
229 Entering Extended Passive Mode (|||50041|)
PWD
257 "/ftp/the_user" is the current directory
PWD
257 "/ftp/the_user" is the current directory
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
SYST
215 UNIX Type: L8
EPSV
229 Entering Extended Passive Mode (|||50015|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
EPSV
229 Entering Extended Passive Mode (|||50025|)
TYPE I
200 Switching to Binary mode.
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
PWD
257 "/ftp/the_user" is the current directory
EPSV
229 Entering Extended Passive Mode (|||50021|)
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
FEAT
211-Features:
 EPRT
 EPSV
 MDTM
 PASV
 REST STREAM
 SIZE
 TVFS
 UTF8
211 End
EPSV
229 Entering Extended Passive Mode (|||50029|)
PWD
257 "/ftp/the_user" is the current directory
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50083|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
AUTH TLS
530 Please login with USER and PASS.
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
SYST
215 UNIX Type: L8
EPSV
229 Entering Extended Passive Mode (|||50066|)
PWD
257 "/ftp/the_user" is the current directory
PWD
257 "/ftp/the_user" is the current directory
OPTS UTF8 ON
200 Always in UTF8 mode.
TYPE I
200 Switching to Binary mode.
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50060|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
EPSV
229 Entering Extended Passive Mode (|||50076|)
TYPE I
200 Switching to Binary mode.
PWD
257 "/ftp/the_user" is the current directory
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50070|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
PWD
257 "/ftp/the_user" is the current directory
EPSV
229 Entering Extended Passive Mode (|||50071|)
SYST
215 UNIX Type: L8
TYPE I
200 Switching to Binary mode.
PWD
257 "/ftp/the_user" is the current directory
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50043|)
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50089|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
EPSV
229 Entering Extended Passive Mode (|||50007|)
TYPE I
200 Switching to Binary mode.
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50045|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
EPSV
229 Entering Extended Passive Mode (|||50017|)
TYPE I
200 Switching to Binary mode.
PWD
257 "/ftp/the_user" is the current directory
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50064|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
PWD
257 "/ftp/the_user" is the current directory
PWD
257 "/ftp/the_user" is the current directory
SYST
215 UNIX Type: L8
EPSV
229 Entering Extended Passive Mode (|||50061|)
TYPE I
200 Switching to Binary mode.
PWD
257 "/ftp/the_user" is the current directory
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50005|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
EPSV
229 Entering Extended Passive Mode (|||50084|)
PWD
257 "/ftp/the_user" is the current directory
TYPE I
200 Switching to Binary mode.
SYST
215 UNIX Type: L8
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50018|)
FEAT
211-Features:
 EPRT
 EPSV
 MDTM
 PASV
 REST STREAM
 SIZE
 TVFS
 UTF8
211 End
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
EPSV
229 Entering Extended Passive Mode (|||50049|)
TYPE I
200 Switching to Binary mode.
PWD
257 "/ftp/the_user" is the current directory
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
PWD
257 "/ftp/the_user" is the current directory
EPSV
229 Entering Extended Passive Mode (|||50029|)
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50050|)
SYST
215 UNIX Type: L8
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
EPSV
229 Entering Extended Passive Mode (|||50058|)
TYPE I
200 Switching to Binary mode.
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50085|)
PWD
257 "/ftp/the_user" is the current directory
SYST
215 UNIX Type: L8
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50047|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
EPSV
229 Entering Extended Passive Mode (|||50027|)
TYPE I
200 Switching to Binary mode.
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
SYST
215 UNIX Type: L8
EPSV
229 Entering Extended Passive Mode (|||50000|)
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50007|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
EPSV
229 Entering Extended Passive Mode (|||50030|)
TYPE I
200 Switching to Binary mode.
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50085|)
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
OPTS UTF8 ON
200 Always in UTF8 mode.
EPSV
229 Entering Extended Passive Mode (|||50001|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
EPSV
229 Entering Extended Passive Mode (|||50078|)
TYPE I
200 Switching to Binary mode.
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50040|)
PWD
257 "/ftp/the_user" is the current directory
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50056|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
EPSV
229 Entering Extended Passive Mode (|||50055|)
TYPE I
200 Switching to Binary mode.
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
EPSV
229 Entering Extended Passive Mode (|||50017|)
PWD
257 "/ftp/the_user" is the current directory
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
FEAT
211-Features:
 EPRT
 EPSV
 MDTM
 PASV
 REST STREAM
 SIZE
 TVFS
 UTF8
211 End
EPSV
229 Entering Extended Passive Mode (|||50055|)
QUIT
221 Goodbye.

220 Welcome Alpine ftp server https://hub.docker.com/r/delfer/alpine-ftp-server/
USER the_user
331 Please specify the password.
PASS the_password
230 Login successful.
EPSV
229 Entering Extended Passive Mode (|||50089|)
TYPE I
200 Switching to Binary mode.
LIST
150 Here comes the directory listing.
drwxr-xr-x    2 1000     1000         4096 Sep 02 09:58 test
226 Directory send OK.
FEAT
211-Features:
 EPRT
 EPSV
 MDTM
 PASV
 REST STREAM
 SIZE
 TVFS
 UTF8
211 End
EPSV
229 Entering Extended Passive Mode (|||50007|)
QUIT
221 Goodbye.

Coverage log:
Nr trees generated: 91
Nr messages exchanged: 2092
Overall time elapsed: 589.75s

Process finished with exit code 0

This is the run where the number of max failed login attempts per session gets limited using a constraint.