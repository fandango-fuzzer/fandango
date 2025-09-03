/Users/alexander/PycharmProjects/fandango/.venv/bin/python /Users/alexander/PycharmProjects/fandango/evaluation/experiments/smtp/smtp.py 
fandango:WARNING: Symbol <pass_incorrect> defined, but not used
fandango:WARNING: Symbol <unix_time> defined, but not used
fandango:WARNING: Symbol <user_incorrect> defined, but not used
fandango:WARNING: Symbol <mail_contents> defined, but not used
fandango:INFO: ---------- Initializing FANDANGO algorithm ---------- 
fandango:INFO: Generating (additional) initial population (size: 100)...
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Initial population generated in 0.00 seconds
fandango:INFO: Current coverage: 0.00%
fandango:INFO: Server: <response_setup> '220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\n'
fandango:INFO: Current coverage: 0.03%
fandango:INFO: Client: <request_ehlo> 'EHLO .i-yON0rx68tF tLL8YA  \r\n'
fandango:INFO: Current coverage: 0.05%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.11%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.14%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.15%
fandango:INFO: Client: <request_auth_user_incorrect> 'TzFM\r\n'
fandango:INFO: Current coverage: 0.18%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.19%
fandango:INFO: Client: <request_auth_pass_incorrect> 'NFQ1X3F4TzVSZEZVVzU=\r\n'
fandango:INFO: Current coverage: 0.22%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.24%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.26%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.26%
fandango:INFO: Client: <request_auth_user_incorrect> 'VEIweFNjSThRNHVzTk8=\r\n'
fandango:INFO: Current coverage: 0.27%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.27%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 0.29%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.29%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.31%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.30%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.31%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.31%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 0.36%
fandango:INFO: Server: <response_auth_success> '235 Authentication successful.\r\n'
fandango:INFO: Current coverage: 0.38%
fandango:INFO: Client: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.41%
fandango:INFO: Server: <response_quit> '221 Bye\r\n'
fandango:INFO: Current coverage: 0.44%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.44%
fandango:INFO: Server: <response_setup> '220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\n'
fandango:INFO: Current coverage: 0.44%
fandango:INFO: Client: <request_ehlo> 'EHLO sXUpOR6  zcevKGkTJQf9rZKMxJ7 s0A5. yDoQBHIjGTKG0me  z93NdtlQ.JSy6Rl gT0XcS8bSK0.4xgzv 3Apef02dEH7p  4DiROKV1rRP-0 ebbQa1  FqcMckPo  leuWIkOXSVcDxIl  \r\n'
fandango:INFO: Current coverage: 0.44%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.44%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.44%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.45%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.45%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Client: <request_auth_pass_incorrect> 'SE9rUXZGRjFlbg==\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'R0RqTXpNTHlIYQ==\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Client: <request_auth_user_incorrect> 'NWtKQ0E=\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Client: <request_auth_pass_incorrect> 'dV9pRFlvNThDOA==\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Server: <response_auth_success> '235 Authentication successful.\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<gkrcfbpophimmipdt@fpmqrowo.de>\r\n'
fandango:INFO: Current coverage: 0.50%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.52%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<zscpccqra@pgqjajwepvrx.de>\r\n'
fandango:INFO: Current coverage: 0.55%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.58%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.59%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.60%
fandango:INFO: Client -> Server: <mail_data> 'subject: aQuvHfkPSU\r\nfrom: vtrklq@wtlmgjkqpzhlfahsw.de\r\nto: wk@sqptcueyfpudjzgs.de\r\ndate: Mon, 04 Oct 1971 07:39:39 +0000\r\nx-mailer: NdqXtoUtSXfvlcsKbfXQ\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nQTQ4MW9mWGdrSwo=\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: Client: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: Server: <response_quit> '221 Bye\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_setup> '220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_ehlo> 'EHLO bHHUOMz bOj9mk642tj6q77 Au05b1nVovsQymuR9.p a15p  QWvh2x1  jzcUu57peqo0mdE aVUaJvTR4raJA2HwURxb a9q0H7T  L3mSTD  TUJyBjbXl xgaBHw  G  7-SImtN.TWLx3WK5jv  HIG.qBj 0Cv \r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.91%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_auth_user_incorrect> 'Rkp3dGlCeXdpOEd5c0pNXzJldlY=\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_auth_pass_incorrect> 'MUNxZTVBamtFZg==\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'dDM=\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_auth_user_incorrect> 'b2RrZ3ZJMzByNUdqemNfQkgwUlA=\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_auth_user_incorrect> 'WWpJ\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_auth_pass_incorrect> 'T2ZpUXk4TUhHekJGZDk=\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<ecimdfxbd@fjckd.de>\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<ghlybehauxa@kxolslswnvkzikfqww.de>\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client -> Server: <mail_data> 'subject: ib4e gC\r\nfrom: gunqdqrmmncgtyhqm@mq.de\r\nto: pezkgqrim@irasorwwtt.de\r\ndate: Thu, 17 Dec 2037 06:41:07 +0000\r\nx-mailer: UVLJCLn \r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nWDlTRFoxSTlL\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<zzr@nrvkogumytbhpfs.de>\r\n'
fandango:INFO: Current coverage: 0.91%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<vvxqnzcadhmtrhnju@gqapawbsbvq.de>\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Client -> Server: <mail_data> 'subject:  4VqFQarYdVkc4Eoo.\r\nfrom: k@brjeyuopxtevhkiggtm.de\r\nto: rjspmqusqjg@xtxdgcvi.de\r\ndate: Fri, 14 Dec 1990 00:40:33 +0000\r\nx-mailer: SJXRuHrDDAX\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nTDI=\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<fowyjfdhkmgjsm@yhjjpedflwzxcbixyn.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<ogglpovmxnliwcb@rhfyxtlvftxjbkp.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: 9qQA95\r\nfrom: rmwvfcwmah@dyqbuetclvnyqzohuof.de\r\nto: lpmfexen@hcbseabgiho.de\r\ndate: Thu, 03 Mar 1983 15:40:33 +0000\r\nx-mailer: REsOowvPM\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nWEZvc2UyaUw4c3hadlJ6VWk=\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<aelpgrfapnpmzmgq@orwzcixyn.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<fqcxmroapfkqvtv@ti.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject:  yQ:p-.s6F:G\r\nfrom: igeyf@nemdmr.de\r\nto: zlqjjke@mbfnqasojrzzwjtzw.de\r\ndate: Wed, 14 Jul 1976 09:07:49 +0000\r\nx-mailer: rwwxfrmgbGiF xfKYEcS\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nV0FSb3l2QkNi\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO lE6  f9WFKFOuou  1HGQMKHVGB  mQuiYRK JLl.p7 gxTfyd7  K  FbKi0KkzYefGRW  KB-vyc4  X0YgZiOB0STp nQW.egz  vrXTXD4N6Q drXJEtjRqcMHuWDUAJay  mSRD7M6DpEQhDPLec  urL8NIhRPcBiEZwudBg  ejMCV-QO \r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'VmxQ\r\n'
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
fandango:INFO: Client: <request_auth_user_incorrect> 'WUZDTHRtSlh3T3FSeEc=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'cjlaUEJBVVl2NUxiZnk1VA==\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'Mm82R2c1aUJSbEVydkQ=\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'dUdwQjJ0Ymg5MW5SUFYxdm44MQ==\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'QmZsazVSNmZzWDAwTw==\r\n'
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
fandango:INFO: Client: <request_auth_user_incorrect> 'anVHSHFiejNKeFJtSjE=\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO p6b0rAlO5 yVusog 4Hn-57sMhk5FwiybG wRVvo-0x6mb30SHO  dDv 3iI2ah4 8f d-I2S1JiWp3  2ijiHPtU04fYQ0JmfM  ar5j  xR1aDv-AqJ KFVogFvrImRkouNjP  Byd  \r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Client: <request_auth_user_incorrect> 'R0s4UXBrdVZ3ZlR6czhKYnlFMQ==\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<vbkacvyuydt@qruwlif.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<lgctqsjtvvhmwzlfcz@ppcvudnnfeauyjrcyr.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: WTg3xgkG6UJx6tv\r\nfrom: agiooyuwk@xzrrnfngcuelctb.de\r\nto: tysaulriopydrqsb@nlubcy.de\r\ndate: Tue, 25 Dec 1979 03:42:12 +0000\r\nx-mailer: hhxAbPFWqm\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nMGE5TEIKOQ04cHU=\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<togzxlxhtjxoyz@skw.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<amlyxrwwvoeilvnxmd@tbypmtvdaepdlrny.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: 4\r\nfrom: aehjeofiugfvb@mchkjhma.de\r\nto: ytodngfsryox@purszzldbul.de\r\ndate: Sat, 11 Feb 2006 21:24:58 +0000\r\nx-mailer: eJviSZEPo \r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nDQ==\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO gJa8OQE8IK2bEd1riuq- Z8ig7EcLXWqYiF7 xhfK2L.u  yPJ.ape  7oPqqtCxejs  \r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Client: <request_auth_user_incorrect> 'dXBVRFVhaHNNSkZYZVhtWHRq\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'QkFScmgxSHVhUlQ0NWlu\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'M3pE\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'clpiMG84Z25oVm9jd0gwNlpoWEY=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'MWp5Z0JWUTNhazdF\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<zbgrnsrxumgzjjvzrex@snivjs.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<pacctlqx@ieqdtwbe.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: P:LKT\r\nfrom: cypyiy@kedygrtcatjcoymlke.de\r\nto: wshttrs@xoyuawmkpgeznjoyric.de\r\ndate: Thu, 19 Sep 2030 23:34:03 +0000\r\nx-mailer: wqbEKJQtv\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nQldjUXAKTEh0OHhVUm55cQ==\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO kDBCQ7tG6z74m 4BGwZcZoktRt 6aeD  s  3U  \r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: Server: <response_auth_success> '235 Authentication successful.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<rlia@jwablyabshwj.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<pdgidwwhyygkwbqonus@dnzwreskjkasaopnla.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: fVJ4alYQ\r\nfrom: plvkyxyimxszhco@kzafu.de\r\nto: nhvolpneescmcza@hvdebbkwmakmh.de\r\ndate: Sat, 30 Nov 2019 13:19:40 +0000\r\nx-mailer: uNUl\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nYXNWaXBjbQ==\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO d-A0P63W qHNh5 gBXDcwFLsFiAwjK3NP7b  IT7sZChpO47dl  hc ajZmQvDHS  9C  326bxWZ1U398Fzw17  \r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'dFB4dUU=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'SUNZVFdBdUpGZFhXSkNF\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'YnZWSg==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'ckJNdWc0dEkzdjc=\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'aTQyMktwZnhienZyZmVIdTI3UGI=\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'NVE5eVg=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'SE14WDBKT2VsX0VUYzFac1lyVjg=\r\n'
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
fandango:INFO: Client: <request_auth_user_incorrect> 'Q0I3TG4yTVhRcXQ=\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'MGdYUHdmVEZLbkE4Z1U=\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'N09EcEUxcGFES2U=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'cXI1\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'cXFsckRQR3plY3F1\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'b3A5Y2lZ\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'czk5Tm02\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'd3c=\r\n'
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
fandango:INFO: Client: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_quit> '221 Bye\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_setup> '220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_ehlo> 'EHLO ZKEerOewndyyql R  kTXlEt6-dNzLrk  Fs  UyrW4Wdxgek7EXpnH FsjJYXpJsy 3sBQOnGcwlVXx5s2.U 5wJAcH S gr rQ3cP7ps yIiD .x8JXZO-2iL7L  qqDAJKWJqyJ3bbcmrlNq GRD039ZC8SDn7.b9 \r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<reeqlykxkzlnkteglrbh@noqeiv.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<oildcxbelfeowmppufrz@pnkaybk.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: hW3U\r\nfrom: bwtdnmflfgepreq@v.de\r\nto: mwucar@aprmfvx.de\r\ndate: Sat, 16 Nov 2013 06:19:27 +0000\r\nx-mailer: jVGjXLyGO\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\ncVlsakdu\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<fttimahfkct@pyenqwgphwqdud.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<iqdkzxyxzplcg@fvpcomzauow.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: whT_1l-b3eai\r\nfrom: sj@dtiiuizfuelwpsanwvr.de\r\nto: rhhedjy@hoctygonlfkyrrzr.de\r\ndate: Mon, 06 Jun 2016 13:35:14 +0000\r\nx-mailer: iPAeDUX\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\neXhhMUZKVk4yYQ==\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<thqqvyyjsds@hrthmxlhgxfsqoaljckh.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<oa@uvdchocgprw.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: MyWoS\r\nfrom: atmwdwctrhhk@lzyaaavpwwmpizv.de\r\nto: klvy@rtzzet.de\r\ndate: Mon, 15 Feb 2027 09:23:06 +0000\r\nx-mailer: mmvdQTYYKbLGULi\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nRjI1Szd2UmxubU05c2laU01k\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO LrYC 4ftE-Ex v6BLz.WZY1ASm  faQUWEKu-wJ2Q.x mrVEDwYKn3Lda  GLN6D SAkg82GO2 wsO  JrmGp1SENP6b2aOKcj jkdW4p2qVpx.  l1d  O3plK.v96-1xUlf  Jgptscq0d1G6WzkvK Y.D AAo  TMzHNR  \r\n'
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
fandango:INFO: Client: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_quit> '221 Bye\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Full coverage reached, stopping evolution.
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO .i-yON0rx68tF tLL8YA  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nTzFM\r\n334 UGFzc3dvcmQ6\r\nNFQ1X3F4TzVSZEZVVzU=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nVEIweFNjSThRNHVzTk8=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO sXUpOR6  zcevKGkTJQf9rZKMxJ7 s0A5. yDoQBHIjGTKG0me  z93NdtlQ.JSy6Rl gT0XcS8bSK0.4xgzv 3Apef02dEH7p  4DiROKV1rRP-0 ebbQa1  FqcMckPo  leuWIkOXSVcDxIl  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nSE9rUXZGRjFlbg==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nR0RqTXpNTHlIYQ==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nNWtKQ0E=\r\n334 UGFzc3dvcmQ6\r\ndV9pRFlvNThDOA==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<gkrcfbpophimmipdt@fpmqrowo.de>\r\n250 Ok\r\nRCPT TO:<zscpccqra@pgqjajwepvrx.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: aQuvHfkPSU\r\nfrom: vtrklq@wtlmgjkqpzhlfahsw.de\r\nto: wk@sqptcueyfpudjzgs.de\r\ndate: Mon, 04 Oct 1971 07:39:39 +0000\r\nx-mailer: NdqXtoUtSXfvlcsKbfXQ\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nQTQ4MW9mWGdrSwo=\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO bHHUOMz bOj9mk642tj6q77 Au05b1nVovsQymuR9.p a15p  QWvh2x1  jzcUu57peqo0mdE aVUaJvTR4raJA2HwURxb a9q0H7T  L3mSTD  TUJyBjbXl xgaBHw  G  7-SImtN.TWLx3WK5jv  HIG.qBj 0Cv \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nRkp3dGlCeXdpOEd5c0pNXzJldlY=\r\n334 UGFzc3dvcmQ6\r\nMUNxZTVBamtFZg==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndDM=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nb2RrZ3ZJMzByNUdqemNfQkgwUlA=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nWWpJ\r\n334 UGFzc3dvcmQ6\r\nT2ZpUXk4TUhHekJGZDk=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<ecimdfxbd@fjckd.de>\r\n250 Ok\r\nRCPT TO:<ghlybehauxa@kxolslswnvkzikfqww.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: ib4e gC\r\nfrom: gunqdqrmmncgtyhqm@mq.de\r\nto: pezkgqrim@irasorwwtt.de\r\ndate: Thu, 17 Dec 2037 06:41:07 +0000\r\nx-mailer: UVLJCLn \r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nWDlTRFoxSTlL\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<zzr@nrvkogumytbhpfs.de>\r\n250 Ok\r\nRCPT TO:<vvxqnzcadhmtrhnju@gqapawbsbvq.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject:  4VqFQarYdVkc4Eoo.\r\nfrom: k@brjeyuopxtevhkiggtm.de\r\nto: rjspmqusqjg@xtxdgcvi.de\r\ndate: Fri, 14 Dec 1990 00:40:33 +0000\r\nx-mailer: SJXRuHrDDAX\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nTDI=\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<fowyjfdhkmgjsm@yhjjpedflwzxcbixyn.de>\r\n250 Ok\r\nRCPT TO:<ogglpovmxnliwcb@rhfyxtlvftxjbkp.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: 9qQA95\r\nfrom: rmwvfcwmah@dyqbuetclvnyqzohuof.de\r\nto: lpmfexen@hcbseabgiho.de\r\ndate: Thu, 03 Mar 1983 15:40:33 +0000\r\nx-mailer: REsOowvPM\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nWEZvc2UyaUw4c3hadlJ6VWk=\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<aelpgrfapnpmzmgq@orwzcixyn.de>\r\n250 Ok\r\nRCPT TO:<fqcxmroapfkqvtv@ti.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject:  yQ:p-.s6F:G\r\nfrom: igeyf@nemdmr.de\r\nto: zlqjjke@mbfnqasojrzzwjtzw.de\r\ndate: Wed, 14 Jul 1976 09:07:49 +0000\r\nx-mailer: rwwxfrmgbGiF xfKYEcS\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nV0FSb3l2QkNi\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO lE6  f9WFKFOuou  1HGQMKHVGB  mQuiYRK JLl.p7 gxTfyd7  K  FbKi0KkzYefGRW  KB-vyc4  X0YgZiOB0STp nQW.egz  vrXTXD4N6Q drXJEtjRqcMHuWDUAJay  mSRD7M6DpEQhDPLec  urL8NIhRPcBiEZwudBg  ejMCV-QO \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nVmxQ\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nWUZDTHRtSlh3T3FSeEc=\r\n334 UGFzc3dvcmQ6\r\ncjlaUEJBVVl2NUxiZnk1VA==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nMm82R2c1aUJSbEVydkQ=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndUdwQjJ0Ymg5MW5SUFYxdm44MQ==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nQmZsazVSNmZzWDAwTw==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nanVHSHFiejNKeFJtSjE=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO p6b0rAlO5 yVusog 4Hn-57sMhk5FwiybG wRVvo-0x6mb30SHO  dDv 3iI2ah4 8f d-I2S1JiWp3  2ijiHPtU04fYQ0JmfM  ar5j  xR1aDv-AqJ KFVogFvrImRkouNjP  Byd  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nR0s4UXBrdVZ3ZlR6czhKYnlFMQ==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<vbkacvyuydt@qruwlif.de>\r\n250 Ok\r\nRCPT TO:<lgctqsjtvvhmwzlfcz@ppcvudnnfeauyjrcyr.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: WTg3xgkG6UJx6tv\r\nfrom: agiooyuwk@xzrrnfngcuelctb.de\r\nto: tysaulriopydrqsb@nlubcy.de\r\ndate: Tue, 25 Dec 1979 03:42:12 +0000\r\nx-mailer: hhxAbPFWqm\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nMGE5TEIKOQ04cHU=\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<togzxlxhtjxoyz@skw.de>\r\n250 Ok\r\nRCPT TO:<amlyxrwwvoeilvnxmd@tbypmtvdaepdlrny.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: 4\r\nfrom: aehjeofiugfvb@mchkjhma.de\r\nto: ytodngfsryox@purszzldbul.de\r\ndate: Sat, 11 Feb 2006 21:24:58 +0000\r\nx-mailer: eJviSZEPo \r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nDQ==\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO gJa8OQE8IK2bEd1riuq- Z8ig7EcLXWqYiF7 xhfK2L.u  yPJ.ape  7oPqqtCxejs  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndXBVRFVhaHNNSkZYZVhtWHRq\r\n334 UGFzc3dvcmQ6\r\nQkFScmgxSHVhUlQ0NWlu\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nM3pE\r\n334 UGFzc3dvcmQ6\r\nclpiMG84Z25oVm9jd0gwNlpoWEY=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nMWp5Z0JWUTNhazdF\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<zbgrnsrxumgzjjvzrex@snivjs.de>\r\n250 Ok\r\nRCPT TO:<pacctlqx@ieqdtwbe.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: P:LKT\r\nfrom: cypyiy@kedygrtcatjcoymlke.de\r\nto: wshttrs@xoyuawmkpgeznjoyric.de\r\ndate: Thu, 19 Sep 2030 23:34:03 +0000\r\nx-mailer: wqbEKJQtv\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nQldjUXAKTEh0OHhVUm55cQ==\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO kDBCQ7tG6z74m 4BGwZcZoktRt 6aeD  s  3U  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<rlia@jwablyabshwj.de>\r\n250 Ok\r\nRCPT TO:<pdgidwwhyygkwbqonus@dnzwreskjkasaopnla.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: fVJ4alYQ\r\nfrom: plvkyxyimxszhco@kzafu.de\r\nto: nhvolpneescmcza@hvdebbkwmakmh.de\r\ndate: Sat, 30 Nov 2019 13:19:40 +0000\r\nx-mailer: uNUl\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nYXNWaXBjbQ==\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO d-A0P63W qHNh5 gBXDcwFLsFiAwjK3NP7b  IT7sZChpO47dl  hc ajZmQvDHS  9C  326bxWZ1U398Fzw17  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndFB4dUU=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nSUNZVFdBdUpGZFhXSkNF\r\n334 UGFzc3dvcmQ6\r\nYnZWSg==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nckJNdWc0dEkzdjc=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\naTQyMktwZnhienZyZmVIdTI3UGI=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nNVE5eVg=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nSE14WDBKT2VsX0VUYzFac1lyVjg=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nQ0I3TG4yTVhRcXQ=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nMGdYUHdmVEZLbkE4Z1U=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nN09EcEUxcGFES2U=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ncXI1\r\n334 UGFzc3dvcmQ6\r\ncXFsckRQR3plY3F1\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nb3A5Y2lZ\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nczk5Tm02\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nd3c=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO ZKEerOewndyyql R  kTXlEt6-dNzLrk  Fs  UyrW4Wdxgek7EXpnH FsjJYXpJsy 3sBQOnGcwlVXx5s2.U 5wJAcH S gr rQ3cP7ps yIiD .x8JXZO-2iL7L  qqDAJKWJqyJ3bbcmrlNq GRD039ZC8SDn7.b9 \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<reeqlykxkzlnkteglrbh@noqeiv.de>\r\n250 Ok\r\nRCPT TO:<oildcxbelfeowmppufrz@pnkaybk.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: hW3U\r\nfrom: bwtdnmflfgepreq@v.de\r\nto: mwucar@aprmfvx.de\r\ndate: Sat, 16 Nov 2013 06:19:27 +0000\r\nx-mailer: jVGjXLyGO\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\ncVlsakdu\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<fttimahfkct@pyenqwgphwqdud.de>\r\n250 Ok\r\nRCPT TO:<iqdkzxyxzplcg@fvpcomzauow.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: whT_1l-b3eai\r\nfrom: sj@dtiiuizfuelwpsanwvr.de\r\nto: rhhedjy@hoctygonlfkyrrzr.de\r\ndate: Mon, 06 Jun 2016 13:35:14 +0000\r\nx-mailer: iPAeDUX\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\neXhhMUZKVk4yYQ==\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<thqqvyyjsds@hrthmxlhgxfsqoaljckh.de>\r\n250 Ok\r\nRCPT TO:<oa@uvdchocgprw.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: MyWoS\r\nfrom: atmwdwctrhhk@lzyaaavpwwmpizv.de\r\nto: klvy@rtzzet.de\r\ndate: Mon, 15 Feb 2027 09:23:06 +0000\r\nx-mailer: mmvdQTYYKbLGULi\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nRjI1Szd2UmxubU05c2laU01k\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO LrYC 4ftE-Ex v6BLz.WZY1ASm  faQUWEKu-wJ2Q.x mrVEDwYKn3Lda  GLN6D SAkg82GO2 wsO  JrmGp1SENP6b2aOKcj jkdW4p2qVpx.  l1d  O3plK.v96-1xUlf  Jgptscq0d1G6WzkvK Y.D AAo  TMzHNR  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'

Process finished with exit code 0


Coverage metrics:
Nr trees generated: 11
Nr messages exchanged: 409
Overall time elapsed: 48.11s
