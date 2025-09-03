/Users/alexander/PycharmProjects/fandango/.venv/bin/python /Users/alexander/PycharmProjects/fandango/evaluation/experiments/smtp/smtp.py 
fandango:WARNING: Symbol <unix_time> defined, but not used
fandango:WARNING: Symbol <mail_contents> defined, but not used
fandango:WARNING: Symbol <user_incorrect> defined, but not used
fandango:WARNING: Symbol <pass_incorrect> defined, but not used
fandango:INFO: ---------- Initializing FANDANGO algorithm ---------- 
fandango:INFO: Generating (additional) initial population (size: 100)...
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Initial population generated in 0.00 seconds
fandango:INFO: Current coverage: 0.00%
fandango:INFO: Server: <response_setup> '220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\n'
fandango:INFO: Current coverage: 0.03%
fandango:INFO: Client: <request_ehlo> 'EHLO t3m X7 pGjafpblNq  VrGiYe  ZODy7zu0oOCn  PkxCe8.UuVgxkQDIH  d  ooJ-9WpuX5tRwgl  \r\n'
fandango:INFO: Current coverage: 0.05%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.11%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.14%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.15%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.17%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.18%
fandango:INFO: Client: <request_auth_pass_incorrect> 'OXlWa1RmOWVLVVQ5aEFJaFc=\r\n'
fandango:INFO: Current coverage: 0.21%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.23%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.25%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.27%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.28%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.26%
fandango:INFO: Client: <request_auth_pass_incorrect> 'el8=\r\n'
fandango:INFO: Current coverage: 0.27%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.27%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.29%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.30%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.28%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.28%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 0.34%
fandango:INFO: Server: <response_auth_success> '235 Authentication successful.\r\n'
fandango:INFO: Current coverage: 0.36%
fandango:INFO: Client: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.39%
fandango:INFO: Server: <response_quit> '221 Bye\r\n'
fandango:INFO: Current coverage: 0.41%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.41%
fandango:INFO: Server: <response_setup> '220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\n'
fandango:INFO: Current coverage: 0.41%
fandango:INFO: Client: <request_ehlo> 'EHLO 6A6BVVqDJjFG.pCgMav  \r\n'
fandango:INFO: Current coverage: 0.41%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.41%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.41%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.43%
fandango:INFO: Client: <request_auth_user_incorrect> 'dV9SQTQ5NzA5eA==\r\n'
fandango:INFO: Current coverage: 0.44%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.44%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 0.45%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.45%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.45%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.45%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.45%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.45%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 0.45%
fandango:INFO: Server: <response_auth_success> '235 Authentication successful.\r\n'
fandango:INFO: Current coverage: 0.45%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<kjjdfldcvriuagwc@wukbh.de>\r\n'
fandango:INFO: Current coverage: 0.49%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.52%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<jlucqjwcnodh@ipxhlsjhjmtql.de>\r\n'
fandango:INFO: Current coverage: 0.55%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.57%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.58%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.60%
fandango:INFO: Client -> Server: <mail_data> 'subject: avAmrMYBdsU\r\nfrom: kuqbcgnsoqguityly@fx.de\r\nto: hrpteoklmidajxsp@qvlndtjrirhigesfx.de\r\ndate: Sun, 02 Jan 2011 17:45:50 +0000\r\nx-mailer: MXThfwjoeDRfRITjswH\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\ncg1xQ1I4ZTdN\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:INFO: Client: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: Server: <response_quit> '221 Bye\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.89%
fandango:INFO: Server: <response_setup> '220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: Client: <request_ehlo> 'EHLO 1-O7hlnX6Yt.0  b3kUjx1EACgW  Hx3 OYFQSo0yG1H37a  ZBmSza1N.tp3  \r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_auth_user_incorrect> 'bV8=\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: Client: <request_auth_pass_incorrect> 'aG9FRDNzZU1v\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: Client: <request_auth_user_incorrect> 'ZzU=\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_auth_pass_incorrect> 'aUdVdEI5TlRNdFRyZ05UWXBaeA==\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_auth_pass_incorrect> 'c3FKTWE1\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_auth_pass_incorrect> 'Tg==\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_auth_user_incorrect> 'WDZVdzNyQlNPQVA=\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_auth_pass_incorrect> 'YWd6SEoxVUR3\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_success> '235 Authentication successful.\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_quit> '221 Bye\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_setup> '220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_ehlo> 'EHLO BkUtQMqUPBMeogpo  cAHLHkzFi7yD01Vm-yz -khnq .KiZYmuOqKSdsWaB  cS9MskvDClDoYDaFEP.s 1v2WLpxG OCJ  GK7ge6YCkKx 02Q9ERK4AnVPZQDg-Z  bJByNxAKB9OGz8ds1.mq  Rs5zqwUNlAXlj7rdFo  gTNPmOiW saTm2YTFTWQ  W  \r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.91%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_auth_pass_incorrect> 'eDcxaTJCNGg=\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_auth_pass_incorrect> 'WnlEaE5MVg==\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_success> '235 Authentication successful.\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<obj@qspwxwivf.de>\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<gyoctsmmd@xzvivgvfqgw.de>\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client -> Server: <mail_data> 'subject: _.Flar6:\r\nfrom: gstgdnrd@ujxzhaixfomm.de\r\nto: zobgvkmx@oadhcqsf.de\r\ndate: Sat, 28 May 1983 18:31:38 +0000\r\nx-mailer: HMOVSZsoCwxH\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nbnhVYjFNSU15OWM1QnFwN3Zv\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<fbcwm@gsbgyynepjscdpzjenq.de>\r\n'
fandango:INFO: Current coverage: 0.91%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<aebjcpqsbkymehgqyh@wj.de>\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Client -> Server: <mail_data> 'subject: _u_7pZWFYggOM-koTI32\r\nfrom: ufemikrnpzcdovifexj@jg.de\r\nto: bxah@jbvomvxbcfwdktffpjx.de\r\ndate: Tue, 07 Oct 2025 15:57:06 +0000\r\nx-mailer: xzjvzSUw\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\neFNCU3FBcG1wTA==\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<yvuq@ndgilehikrqqeylstxl.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<ayuhjfttnxumm@jqbfdjqznzvf.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: VKpDH\r\nfrom: orjxtppe@dgzrqzdpklnrmsciaji.de\r\nto: izeirdy@syyobipmmyqsmw.de\r\ndate: Tue, 16 Dec 2031 06:59:20 +0000\r\nx-mailer: RAy\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\ndmwzUkc=\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<wftx@x.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<unslcg@zyknprodgsdenhyexvd.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: YtiX\r\nfrom: ehsnbyvffni@kldxcqkxqjtzki.de\r\nto: dmdeejteukjwumwjs@niphpcvojmjixrugord.de\r\ndate: Wed, 15 Mar 2017 23:44:22 +0000\r\nx-mailer: TIIzzRnqouvR\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nRjdWRg==\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_quit> '221 Bye\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_setup> '220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_ehlo> 'EHLO e7aHhfYtnu2kv -g  7Ax1BCt8ma.vbPwWi0  8dlYh6PYIqX-O.0n2r  \r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'Mk90\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'WXFObUpMZ1FfMVA3M3IyZg==\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'bE5IWkdFMTBiWk5oYzBhSw==\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'a3FwdnN4TU4=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_success> '235 Authentication successful.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<acsbuu@yklidfnxrvvw.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<aonqmvjlm@jplhklrlvtfwzguccql.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: 8ZSRDUcV19\r\nfrom: fsituwtzrfxzbjini@nkpvixdvsu.de\r\nto: pumlwhsw@sw.de\r\ndate: Mon, 08 Nov 2010 00:55:16 +0000\r\nx-mailer: F hIL\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nZ0pKMnpvaHNa\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<gedbgpnqvdweyljap@peguzmoxr.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<lobpierhuetq@f.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: 32eyq3Ai\r\nfrom: pidxgnphqavu@oxs.de\r\nto: qwgkensxxuegony@vylrrnklcvbgwfbtf.de\r\ndate: Sat, 22 Jun 2030 14:57:30 +0000\r\nx-mailer: gcBTzPOiJYPt\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nNDJmak1R\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_quit> '221 Bye\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_setup> '220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_ehlo> 'EHLO efzPDFh4xufeRq1K  052kmhmDmIea 9mZnS9fn9wzZ  uaKZhCS03H 9rhvrZc1OKsxUUNbGZJ6 uyu00FdLdWfNw0Q0  I0XcGq ZnKv2MyT1CB.IeA.ZVPV  r \r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'UUhQOXhI\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_success> '235 Authentication successful.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_quit> '221 Bye\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_setup> '220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_ehlo> 'EHLO D1OhZ BzL2Ldjgq6rEj9-Vb  4wmxJp1apveMlEsMe9rQ  kv ymWgACM5QqkDehnId  qNnE5qPUm.vQlrGDrs WXVu44zEVyeox ktwCQfI4YL z7B dPJT7Wg  q7.RAWO12FM0  89C9jT4wLdUo zah8HbIqg9AR  \r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: Client: <request_auth_pass_incorrect> 'X012dzRqQmtqWkFSZlFX\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'aXB1OGU=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'VXBUVHFoeDJwVDY=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'S3MydHVMVVRnb09PS1ZfblVnX2c=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'dW9oaUlkQ2k0\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'U0VpUWcwaFV0\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_success> '235 Authentication successful.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<loks@agfndhbiilbnyqpxugx.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<g@vpk.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: Zw1WsTcXmqT9ZcakYFd_\r\nfrom: fbasmxraw@xanoi.de\r\nto: zodbnqcqugwgihhdlxf@cbjvilbgzo.de\r\ndate: Thu, 19 Jan 1995 17:47:04 +0000\r\nx-mailer: AFXeNXyF\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\ncQpUUA0=\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_quit> '221 Bye\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_setup> '220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_ehlo> 'EHLO tq6DyNRt  v  kzwOP  MUAJg.LxnfNaGDC A4RWV3Bf t7UugXDlI86  k7s- xPmWsgG  \r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Client: <request_auth_user_incorrect> 'NllUc0xuNEpL\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_success> '235 Authentication successful.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<ifdzzfp@ubg.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<utqx@bzgmxii.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: 7gHt\r\nfrom: icldmeyrf@qjysv.de\r\nto: dkadunx@kcjcotzakxsktbgxui.de\r\ndate: Sat, 19 May 2007 08:16:34 +0000\r\nx-mailer: IXzudPfMzQSAQhdw\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\ncHQ3WVd2a3EzcQ==\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<vwaiuf@rhhts.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<lprafacmxogjl@zegmzgqakovcpqyzzdds.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: QLxADSX\r\nfrom: roiumbjux@dferslqylmllxn.de\r\nto: xrm@ytoipwwmbgtlka.de\r\ndate: Sat, 27 Feb 1999 05:50:05 +0000\r\nx-mailer: GXXkEzlKTLXVrnZuF\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nSEZ3NGVISE9B\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_quit> '221 Bye\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_setup> '220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_ehlo> 'EHLO WSJurm  gENQ  GYlPemzv1eGrapkegX5.  5Hfz2Y6CIzRDWDN8SXV 4Ve2  d-C3q  IW2ybZeeukQY.h  xeft-ek  t-LU.j3XQlhq.RrCC  XtQhfRn4leTkhaf70  E4-cSFQXciSE3axbNZ- 4cPlBhSk6Ei4B8  5SXT0P8qFZvJusGQTHr -vz-FUU7-mt  PrB87xFytEA432cO ystzb65lobWhhd  tBPzIEekqphTeobVD  cRatbq2pSY4TId.00w LgpDZpO \r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'OXNCdg==\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'MXl0QTJzQmlBM0g=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'MWFQWWJVbkhmcXlvZg==\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'dVNDOHNtNnBWQm9q\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_success> '235 Authentication successful.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<wbbmgh@cadplfdbzfb.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<ouhynypyuqz@qcpxqjcffrwinzo.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: TMr\r\nfrom: hnwydcnljzr@vgbkguclzff.de\r\nto: tgtubhqkfodlso@sgunagjbwkwvsjzsrf.de\r\ndate: Fri, 04 Dec 2037 19:34:59 +0000\r\nx-mailer: TtthNU\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\ndTcwVzQycFRWMkg2\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<ofzpqqlhj@roxgtoeyjmo.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<plocohfqmkoxqsvv@wvcivavlclkalohxtztn.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: gW9Rx\r\nfrom: rsgabmg@vdlkxphxbadhndmmww.de\r\nto: nbdpfn@cfpiody.de\r\ndate: Wed, 30 Sep 2015 04:40:04 +0000\r\nx-mailer: woKfvlG\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nOApQVFFNc2VnY2tQSzY2dDBrcw==\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<ncwb@mmkockzmmdzphdmhg.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<ckgwtjwnll@mz.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: sl68m5kcB0mEo RMznk\r\nfrom: bscwfrsv@kltw.de\r\nto: jbk@ozshus.de\r\ndate: Mon, 13 Oct 1975 06:04:56 +0000\r\nx-mailer: oucNlnmtpV\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nU0FRd1hJRm03dk8=\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<cs@r.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<ulqrvczs@odpcveuohwtwyz.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: hUkVn-TNK8K.9VO3f\r\nfrom: qcyoykkakayvbqtrvdal@vnuokefwyiusmwhztcu.de\r\nto: axfdjcmie@byyblds.de\r\ndate: Fri, 30 Jun 2028 13:45:09 +0000\r\nx-mailer: xezCUjKIspvzZ\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nOFcwR2s3WTQNdUNPZWdIeFc=\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<ydetpyxi@nrummm.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<ixjrvhyh@nwiyamaoca.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: qB0BZyCAcMm5yC\r\nfrom: njlpijwrzhxctpzf@nwbadl.de\r\nto: qyowlxazhd@znqvpmbda.de\r\ndate: Sat, 07 Mar 2015 04:13:13 +0000\r\nx-mailer: XsCzNajRfoR\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nUzdBcXI=\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_quit> '221 Bye\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_setup> '220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_ehlo> 'EHLO DW.ux4JY6Ah LtvtUcqfdr Hhlv2URLGg3SKtMF  PI3-fRNMXw  I.y.thq5 NajJ  2LYcl qPbC0q6R9  dFFQlFwEsx4Af54 .8DJoiLixTs \r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: Server: <response_auth_success> '235 Authentication successful.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: Client: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: Server: <response_quit> '221 Bye\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.99%
fandango:INFO: Server: <response_setup> '220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: Client: <request_ehlo> 'EHLO CiBcjEzCIMoa8Od iFsEoOdyaxP BVbo-ucV3ouUSB5-UtI nu5Nx1bMSqRM9rL Bux5.Fh FCe  GE7  4X1Fs7mhgh.yTnYq 7GPGu  rSnQy3gIE71aaD93AAa7 eW D n0B0VHcCh4fXLt-M6RdN  fezlpVG.f9OMjoeM  nYFLU8q9uDV4c  mMMdJXe1.-I2w fXP4owm0  \r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: Client: <request_auth_user_incorrect> 'dHFZMzhnbzlaM0Rf\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: Client: <request_auth_pass_incorrect> 'OWtQQ0tLRWNCZVdsWDNmSA==\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: Client: <request_auth_user_incorrect> 'M19UY2JTeGhOemZUUmlmVg==\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'WXNkR3p6c2RLQzFlT0VNWGw=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'ZUhvdDVTZld5b1M=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'MQ==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'V3NEYU1oZl9F\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'Y1I2ejdNMTI=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'Q1VNVVVnMA==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_success> '235 Authentication successful.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<noojnumhhnybmctxikct@wltqbxrfxjo.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<mshzpxms@sbzjpme.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: F:7pAq hc\r\nfrom: gwzakopju@kjpjrelnsmodjhv.de\r\nto: xottsu@fauookntqw.de\r\ndate: Fri, 22 Feb 2008 01:49:02 +0000\r\nx-mailer: lGvhXZ\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nWjZyWHpjRjANZVFHNGdHMUROY20=\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_quit> '221 Bye\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_setup> '220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_ehlo> 'EHLO 1Ki6j8  TkzSG4M  uUsViEnIVP-oQ  eYnGd0CTX9OGpBVwGPFV 0jo JC5o-22OIxkys5  zeaU06  KDOFbgffPo9clvc megH9Kh4P-niFzJg  TeTAOU j9YvXBMZC4KzSMd i UQsZaixe0vLT  Mo 96 RU  Uwz-XhLkt3fu  a-57O9bq  yMJXz4VyWZVSGz4R TCWUW0Ep  \r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'VHZNdThGb2VPWg==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'OQ==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_success> '235 Authentication successful.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<gts@ktlwab.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<lqladqkuokcofcpr@uesbfezcnycx.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: JzuxnbAEME\r\nfrom: gdeuoroyjvvy@fawymewozcqsxxw.de\r\nto: qqygwgrtxsxp@qwzj.de\r\ndate: Sat, 16 Dec 2023 04:31:13 +0000\r\nx-mailer: tNlpdS\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nT0NWNUlWR0h4U3NZWkxDYW1TdA==\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<uojdu@hgoxdceageakxatddb.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<pzuhfijfabmokvyinffx@ualewbndd.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: PAGC.dqW-lND9Hs\r\nfrom: p@ckmlgu.de\r\nto: rbriogwz@cicdgfzvklobcgka.de\r\ndate: Thu, 05 Apr 2001 06:08:26 +0000\r\nx-mailer: zSN JJWLmG\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nc1U=\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<cniowbahizqcqclfym@cckwktgexyhgxatpx.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<qwufzscjeux@qvdakakpfcu.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: yu0YCC0pdR\r\nfrom: imyetedpda@clqvzzftcyijdnzvp.de\r\nto: jaj@oozqpfzvthd.de\r\ndate: Wed, 02 Nov 2011 08:12:22 +0000\r\nx-mailer: YEyORaQaO IGqJKYnacu\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nVHpVUVEwTmdR\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_quit> '221 Bye\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_setup> '220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_ehlo> 'EHLO G2If1BxOa5Mu2co9E  yH7k4QqCNsQI8r0Ilp  sVl8Hj9Vh9D5V..qlW  UNZhob4txlsJ14KDZm AFLabkN  a83hmbY8j6f6Z  urjaNgymCVOf9PUZy  SMOTYVfxjLZFehs9w  Q0hKygEXHx  SVCMoqND0PV ezzPKgwaaO00 ZCCwJsP5-9wU5cfP  mOvIhH  G0fcQ4U6xQ4p UOgGvLHsAUBgsVqSqEW XkKSZrZD  \r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'X0hQSDBnMndoVVgwUHk3NTF0WQ==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'YVhfOXc0aDZmZlJrRVZfNjE=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'OUdXVW9rV0ZqdTBWa2Q=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'bmZOTHBiM2lyanJqcDY4\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'ZFR4NU80\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'UVJYVUg3ZTNHdDdtaXhLWFF5VXI=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'bkd3NHNveW9pMXo3VkZ0S1p6VA==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'YXEwT3hIYnZZbjVTZ3dlX0s=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'YnlFMnNKNGxBYzhoenVCZXAxbw==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'ZUM4VmczbmhodGlhRjU0QWxw\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'd1dDak5o\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'bUNBek8wOHV6UEFrVUxyTmQwSw==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'WVJxeUNp\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'VWdDQkJC\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'X1hWdzhfZU8=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'enNpck1meHJOdlUxbFFlUThD\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'OEw5MEJEUXNNWTVwd0oz\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'QmM=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'Q1JEeWZZ\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'a2JzRmxIX3QxT2lHMzdQVg==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'UHJxS2RzRA==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_success> '235 Authentication successful.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<rpsuethzwkwwca@pwtfncepeusmio.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<oztmembwebhchjvu@nbz.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: _C\r\nfrom: bkemcprfhmrqiuujm@tndumhlfpishuyxkvslt.de\r\nto: jdnwoyzyanwpkfftuazn@ptilgegeia.de\r\ndate: Mon, 28 Aug 2006 15:26:41 +0000\r\nx-mailer: jISVEwUMrAulUgsC\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nOE1vdHo=\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<jqnoontgmgmmkr@daervfybaxamerkxih.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<rcusoqza@bsdxnfrw.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: p2wH.fZvne d9\r\nfrom: nnbxuukygv@cwillpyukfbur.de\r\nto: saibvxfqqlpiawjhs@sxc.de\r\ndate: Sat, 26 Nov 1994 17:46:09 +0000\r\nx-mailer: gjdcZCYdJBXzWTQf\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\naXhvMEJwNEpjYm14aw==\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<dvpnjfzfaq@eoqvxrxrupzinpoaghzd.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<foobgbpbpofiiuebtkx@zs.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: ZvXv_sutyDPND3GnHcQ\r\nfrom: f@umchgbbt.de\r\nto: vb@magfopjvsk.de\r\ndate: Tue, 14 Oct 2036 15:53:35 +0000\r\nx-mailer: rqRjqHl\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nSWNxTzg2\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_quit> '221 Bye\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_setup> '220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_ehlo> 'EHLO B  8ODU9gye zksRd6QcY6FdpDa uhHfErM  n BlkFdmm24g48  hjLbLR 3A MfTDPZ9IqKdjqqjUM RoOLxIG  YoYUwFQC  IQNkW9  L4O7WVEFN2JvoYVvq  UPzYJ6 .3uqT1jsJEX \r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_success> '235 Authentication successful.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<qrzukcyaksofrqrmordd@bjvmu.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<kasjvyob@mhtmxswwlbtatwwi.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: LQ0DA8epJS\r\nfrom: fyyihahspy@xbsgsugtnrs.de\r\nto: gchsnhqektwtj@menwjdixxtwvm.de\r\ndate: Thu, 18 Jul 2002 21:49:41 +0000\r\nx-mailer: LMtnFvnybmWRXz \r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nWFhtbENLUzVrcVVGblhFckFk\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_quit> '221 Bye\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Full coverage reached, stopping evolution.
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO t3m X7 pGjafpblNq  VrGiYe  ZODy7zu0oOCn  PkxCe8.UuVgxkQDIH  d  ooJ-9WpuX5tRwgl  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nOXlWa1RmOWVLVVQ5aEFJaFc=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nel8=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO 6A6BVVqDJjFG.pCgMav  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndV9SQTQ5NzA5eA==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<kjjdfldcvriuagwc@wukbh.de>\r\n250 Ok\r\nRCPT TO:<jlucqjwcnodh@ipxhlsjhjmtql.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: avAmrMYBdsU\r\nfrom: kuqbcgnsoqguityly@fx.de\r\nto: hrpteoklmidajxsp@qvlndtjrirhigesfx.de\r\ndate: Sun, 02 Jan 2011 17:45:50 +0000\r\nx-mailer: MXThfwjoeDRfRITjswH\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\ncg1xQ1I4ZTdN\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO 1-O7hlnX6Yt.0  b3kUjx1EACgW  Hx3 OYFQSo0yG1H37a  ZBmSza1N.tp3  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nbV8=\r\n334 UGFzc3dvcmQ6\r\naG9FRDNzZU1v\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nZzU=\r\n334 UGFzc3dvcmQ6\r\naUdVdEI5TlRNdFRyZ05UWXBaeA==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nc3FKTWE1\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nTg==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nWDZVdzNyQlNPQVA=\r\n334 UGFzc3dvcmQ6\r\nYWd6SEoxVUR3\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO BkUtQMqUPBMeogpo  cAHLHkzFi7yD01Vm-yz -khnq .KiZYmuOqKSdsWaB  cS9MskvDClDoYDaFEP.s 1v2WLpxG OCJ  GK7ge6YCkKx 02Q9ERK4AnVPZQDg-Z  bJByNxAKB9OGz8ds1.mq  Rs5zqwUNlAXlj7rdFo  gTNPmOiW saTm2YTFTWQ  W  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\neDcxaTJCNGg=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nWnlEaE5MVg==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<obj@qspwxwivf.de>\r\n250 Ok\r\nRCPT TO:<gyoctsmmd@xzvivgvfqgw.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: _.Flar6:\r\nfrom: gstgdnrd@ujxzhaixfomm.de\r\nto: zobgvkmx@oadhcqsf.de\r\ndate: Sat, 28 May 1983 18:31:38 +0000\r\nx-mailer: HMOVSZsoCwxH\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nbnhVYjFNSU15OWM1QnFwN3Zv\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<fbcwm@gsbgyynepjscdpzjenq.de>\r\n250 Ok\r\nRCPT TO:<aebjcpqsbkymehgqyh@wj.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: _u_7pZWFYggOM-koTI32\r\nfrom: ufemikrnpzcdovifexj@jg.de\r\nto: bxah@jbvomvxbcfwdktffpjx.de\r\ndate: Tue, 07 Oct 2025 15:57:06 +0000\r\nx-mailer: xzjvzSUw\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\neFNCU3FBcG1wTA==\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<yvuq@ndgilehikrqqeylstxl.de>\r\n250 Ok\r\nRCPT TO:<ayuhjfttnxumm@jqbfdjqznzvf.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: VKpDH\r\nfrom: orjxtppe@dgzrqzdpklnrmsciaji.de\r\nto: izeirdy@syyobipmmyqsmw.de\r\ndate: Tue, 16 Dec 2031 06:59:20 +0000\r\nx-mailer: RAy\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\ndmwzUkc=\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<wftx@x.de>\r\n250 Ok\r\nRCPT TO:<unslcg@zyknprodgsdenhyexvd.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: YtiX\r\nfrom: ehsnbyvffni@kldxcqkxqjtzki.de\r\nto: dmdeejteukjwumwjs@niphpcvojmjixrugord.de\r\ndate: Wed, 15 Mar 2017 23:44:22 +0000\r\nx-mailer: TIIzzRnqouvR\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nRjdWRg==\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO e7aHhfYtnu2kv -g  7Ax1BCt8ma.vbPwWi0  8dlYh6PYIqX-O.0n2r  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nMk90\r\n334 UGFzc3dvcmQ6\r\nWXFObUpMZ1FfMVA3M3IyZg==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nbE5IWkdFMTBiWk5oYzBhSw==\r\n334 UGFzc3dvcmQ6\r\na3FwdnN4TU4=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<acsbuu@yklidfnxrvvw.de>\r\n250 Ok\r\nRCPT TO:<aonqmvjlm@jplhklrlvtfwzguccql.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: 8ZSRDUcV19\r\nfrom: fsituwtzrfxzbjini@nkpvixdvsu.de\r\nto: pumlwhsw@sw.de\r\ndate: Mon, 08 Nov 2010 00:55:16 +0000\r\nx-mailer: F hIL\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nZ0pKMnpvaHNa\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<gedbgpnqvdweyljap@peguzmoxr.de>\r\n250 Ok\r\nRCPT TO:<lobpierhuetq@f.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: 32eyq3Ai\r\nfrom: pidxgnphqavu@oxs.de\r\nto: qwgkensxxuegony@vylrrnklcvbgwfbtf.de\r\ndate: Sat, 22 Jun 2030 14:57:30 +0000\r\nx-mailer: gcBTzPOiJYPt\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nNDJmak1R\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO efzPDFh4xufeRq1K  052kmhmDmIea 9mZnS9fn9wzZ  uaKZhCS03H 9rhvrZc1OKsxUUNbGZJ6 uyu00FdLdWfNw0Q0  I0XcGq ZnKv2MyT1CB.IeA.ZVPV  r \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nUUhQOXhI\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO D1OhZ BzL2Ldjgq6rEj9-Vb  4wmxJp1apveMlEsMe9rQ  kv ymWgACM5QqkDehnId  qNnE5qPUm.vQlrGDrs WXVu44zEVyeox ktwCQfI4YL z7B dPJT7Wg  q7.RAWO12FM0  89C9jT4wLdUo zah8HbIqg9AR  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nX012dzRqQmtqWkFSZlFX\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\naXB1OGU=\r\n334 UGFzc3dvcmQ6\r\nVXBUVHFoeDJwVDY=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nS3MydHVMVVRnb09PS1ZfblVnX2c=\r\n334 UGFzc3dvcmQ6\r\ndW9oaUlkQ2k0\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nU0VpUWcwaFV0\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<loks@agfndhbiilbnyqpxugx.de>\r\n250 Ok\r\nRCPT TO:<g@vpk.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: Zw1WsTcXmqT9ZcakYFd_\r\nfrom: fbasmxraw@xanoi.de\r\nto: zodbnqcqugwgihhdlxf@cbjvilbgzo.de\r\ndate: Thu, 19 Jan 1995 17:47:04 +0000\r\nx-mailer: AFXeNXyF\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\ncQpUUA0=\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO tq6DyNRt  v  kzwOP  MUAJg.LxnfNaGDC A4RWV3Bf t7UugXDlI86  k7s- xPmWsgG  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nNllUc0xuNEpL\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<ifdzzfp@ubg.de>\r\n250 Ok\r\nRCPT TO:<utqx@bzgmxii.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: 7gHt\r\nfrom: icldmeyrf@qjysv.de\r\nto: dkadunx@kcjcotzakxsktbgxui.de\r\ndate: Sat, 19 May 2007 08:16:34 +0000\r\nx-mailer: IXzudPfMzQSAQhdw\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\ncHQ3WVd2a3EzcQ==\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<vwaiuf@rhhts.de>\r\n250 Ok\r\nRCPT TO:<lprafacmxogjl@zegmzgqakovcpqyzzdds.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: QLxADSX\r\nfrom: roiumbjux@dferslqylmllxn.de\r\nto: xrm@ytoipwwmbgtlka.de\r\ndate: Sat, 27 Feb 1999 05:50:05 +0000\r\nx-mailer: GXXkEzlKTLXVrnZuF\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nSEZ3NGVISE9B\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO WSJurm  gENQ  GYlPemzv1eGrapkegX5.  5Hfz2Y6CIzRDWDN8SXV 4Ve2  d-C3q  IW2ybZeeukQY.h  xeft-ek  t-LU.j3XQlhq.RrCC  XtQhfRn4leTkhaf70  E4-cSFQXciSE3axbNZ- 4cPlBhSk6Ei4B8  5SXT0P8qFZvJusGQTHr -vz-FUU7-mt  PrB87xFytEA432cO ystzb65lobWhhd  tBPzIEekqphTeobVD  cRatbq2pSY4TId.00w LgpDZpO \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nOXNCdg==\r\n334 UGFzc3dvcmQ6\r\nMXl0QTJzQmlBM0g=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nMWFQWWJVbkhmcXlvZg==\r\n334 UGFzc3dvcmQ6\r\ndVNDOHNtNnBWQm9q\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<wbbmgh@cadplfdbzfb.de>\r\n250 Ok\r\nRCPT TO:<ouhynypyuqz@qcpxqjcffrwinzo.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: TMr\r\nfrom: hnwydcnljzr@vgbkguclzff.de\r\nto: tgtubhqkfodlso@sgunagjbwkwvsjzsrf.de\r\ndate: Fri, 04 Dec 2037 19:34:59 +0000\r\nx-mailer: TtthNU\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\ndTcwVzQycFRWMkg2\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<ofzpqqlhj@roxgtoeyjmo.de>\r\n250 Ok\r\nRCPT TO:<plocohfqmkoxqsvv@wvcivavlclkalohxtztn.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: gW9Rx\r\nfrom: rsgabmg@vdlkxphxbadhndmmww.de\r\nto: nbdpfn@cfpiody.de\r\ndate: Wed, 30 Sep 2015 04:40:04 +0000\r\nx-mailer: woKfvlG\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nOApQVFFNc2VnY2tQSzY2dDBrcw==\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<ncwb@mmkockzmmdzphdmhg.de>\r\n250 Ok\r\nRCPT TO:<ckgwtjwnll@mz.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: sl68m5kcB0mEo RMznk\r\nfrom: bscwfrsv@kltw.de\r\nto: jbk@ozshus.de\r\ndate: Mon, 13 Oct 1975 06:04:56 +0000\r\nx-mailer: oucNlnmtpV\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nU0FRd1hJRm03dk8=\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<cs@r.de>\r\n250 Ok\r\nRCPT TO:<ulqrvczs@odpcveuohwtwyz.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: hUkVn-TNK8K.9VO3f\r\nfrom: qcyoykkakayvbqtrvdal@vnuokefwyiusmwhztcu.de\r\nto: axfdjcmie@byyblds.de\r\ndate: Fri, 30 Jun 2028 13:45:09 +0000\r\nx-mailer: xezCUjKIspvzZ\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nOFcwR2s3WTQNdUNPZWdIeFc=\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<ydetpyxi@nrummm.de>\r\n250 Ok\r\nRCPT TO:<ixjrvhyh@nwiyamaoca.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: qB0BZyCAcMm5yC\r\nfrom: njlpijwrzhxctpzf@nwbadl.de\r\nto: qyowlxazhd@znqvpmbda.de\r\ndate: Sat, 07 Mar 2015 04:13:13 +0000\r\nx-mailer: XsCzNajRfoR\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nUzdBcXI=\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO DW.ux4JY6Ah LtvtUcqfdr Hhlv2URLGg3SKtMF  PI3-fRNMXw  I.y.thq5 NajJ  2LYcl qPbC0q6R9  dFFQlFwEsx4Af54 .8DJoiLixTs \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO CiBcjEzCIMoa8Od iFsEoOdyaxP BVbo-ucV3ouUSB5-UtI nu5Nx1bMSqRM9rL Bux5.Fh FCe  GE7  4X1Fs7mhgh.yTnYq 7GPGu  rSnQy3gIE71aaD93AAa7 eW D n0B0VHcCh4fXLt-M6RdN  fezlpVG.f9OMjoeM  nYFLU8q9uDV4c  mMMdJXe1.-I2w fXP4owm0  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndHFZMzhnbzlaM0Rf\r\n334 UGFzc3dvcmQ6\r\nOWtQQ0tLRWNCZVdsWDNmSA==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nM19UY2JTeGhOemZUUmlmVg==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nWXNkR3p6c2RLQzFlT0VNWGw=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nZUhvdDVTZld5b1M=\r\n334 UGFzc3dvcmQ6\r\nMQ==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nV3NEYU1oZl9F\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nY1I2ejdNMTI=\r\n334 UGFzc3dvcmQ6\r\nQ1VNVVVnMA==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<noojnumhhnybmctxikct@wltqbxrfxjo.de>\r\n250 Ok\r\nRCPT TO:<mshzpxms@sbzjpme.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: F:7pAq hc\r\nfrom: gwzakopju@kjpjrelnsmodjhv.de\r\nto: xottsu@fauookntqw.de\r\ndate: Fri, 22 Feb 2008 01:49:02 +0000\r\nx-mailer: lGvhXZ\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nWjZyWHpjRjANZVFHNGdHMUROY20=\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO 1Ki6j8  TkzSG4M  uUsViEnIVP-oQ  eYnGd0CTX9OGpBVwGPFV 0jo JC5o-22OIxkys5  zeaU06  KDOFbgffPo9clvc megH9Kh4P-niFzJg  TeTAOU j9YvXBMZC4KzSMd i UQsZaixe0vLT  Mo 96 RU  Uwz-XhLkt3fu  a-57O9bq  yMJXz4VyWZVSGz4R TCWUW0Ep  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nVHZNdThGb2VPWg==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nOQ==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<gts@ktlwab.de>\r\n250 Ok\r\nRCPT TO:<lqladqkuokcofcpr@uesbfezcnycx.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: JzuxnbAEME\r\nfrom: gdeuoroyjvvy@fawymewozcqsxxw.de\r\nto: qqygwgrtxsxp@qwzj.de\r\ndate: Sat, 16 Dec 2023 04:31:13 +0000\r\nx-mailer: tNlpdS\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nT0NWNUlWR0h4U3NZWkxDYW1TdA==\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<uojdu@hgoxdceageakxatddb.de>\r\n250 Ok\r\nRCPT TO:<pzuhfijfabmokvyinffx@ualewbndd.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: PAGC.dqW-lND9Hs\r\nfrom: p@ckmlgu.de\r\nto: rbriogwz@cicdgfzvklobcgka.de\r\ndate: Thu, 05 Apr 2001 06:08:26 +0000\r\nx-mailer: zSN JJWLmG\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nc1U=\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<cniowbahizqcqclfym@cckwktgexyhgxatpx.de>\r\n250 Ok\r\nRCPT TO:<qwufzscjeux@qvdakakpfcu.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: yu0YCC0pdR\r\nfrom: imyetedpda@clqvzzftcyijdnzvp.de\r\nto: jaj@oozqpfzvthd.de\r\ndate: Wed, 02 Nov 2011 08:12:22 +0000\r\nx-mailer: YEyORaQaO IGqJKYnacu\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nVHpVUVEwTmdR\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO G2If1BxOa5Mu2co9E  yH7k4QqCNsQI8r0Ilp  sVl8Hj9Vh9D5V..qlW  UNZhob4txlsJ14KDZm AFLabkN  a83hmbY8j6f6Z  urjaNgymCVOf9PUZy  SMOTYVfxjLZFehs9w  Q0hKygEXHx  SVCMoqND0PV ezzPKgwaaO00 ZCCwJsP5-9wU5cfP  mOvIhH  G0fcQ4U6xQ4p UOgGvLHsAUBgsVqSqEW XkKSZrZD  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nX0hQSDBnMndoVVgwUHk3NTF0WQ==\r\n334 UGFzc3dvcmQ6\r\nYVhfOXc0aDZmZlJrRVZfNjE=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nOUdXVW9rV0ZqdTBWa2Q=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nbmZOTHBiM2lyanJqcDY4\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nZFR4NU80\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nUVJYVUg3ZTNHdDdtaXhLWFF5VXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nbkd3NHNveW9pMXo3VkZ0S1p6VA==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nYXEwT3hIYnZZbjVTZ3dlX0s=\r\n334 UGFzc3dvcmQ6\r\nYnlFMnNKNGxBYzhoenVCZXAxbw==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nZUM4VmczbmhodGlhRjU0QWxw\r\n334 UGFzc3dvcmQ6\r\nd1dDak5o\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nbUNBek8wOHV6UEFrVUxyTmQwSw==\r\n334 UGFzc3dvcmQ6\r\nWVJxeUNp\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nVWdDQkJC\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nX1hWdzhfZU8=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nenNpck1meHJOdlUxbFFlUThD\r\n334 UGFzc3dvcmQ6\r\nOEw5MEJEUXNNWTVwd0oz\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nQmM=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nQ1JEeWZZ\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\na2JzRmxIX3QxT2lHMzdQVg==\r\n334 UGFzc3dvcmQ6\r\nUHJxS2RzRA==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<rpsuethzwkwwca@pwtfncepeusmio.de>\r\n250 Ok\r\nRCPT TO:<oztmembwebhchjvu@nbz.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: _C\r\nfrom: bkemcprfhmrqiuujm@tndumhlfpishuyxkvslt.de\r\nto: jdnwoyzyanwpkfftuazn@ptilgegeia.de\r\ndate: Mon, 28 Aug 2006 15:26:41 +0000\r\nx-mailer: jISVEwUMrAulUgsC\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nOE1vdHo=\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<jqnoontgmgmmkr@daervfybaxamerkxih.de>\r\n250 Ok\r\nRCPT TO:<rcusoqza@bsdxnfrw.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: p2wH.fZvne d9\r\nfrom: nnbxuukygv@cwillpyukfbur.de\r\nto: saibvxfqqlpiawjhs@sxc.de\r\ndate: Sat, 26 Nov 1994 17:46:09 +0000\r\nx-mailer: gjdcZCYdJBXzWTQf\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\naXhvMEJwNEpjYm14aw==\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<dvpnjfzfaq@eoqvxrxrupzinpoaghzd.de>\r\n250 Ok\r\nRCPT TO:<foobgbpbpofiiuebtkx@zs.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: ZvXv_sutyDPND3GnHcQ\r\nfrom: f@umchgbbt.de\r\nto: vb@magfopjvsk.de\r\ndate: Tue, 14 Oct 2036 15:53:35 +0000\r\nx-mailer: rqRjqHl\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nSWNxTzg2\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO B  8ODU9gye zksRd6QcY6FdpDa uhHfErM  n BlkFdmm24g48  hjLbLR 3A MfTDPZ9IqKdjqqjUM RoOLxIG  YoYUwFQC  IQNkW9  L4O7WVEFN2JvoYVvq  UPzYJ6 .3uqT1jsJEX \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<qrzukcyaksofrqrmordd@bjvmu.de>\r\n250 Ok\r\nRCPT TO:<kasjvyob@mhtmxswwlbtatwwi.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: LQ0DA8epJS\r\nfrom: fyyihahspy@xbsgsugtnrs.de\r\nto: gchsnhqektwtj@menwjdixxtwvm.de\r\ndate: Thu, 18 Jul 2002 21:49:41 +0000\r\nx-mailer: LMtnFvnybmWRXz \r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nWFhtbENLUzVrcVVGblhFckFk\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'

Process finished with exit code 0


Coverage metrics:
Nr trees generated: 15
Nr messages exchanged: 615
Overall time elapsed: 86.03s
