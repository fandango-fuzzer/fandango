/Users/alexander/PycharmProjects/fandango/.venv/bin/python /Users/alexander/PycharmProjects/fandango/evaluation/experiments/smtp/smtp.py 
fandango:WARNING: Symbol <pass_incorrect> defined, but not used
fandango:WARNING: Symbol <mail_contents> defined, but not used
fandango:WARNING: Symbol <unix_time> defined, but not used
fandango:WARNING: Symbol <user_incorrect> defined, but not used
fandango:INFO: ---------- Initializing FANDANGO algorithm ---------- 
fandango:INFO: Generating (additional) initial population (size: 100)...
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Initial population generated in 0.00 seconds
fandango:INFO: Current coverage: 0.00%
fandango:INFO: Server: <response_setup> '220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\n'
fandango:INFO: Current coverage: 0.03%
fandango:INFO: Client: <request_ehlo> 'EHLO Qgf6IEIQ IiQBY5ezM8N4.Gnu CVpV5L  2di7pUfcKLqy-IxcP  u0Mw8T  UuL AghWBA7Xkx  GaaWcfl ZV79NWCkPBcd -ocl6jt  scv YR8Z4ETP  ZBClY7eWyJt2  \r\n'
fandango:INFO: Current coverage: 0.05%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.11%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.14%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.15%
fandango:INFO: Client: <request_auth_user_incorrect> 'a2hLV2ZiMVV0VzBBUw==\r\n'
fandango:INFO: Current coverage: 0.18%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.19%
fandango:INFO: Client: <request_auth_pass_incorrect> 'Wm9wRk0xUDdHaW0=\r\n'
fandango:INFO: Current coverage: 0.22%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.24%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.27%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.26%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.29%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.28%
fandango:INFO: Client: <request_auth_pass_incorrect> 'NnVLN3RpbzdUZmEzNTV3RnE1Xzg=\r\n'
fandango:INFO: Current coverage: 0.29%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.29%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.31%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.30%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.30%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.30%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 0.36%
fandango:INFO: Server: <response_auth_success> '235 Authentication successful.\r\n'
fandango:INFO: Current coverage: 0.38%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<fjmunekgwsq@kkmzrandocxzuxxwunf.de>\r\n'
fandango:INFO: Current coverage: 0.43%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<jabgttaxsnou@tljluuwduudtmnpw.de>\r\n'
fandango:INFO: Current coverage: 0.48%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.51%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.52%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.54%
fandango:INFO: Client -> Server: <mail_data> 'subject: Lbn\r\nfrom: kexyrabxhixxoohvv@ppzdzddt.de\r\nto: prp@yzsbibvscvi.de\r\ndate: Thu, 25 Jun 1987 13:56:28 +0000\r\nx-mailer: SxLndNl\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nTmpxUEF5ZlhKalBmVFVVUwpyDUo=\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.81%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<xjnyxyvikmvc@lkidwgytjkzgvtiahtr.de>\r\n'
fandango:INFO: Current coverage: 0.83%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.83%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<tsugprtvyzkrnecbgld@zcznbnhc.de>\r\n'
fandango:INFO: Current coverage: 0.84%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.86%
fandango:INFO: Client -> Server: <mail_data> 'subject: IuuQW7ts\r\nfrom: x@qdxorcucyirndcukv.de\r\nto: xlmgbnvxg@zwjoottbtdkyp.de\r\ndate: Mon, 15 Feb 2021 15:05:00 +0000\r\nx-mailer: eprFfplphNeE\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nClBD\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.86%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<g@vlubij.de>\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<trl@xwivabz.de>\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:INFO: Client -> Server: <mail_data> 'subject: 5s20tW3jD\r\nfrom: xuyouhwsugnujbmduwq@npdhp.de\r\nto: cakbhpkaxnxjeblrpc@tdufqgizfxez.de\r\ndate: Tue, 15 Dec 1998 19:41:00 +0000\r\nx-mailer: exOYRunUZBfJOPLX\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nRzlj\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.87%
fandango:INFO: Client: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: Server: <response_quit> '221 Bye\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.92%
fandango:INFO: Server: <response_setup> '220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:INFO: Client: <request_ehlo> 'EHLO sgwl54Q1Md-  ZxLKYyXTL-UhYt  eka  0zIiHhyKS7yMzUR9Gdb e2BAnf  nC  nwzWWecDazHPK8  -6ekTrIffX8B 9kKD7c F2u  6Wsco PNK8n0X2vLn 5Cl8ESh YzHkyi6M7ZJI S77pBatCoyngFiS.QQ6  jiA1OVAKvDhUuebNGm83  RZaHLhOmX  MVqevYn xOH  \r\n'
fandango:INFO: Current coverage: 0.92%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Client: <request_auth_pass_incorrect> 'czBJc1VEYXB0TmhiS0RuWnQ=\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:INFO: Client: <request_auth_user_incorrect> 'VDluTTBTNg==\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: Client: <request_auth_pass_incorrect> 'UHp0VzVkdDNwcU8=\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: Client: <request_auth_pass_incorrect> 'WjhhUkFsb3ZoSVFKZGdvWVRQR0Q=\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: Client: <request_auth_pass_incorrect> 'SnNRdWRfbjBWUnR0Rmc=\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: Client: <request_auth_user_incorrect> 'MExoVGd2Qko=\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: Client: <request_auth_pass_incorrect> 'c0Q1dXlWeThTY01IcWdEM2NH\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: Client: <request_auth_user_incorrect> 'YWg5bVRWMEhlN05Zaw==\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Client: <request_auth_pass_incorrect> 'T1FLSzF5QUJJRDFuZGth\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Client: <request_auth_pass_incorrect> 'ZTdRWThPcjZQVU9kMkU=\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Server: <response_auth_success> '235 Authentication successful.\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<jdbxrqhpv@lvygyfwlqkdwdzxxv.de>\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<wbfwzks@mkoiapq.de>\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Client -> Server: <mail_data> 'subject: .49KhWeQA CbH\r\nfrom: ucctpwrqcnbfpdf@fud.de\r\nto: pxqflxqbubepzdsil@pslalzwfp.de\r\ndate: Tue, 09 Apr 1991 01:28:57 +0000\r\nx-mailer: oi \r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nME44VFpkbFFGRDZWZWw=\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Client: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Server: <response_quit> '221 Bye\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Server: <response_setup> '220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Client: <request_ehlo> 'EHLO o  o.Ip  0dg1HRbRqhR3kU  .acdvLEw8Z9ulF.L1n2  JXsw  G67Iw7Ez ZOjUmaaC7m isnppX.wvZdkGT  QAYqpdD4n-mbuaPM EFJ3mPMkA1MaoACICI  HPOAsC4RtX5Txu  jrzVHK  D5yJfPD  Qhn0pr50.aEPWSEOs.M  bq mFn7UYbja.QWmA3 40iIo7  FYb1  \r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: Client: <request_auth_user_incorrect> 'YWtuNW5FQnk=\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: Client: <request_auth_pass_incorrect> 'QW1OazFsY2N3ag==\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: Client: <request_auth_pass_incorrect> 'a0NPNFluck11U3UxMg==\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: Client: <request_auth_user_incorrect> 'Q2NIYjlTbkFNU0ludndlWg==\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: Server: <response_auth_success> '235 Authentication successful.\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: Client: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_quit> '221 Bye\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_setup> '220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_ehlo> 'EHLO egRK9VBp35  EtGimFvdfaaSxNi5Hg-Q HpD1zBBuhGiPF h.Ku2moevnEdbXXnxT w8QWbZBKPjT4  c5  pP5A  CkA6ZZMY7loDPTjpkaUe  -BXOxX  X7HeNbmg7Kl0R14S  p1MLuvj -4F.FB9lJ17fPrx  79 yBD3eI2.7805SAAh  ZxssbWZyt07G2Q2 -BbcGR0.i8yn5c2Sdz  TDWJ 9u4W9G3Rpca9m  ZyWfl6zBl4JQP8Rgz URGD-J \r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'TEtfQ1p2Zkc4MExqV1lCbzA=\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'UUg0eQ==\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'MTZNM0EyNVB1QVk5UXUySTN5SQ==\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'aUtyS0g1N0ZycUI0R2I=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'Ykxpd0pwVDQ=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'NVZPVw==\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'aVZhcjZC\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO TcT.RjONQX 0YxYyNFjWaIES  oBaU3J0RpCQdlnomXM  wiEcQFiZDwWWWbQjiB  QKHyzeIUhz0WLyy3MF  JWB2qbFhy0MlWNGsF b483jGjBezNl  yZ2HGQq8s7  \r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Client: <request_auth_user_incorrect> 'NWtqODFDT1ZnbG5HOA==\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'Y2djY2s1YTEwN1Yybw==\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'ZmpnUGVl\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<jdyyvkllgahrsihkwgyk@hulninfsordfasoszv.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<rbbjcl@hwdevyc.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: -28ptESJXZJuQEX0T\r\nfrom: ufttfzhalzxextdg@oc.de\r\nto: ljorvtoy@tzifsmdzy.de\r\ndate: Tue, 31 May 2033 06:40:24 +0000\r\nx-mailer: lhRJiKEJ\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nVm9HZFF5bktEbmdnbw==\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<deejkiqnq@y.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<tqaefrcd@lqnbafxwizxjrbujm.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: sZ4VmNWKcJ\r\nfrom: oqayisyhoqczx@u.de\r\nto: rhepe@xmikm.de\r\ndate: Fri, 11 May 2035 17:09:05 +0000\r\nx-mailer: x\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\ncE8wMzBNazBQY09h\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<abyksdll@tslw.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<faikfiwymadnhrq@hggjynoxgjeeqhvctf.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: LYQ_MwG\r\nfrom: qoifqbexs@jywweuvr.de\r\nto: gmcmojfefddjbff@cgkd.de\r\ndate: Thu, 22 Sep 2016 08:02:57 +0000\r\nx-mailer: MZsAKwngUYTGg\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nNDE3U0hrU1ZyNFZjNTlSaXhXYng=\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<pkhbjtqxseaghx@bbqzovwnynzufat.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<fueipdl@wmyjjnfinodnvx.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: -T-a09\r\nfrom: oqbkvvegwiwdppgd@raodirksiwwzwftx.de\r\nto: rncjsff@wumtvbdtepteupmm.de\r\ndate: Fri, 10 May 1985 10:08:54 +0000\r\nx-mailer: a\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nYnpiVVFv\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<bzndif@ei.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<mxeolbubjnkbktaddv@j.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: DazRoSYI\r\nfrom: bk@pocakwahledftmowttq.de\r\nto: sxlrreglmknlfd@jn.de\r\ndate: Sun, 26 Sep 2010 06:58:45 +0000\r\nx-mailer: ziZxSGlDYxFPU\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nN2NNNmQ0VUx3eXE=\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<qtzlpgtownmwxznntck@vwovifjofozlednb.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<hfvmgd@h.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: YNRJJqmD0s57fbg3X\r\nfrom: hwqdpniwpk@ovdqwj.de\r\nto: njdocairqtkb@sblkkzswvga.de\r\ndate: Thu, 15 Dec 1977 14:24:40 +0000\r\nx-mailer: whaAxKJPkyeIO P\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nN2FX\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO i0w F0vglowh  r  oiXl2orYzOTkop0  F7 axw  U  34H6 wtajuW  naO7eq-A61UsUTWv57zc f-jruJE  Fz9AA-3d0 g  \r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: Client: <request_auth_pass_incorrect> 'TmlUbg==\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'Vk5OTjV5UzFxUXNuN0tOMUM5dA==\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'M2pLRWZoZ0pRMlJwbEJTTGI=\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'T0tNMHpiZFd2T3JlSFIybTQ=\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'T3ltOVRlUDBPWXBVVFkxWkkwdTQ=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'aW5wbGVMOVJOQXBJZ1AySmtY\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'Y0ZmMHVIZEo4VGV0a0ljSkt1OXo=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'SEdVaFBY\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'Q21HTk5FV1VDZUo=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'VUQ0WFpaSmZDVV8=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'aFZSTklvN2l5aHhXNW5RR3ZU\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'Mk5sOEth\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<xgzlhwr@rsfxzqvnzdxq.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<t@osikdbidbbcte.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: 3KYPbgqlq\r\nfrom: kjo@sklw.de\r\nto: rmnxechfqijlc@e.de\r\ndate: Sat, 24 Aug 1991 22:14:26 +0000\r\nx-mailer: oyZkPCjWNgCnFEiVhWf\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nZ0h1a0VVWmNT\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<hmkosebqncnz@epqh.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<pyuoljpdkapwzkioptt@yfuauiusocjqvhdiry.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: Lf_1OQXf1pv6vB5XDVX\r\nfrom: e@j.de\r\nto: oqcwcpsg@whbbemsi.de\r\ndate: Fri, 25 Aug 2023 10:00:30 +0000\r\nx-mailer: pupo\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nZTd5RFBzQjFSeUVhd1Bh\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO -Lyk  sH8pM.bv8XJ-  mgp7o4-tPYYnQ4dH ntTP  X2rgW  \r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'NQ==\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'cW1xRzVFeDQ0RFBiTWdXQkY=\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'MFE4VnFBWXRIUVJKOQ==\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'b1gwUThpc2VMZVZmb0c=\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'YjJXb3ZfYWxDM2g=\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO txR.2k2i8mwFIEG3 0T-ScXUZ1MIol UjgLEqEB3haZez7oBNb p6 w2RdP  eiSPh1GkmXATdFD  G3T  HfgJ3eYIsvya9s-  hFwGao.iTrBnF2V0 hu687Eta  VABJ03KBl aAkj qpdsCktV.n6mNOyAk 1QRfLi.7 mw3vpnY.M  d65YoxiaMr  pJOpcI3fm7y3Do8f \r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: Server: <response_auth_success> '235 Authentication successful.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: Client: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_quit> '221 Bye\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_setup> '220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_ehlo> 'EHLO 0  Wt0BlBqvEJW4uhkE 1 FL2C0Xo5WnrVjLrKD WcO miKP dqvmCMztBAwkgH68rM  f6S7wMPu-fx2enhJt.  B  gr.c1QzKP7ks1tHJ5 4wYQ4eY7PV7xy7K  rCra8JDo1LWi4F7Q-  GNI-E  kjBAICifJ6y6wvnP5 jIuMPhVyPTX9N4PZMRCA uJ9YdNgANRJfpmliYa oChnM..EwkR2Z  eZmOrkcnEE ALbGBn6vtDrWC3B1  -oip06ZTFcckqA  \r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'VDVtUThPOWc1TDdseGpEd3VC\r\n'
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
fandango:INFO: Client: <request_auth_user_incorrect> 'dw==\r\n'
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
fandango:INFO: Client: <request_auth_user_incorrect> 'YVR3a3owd1FNbm4=\r\n'
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
fandango:INFO: Client: <request_auth_user_incorrect> 'c1NtOWFuNg==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'enp4NF9VSTFkcERWUQ==\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO Q36M5GbWkyt  IyJcLwj-aKDgqXqKK  ahx-jEaByomnimTfVHN 2224Crj3xHS9bBVyZyEg  Va276ai  dodTr  xQP0QB7K6WFdiqDhnS b3ngWPP  n8VePahlGqeulJYf4jl NJhDiWpbM0bhEKSyWC-3 gzpyorgkNGlxib4foJlf  L73NcUPSHOTNScpavKT MBS5wR.eL f.LYm2  KQD.nNsk bjesD95TWQiJ3XC  K.lD7UYVKyH2  bTRs4pTuuu 61S  nQpFn \r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'anp3UV9jMDczT19ITkpuaHFrWFg=\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'WkZGdnk=\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'a1R3OUI=\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO o952BD-g-SM  bzfxEusu4QHkbUrGK6QP QFzG9OqYpNFW5NOYWTvA  7wPOjezDcr8HFc1WD  uk8qiB3YeZ3TSuNCMe8  TsQlrnqv.  b0dkwaYaSeWO G BqV9 AwW4Xze1KV7OruOCOY 6HLaXM q-qzwUPsq aP 8vwHKcFdl J  e  SIAQ5A3O23eRdKJ \r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'QUlBUEg1MQ==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'aWp0SkQxc3pxVXVqaWh0Rmk=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'TFU1dTU=\r\n'
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
fandango:INFO: Client: <request_auth_user_incorrect> 'QklGZFM3UXNwUXBFUzYzdEY=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'c2RNNjhBZFV2c1o5Rg==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'bTF4YzYwcEVXUm1zREV5ZVI=\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<kyezkqefrutxqs@egbyvghfuhrussiavzuo.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<h@kjivcxjpbixuay.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: ZAvag3Ra\r\nfrom: kzrnchscbyfdg@qjzcsbftci.de\r\nto: itlinbm@fgjoypiwgrvezcu.de\r\ndate: Thu, 28 Jan 1993 15:25:59 +0000\r\nx-mailer: tgKOGIdGEoKNEMjfywkp\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nRlVs\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<cxmaur@jwsiziqh.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<dlbchkkopbaskihpvd@zs.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: RjELlWvLFCeb\r\nfrom: eastgigzwgjzq@cdkpzzgjdvrpsaussyu.de\r\nto: kugyuntqxzu@usxwznarlxrmoogmxzgy.de\r\ndate: Wed, 13 Jan 1999 01:30:19 +0000\r\nx-mailer: iu\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nSGJmRnFtaWFK\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO kpSKZE.W5bhxHre rNtk7 loOBygsPo Xp3P  UX6LgWg7wnPejoY 3KG0-nL4  gAdw-Mwqct.OQ- yWDaiDgqfR.5Yq  SrNdbjVwmCSg BJ44HRNrTEsZddjaN VZgsEmj1cHW  HFQnVA2oARaC  GJC \r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'dlNfNWpnZnNr\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'bnNPd3dMc2syVHpt\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<xhzrk@evekjqwnkpsixgfgnaml.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<ayhsdbwnwbjb@hvjqxrnr.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: HuNsKLuCC:xuMBTvW\r\nfrom: ryggkoodni@ydngdarfjwljxlgtfaj.de\r\nto: uhbexdaglukttzsyho@gtdjz.de\r\ndate: Tue, 05 Jul 2022 03:02:59 +0000\r\nx-mailer: zQtLEyy\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nCms1WXBzdWJhemV5Qk5m\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<vttleljmsure@wnxivafbfrgk.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<xriznibh@rv.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: 4C6B2\r\nfrom: lism@hicuyjwwwt.de\r\nto: pzoxfy@hhpvfsngvadyabsd.de\r\ndate: Thu, 30 Sep 1971 23:00:43 +0000\r\nx-mailer: qZYakMj fur\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\ndTk0V0U=\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<zmfxjobcbaje@vlmxkosbnx.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<eyvfwq@nwohyhiowbap.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: ad:omVbbwzflA4 L0tg\r\nfrom: oupsfkuar@n.de\r\nto: xxyvkgtbysia@neaoigvqu.de\r\ndate: Sun, 01 Feb 2032 01:12:24 +0000\r\nx-mailer: uRY\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nQw==\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<hsmyw@qwhzrtejs.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<w@lgfvh.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject:  n9dTFy\r\nfrom: bygzhwpfqemjdypffi@z.de\r\nto: itbulvakbd@hrvlpgxkijtvv.de\r\ndate: Sun, 05 Oct 2003 05:25:05 +0000\r\nx-mailer: XXFpkBSMM PcuSmFvOU\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nb1ZBYW9kMFVpTApwT0hDcEFVZg==\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<jzxxxxqdybkieal@arpacdtnaihameywj.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<jez@egrjxu.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: vt_uu5A\r\nfrom: ypjt@kwnfhqials.de\r\nto: niuclkywcjqsaundjyf@tgpardbcxb.de\r\ndate: Thu, 09 Jun 2033 01:54:01 +0000\r\nx-mailer: GCgUCwZfJcJMbZuA\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nc2N2MTRSU25aNHA4aXRNWA==\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<nznceqzz@xad.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<dul@dpvjusnan.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: 7n0cshcB4cI0YTkimaHJ\r\nfrom: youetbmsp@pzzzicxxewhddi.de\r\nto: f@xujutsmmnklsknkkc.de\r\ndate: Thu, 30 Mar 1995 22:25:53 +0000\r\nx-mailer: FmmtAMZSLbtSUrgnib\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\na3BNRUxUdm9YaWhEMgo3UnFxMzI=\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO lu 0QMB7gJ0CpXS U4oSEmVjHiMqz  tn-UDk2-wN XTO6qlWsR1cJU3o-Dhc 2h7KyvCQDkXtpfV  1zZ31epA7  p.Uzkfik-tx54PzGOESJ o9TnWIfmo3yBS5  \r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'RTJnNDlLS0x5VE1ka2M=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'X1hKcTl6cEMz\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'S2hvZDJFRzc4ajg1\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'Mw==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'RzVYMko4WWw3Y2w=\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'aXl6WHdleHZwRFJF\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<amnjdqrcyq@avhqrdhcpofoiesndaqe.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<chrum@hjvhkf.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: 3TH_-IbyQ:CE1oG9D3i\r\nfrom: dgcbofvhqgsbasqbt@ndysuyryjaartnpr.de\r\nto: muoeaupgxht@ouowcqj.de\r\ndate: Thu, 22 Dec 1977 01:32:17 +0000\r\nx-mailer: AdmOltPdQUA\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nNmM1Vll1ekxHOGZpTjJRS0M=\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO akZ79ITN-VLMWOUh8x \r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'Zw==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'Tm9GZlpUdmNlUDM=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'MVAzZEdCeDdjUF9qZkcw\r\n'
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
fandango:INFO: Client: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_quit> '221 Bye\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_setup> '220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_ehlo> 'EHLO xZROshme  \r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'YmRvN3c=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'QW9iSA==\r\n'
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
fandango:INFO: Client: <request_auth_user_incorrect> 'NjZEcw==\r\n'
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
fandango:INFO: Client: <request_auth_user_incorrect> 'bDdIanBUOQ==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'dTA=\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<eknwwlqitrnbapsqbtf@dis.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<amazbjfnxolfvsv@kqbenoehfltnqilq.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: Xi\r\nfrom: hbschn@wkjxnukysavuqmnasct.de\r\nto: bznd@y.de\r\ndate: Thu, 13 Feb 1992 03:00:56 +0000\r\nx-mailer: swCUBMLjCnqKHThe NCC\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nbk81OFppSGcN\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<ajqbayjyxkvtminfkyy@vdmjsezicxmg.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<uhju@wkmtogwenuunggmgsw.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: xk4_ ubja6YF2Tbq\r\nfrom: zqqgrn@guiwvxakayynbsjon.de\r\nto: cmiovfxj@frlbcbhxhoykbdc.de\r\ndate: Mon, 07 Jul 2003 11:12:21 +0000\r\nx-mailer: AddqkazUAsY\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nRGRqeWVKcm5TTg==\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<ocokxltbfucwoatvy@r.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<jrog@uslqfarrb.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: -wIdphS2AKm10m41WU\r\nfrom: ebdtwgxbdcadmy@lejtcpqxszhkucdypf.de\r\nto: fgubvbfzeigllmy@fdcfsszti.de\r\ndate: Sun, 08 Sep 1985 06:32:08 +0000\r\nx-mailer: ajRDCcqWKKfTUZnQ\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nQU9SVWhGZEMKOHRjcTFESFM5QVc=\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<yvffsdvvkpcvuxxg@tavfj.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<p@xvwwuhbw.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: 5k-:60g A5D\r\nfrom: rpdfcjoyym@fzaczw.de\r\nto: bvejwklvsr@x.de\r\ndate: Sat, 09 Oct 1999 22:48:11 +0000\r\nx-mailer: xdgIBzyEadrtTE\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nMVhvN1VsOGVxVTJWaGsyYg==\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<mqdtzrnaexqoybm@flbhxstnvtl.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<cltbi@rvla.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: m\r\nfrom: evifwsbauvzwoffdxc@hwqkhifpdpxskdkyx.de\r\nto: dy@aewcxdxjhqfjb.de\r\ndate: Mon, 30 Jan 2012 11:48:48 +0000\r\nx-mailer: zPQIkKYZESOoMgTQJN\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nZG9vYUhiQVdmQzFH\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<dbdgooqcngvgiarzpet@etgaimj.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<disivrih@wkdjdvqcwcw.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: c -dVCPyW\r\nfrom: vdb@wcj.de\r\nto: tdcjusmuxy@aqkg.de\r\ndate: Mon, 25 Oct 2010 21:00:13 +0000\r\nx-mailer: EYlActqPYY\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nSWFsa3V3cQo1bXB4WkR2RDA=\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO 1AdA08ZWZh 2 Txhx9  A712N7Sy7LiMc  Bjyt3Yvh3  41-oodqIF.Rgr  eRe5Mzy  cDR0FSTKN.I scDu3hOuFYwqBR6fz 9gvDxWcGeOg2vlEm \r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'ZnYyY3g=\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<maypcrlctyemuoqduvg@wnikptmtckzqdn.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<viotghwqogb@sclcpewzegswllwlodh.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: B5q-jE:a1\r\nfrom: oeevcvv@itoint.de\r\nto: xqzeixl@gkqulsb.de\r\ndate: Wed, 14 Apr 1982 06:26:11 +0000\r\nx-mailer: xJjItBetAcIGl\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nQnVKCg==\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO zpe5RCHBfF yb-nO59NPv jauyaV0JJqtV ul 8  RZSc1FUOz1lj9vI nLsw8rB ywaFacN-rv0vm0D7AK  \r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'Xw==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'VF9nMkJiRU5TWU5KSHpi\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'NVlheGZTdzBCZjgwX3o=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'RUJXVlBn\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO W -gpmk v5UQ2D2WvL  .tQjIk06G4t5iN.2U OUSUlkVl2  UXT  \r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'cTFJSWgybm52YXhUcQ==\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'WXhleHo2WVBsN2k=\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<skxxcedbnlqdvbwlin@fh.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<lsmdaiuvewmbflhbpyy@zectzstoo.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: ViEtRCkW.kR42vf6fwlu\r\nfrom: wdrmbqhq@nk.de\r\nto: bbkl@iwmucpvsjwloygjoa.de\r\ndate: Fri, 18 Apr 2003 15:50:58 +0000\r\nx-mailer: fiVRUqbpHzSzHLvnIlA\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nUlo=\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO bqLZpt1pd8 .TlyS5QgbYKV6  H-FSmi-Yv  LoX 7ljbMk3mCua6IlQsKVX avlM  bpyDPCjb  i0g1tKz8  .UnqURWlZ2WB7fZcFH I1 ODySlk  7srovkonqUjIAt Qxrhx fn6  ntuG  iO3vsxictnL1vZN07eUw  \r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'Z0UxelpRcnl1TkNtdg==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'c0NkU05lWUw=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'azVoOA==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'OHNUNHFDdm0zNTE3Tktn\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'WnBvNmZoTzha\r\n'
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
fandango:INFO: Client: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_quit> '221 Bye\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_setup> '220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_ehlo> 'EHLO pMwPfqhga Vx EfQvX210J  4IlD awrogzQcrnGzSxEwG8t -etz  sUL H--Y-9qpL1xEUek8  n yBfrT1a-4P6  yjX.8XGDHoTzX6 dqwk5GpXyblfwS phl5eP4 YMyYBrkbuFt L-sb pdMXpsi4Am.KUZtOi6u  \r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'STNSdEo4cmpTQmZhb0hKMDN1OWM=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'bHh3VExqUlVGZjVvMkdVMDVCNQ==\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'd3JieEN3cEUwNWExbGRK\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'X2VhYlZ2Rw==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'cE45bThSdFQ=\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO SimJnlQxHJPB.XIDi  H856J0EtUM-BDRSfZB7 Ix7UqDeiEF5pe2y tc7PFU  SpVxmz  XlxnNR7as  SrrC  O-Hn  QepXiJsmmip  h2k.rAa  gavx  .QDGfoaE WbtYSoY0YcnPsY z 6mkbw8e  \r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'dGI=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'MWtGRk9RbXk=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'a3dtelpUUFdDVg==\r\n'
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
fandango:INFO: Client: <request_auth_user_incorrect> 'NXFnT283YzRCbE9TVndYS2Q=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'MURVcDd0TW9uaQ==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'YjBYeV95Z3UwakU2d0VMWlU=\r\n'
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
fandango:INFO: Client: <request_auth_user_incorrect> 'T1RCUXZRN0tJbQ==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'M0xta0RIZzRSdHl5QWE=\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'U2hqZjJ1Wk9iOHd6Vmp6dXZvdTQ=\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<lnytzrnoovfnc@se.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<eelmyigzwptfsawrnh@dgljevlb.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: EpOZpHOa:NVygg\r\nfrom: olapfoiuxml@tro.de\r\nto: bhf@jrwfdn.de\r\ndate: Fri, 23 May 1975 19:50:54 +0000\r\nx-mailer: L\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nd0tQSEZ2VW1iTw==\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO JQH.yYeojlBzVQ  o1v 0b5-bHQXDfQGfvuFASos  r-eymYOaT0jGI20.0K D  iiBbAUuS \r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'S1h0aWt4QTQyOXM1WnJiVlBrZQ==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'bg==\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO hhl-zFxf3bp pfO6 tHlpxSsAMY2  6j  G.yKiaywgI kYMAFctpTu8Nq.nLGQW GSs MlK.ykld-igDvZ9k xwJLHf9l  4W5HCR  pa7IVBOGj8ljm75 a3V-.-xFKX  gOCm3 1ihwig MSEiIvg jWUr 9gPAdOwlX9r  fbrRaL1VQRTSj  3oEcabs2I4xF  \r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'cDdUUmZ6ME9yRzRZZG1HblZY\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'TzY=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'UTloUXBTTjhoTHYyMXo=\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<jrtszjtzfzwkadgy@etxhyhvnefik.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<cfwuqf@tzx.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: WPIuK_\r\nfrom: pvxejacam@cawvswjmlzbkifa.de\r\nto: dzlpxzhesiqug@sww.de\r\ndate: Mon, 12 Mar 2007 00:45:18 +0000\r\nx-mailer: hd\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nTXFyUG5qWWJZWWFnbnI=\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO C nm2p3FuOVo.FeETuxaqX dPUXilCn CNy3vrnVTI63ux.5mm mH6uPvXruLUANoMa7y  tI3aaWHKa1RxHdh vkcCPi  mn4TzqEdNB  vce2oWKMFbgg.R W1XqPoWmgTDRna.X  MJSlQJFCKpUlq6  5uOrSjR0 InqVVGg1kY  JAtJMWv2g84G1 AdjF7nkb.o48 izgEJ NvoIpP.nniQQy  \r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'NWVwcXNmUTM=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'YkM=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'WThGejlUWkxaR0wyc1VoOGtMZ3Y=\r\n'
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
fandango:INFO: Client: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_quit> '221 Bye\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_setup> '220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_ehlo> 'EHLO bg87r51  - .wTZ-Phpom5 HPUGc9ZExW hUfE9wfjGS4oiqXYWe Q  \r\n'
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
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_setup> '220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_ehlo> 'EHLO tV.rhwzdm rxbBx9rafof.N7 rtkE g23jMakWgj AsYLrW6GZlIu3pwFtl3Y  MjkNA1op9s8X2-EWifWZ  n ucK2Al  4  eX3u9GR y30b  \r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'YnBjWGpCb2hF\r\n'
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
fandango:INFO: Client: <request_auth_user_incorrect> 'ZlVO\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'NGtVWUVZV1hTcXJZeV9jenk2Qw==\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'Z0g5QjVyR3BidlBX\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'cFJfNDgwVjdEV0FqTw==\r\n'
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
fandango:INFO: Client: <request_auth_user_incorrect> 'N2U3U1daMmtLY2dBdjZTY1RKQTY=\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'eExwQ01SdWts\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'Mzd3UUVwMVhTMThhUVlmYkY=\r\n'
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
fandango:INFO: Client: <request_auth_user_incorrect> 'Zm1uNg==\r\n'
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
fandango:INFO: Client: <request_auth_user_incorrect> 'bjBfTXE2NGNlQkNW\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'N3JfQ1FrMkMzM3dxVUc0\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'OGthUEs=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'cEdEc2FOSUJjUnpteg==\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<dcconshhgh@ocnptb.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<fhympguj@nscjvzbvhxduqvhncydg.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: uMUdGc6\r\nfrom: bzvgnjvyrbnfzj@pvxfffnot.de\r\nto: oot@rhygkqrciq.de\r\ndate: Sat, 18 Apr 1970 23:53:04 +0000\r\nx-mailer: bDCyAJCJzuQzGHMXMcg\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nUVhlSQ==\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<rz@kuteassuswwoqerhrptj.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<csbngfesuhftl@qsnr.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: N.1FWXUKz9B\r\nfrom: jqpmhkncrxhoyktpezcu@jrizhf.de\r\nto: qn@meodtqptijzbbjnqk.de\r\ndate: Sat, 05 Apr 2025 01:43:24 +0000\r\nx-mailer: qdjLPqxQ\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nWQ==\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<g@adu.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<cxtuldg@zhstaslvlf.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: kZS t2: Cef\r\nfrom: ysbfewe@xydicgvrdqkaydf.de\r\nto: jxzsrm@hjureqvaokziwrhqy.de\r\ndate: Sat, 04 Feb 2006 02:29:03 +0000\r\nx-mailer: iYv\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nMXc3S2ZqcDQ=\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO nQsT  U  K0ZWCW0AEcVZkF-d iB0Fm7KLz.3GBnxyTV 8W2-r4j1lIdCW 3zgV  6OgM0H3ZwUO LLiAujlyRTD3p.gSX  A-ux5fzz76lTDJSj  X2SeNyvqh  lQgGTgnvuVItFi  .Kw7OeCI  7Ow-m2BWQr  \r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'WXh0Sk8=\r\n'
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
fandango:INFO: Client: <request_auth_user_incorrect> 'WEg0eVJO\r\n'
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
fandango:INFO: Client: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_quit> '221 Bye\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_setup> '220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_ehlo> 'EHLO a-6laxIGUIZCTAc  -VfzkK3E5-inwrtts3  xuSlW8at VvUO.ZjXP  hC9m1RgVujvZVvIw 0M84fJE98nBYgJ-t  xUrJSS4EP \r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'Znc1V3djdHhHSFE=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'ckI=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'dEM=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'ckxJWTRMbg==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'bGZkX3NNZ2N0X1U1OU4=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'OEw=\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO 3kQbrGQdVIvcbM JKF  37luC8vfxc  kE896Vx fi3afs5  R4JrapxdQxf  MvUkOnsW 4KEr0  HpSIJB10  HotOOAuUaY-WSZ  m7QgixY4zBey 5yHzUQBI VpSNC-Wy6. dIuDdWlHcupPvj  JXBwcWUXWoTWzYwpUaFJ  Nj0zNADX-fevUsM65wX  \r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'aktvdkwydGlxNw==\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'ZzZBMEp3OFc=\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO EzXWDAcR.EJXfwKhi  UD G  nR \r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<tkwqmqkbijjfodmt@wogrkzqi.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<tygtngxnqwob@jneevtzpawsqobw.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: c\r\nfrom: c@gtycpxirbpaidsovvg.de\r\nto: gjbpwblf@yyziaedcg.de\r\ndate: Thu, 09 Jan 2025 04:44:34 +0000\r\nx-mailer: ZhOFubFrxloW\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nREJMUXhONXY=\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_quit> '221 Bye\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Full coverage reached, stopping evolution.
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO Qgf6IEIQ IiQBY5ezM8N4.Gnu CVpV5L  2di7pUfcKLqy-IxcP  u0Mw8T  UuL AghWBA7Xkx  GaaWcfl ZV79NWCkPBcd -ocl6jt  scv YR8Z4ETP  ZBClY7eWyJt2  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\na2hLV2ZiMVV0VzBBUw==\r\n334 UGFzc3dvcmQ6\r\nWm9wRk0xUDdHaW0=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nNnVLN3RpbzdUZmEzNTV3RnE1Xzg=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<fjmunekgwsq@kkmzrandocxzuxxwunf.de>\r\n250 Ok\r\nRCPT TO:<jabgttaxsnou@tljluuwduudtmnpw.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: Lbn\r\nfrom: kexyrabxhixxoohvv@ppzdzddt.de\r\nto: prp@yzsbibvscvi.de\r\ndate: Thu, 25 Jun 1987 13:56:28 +0000\r\nx-mailer: SxLndNl\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nTmpxUEF5ZlhKalBmVFVVUwpyDUo=\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<xjnyxyvikmvc@lkidwgytjkzgvtiahtr.de>\r\n250 Ok\r\nRCPT TO:<tsugprtvyzkrnecbgld@zcznbnhc.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: IuuQW7ts\r\nfrom: x@qdxorcucyirndcukv.de\r\nto: xlmgbnvxg@zwjoottbtdkyp.de\r\ndate: Mon, 15 Feb 2021 15:05:00 +0000\r\nx-mailer: eprFfplphNeE\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nClBD\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<g@vlubij.de>\r\n250 Ok\r\nRCPT TO:<trl@xwivabz.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: 5s20tW3jD\r\nfrom: xuyouhwsugnujbmduwq@npdhp.de\r\nto: cakbhpkaxnxjeblrpc@tdufqgizfxez.de\r\ndate: Tue, 15 Dec 1998 19:41:00 +0000\r\nx-mailer: exOYRunUZBfJOPLX\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nRzlj\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO sgwl54Q1Md-  ZxLKYyXTL-UhYt  eka  0zIiHhyKS7yMzUR9Gdb e2BAnf  nC  nwzWWecDazHPK8  -6ekTrIffX8B 9kKD7c F2u  6Wsco PNK8n0X2vLn 5Cl8ESh YzHkyi6M7ZJI S77pBatCoyngFiS.QQ6  jiA1OVAKvDhUuebNGm83  RZaHLhOmX  MVqevYn xOH  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nczBJc1VEYXB0TmhiS0RuWnQ=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nVDluTTBTNg==\r\n334 UGFzc3dvcmQ6\r\nUHp0VzVkdDNwcU8=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nWjhhUkFsb3ZoSVFKZGdvWVRQR0Q=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nSnNRdWRfbjBWUnR0Rmc=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nMExoVGd2Qko=\r\n334 UGFzc3dvcmQ6\r\nc0Q1dXlWeThTY01IcWdEM2NH\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nYWg5bVRWMEhlN05Zaw==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nT1FLSzF5QUJJRDFuZGth\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nZTdRWThPcjZQVU9kMkU=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<jdbxrqhpv@lvygyfwlqkdwdzxxv.de>\r\n250 Ok\r\nRCPT TO:<wbfwzks@mkoiapq.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: .49KhWeQA CbH\r\nfrom: ucctpwrqcnbfpdf@fud.de\r\nto: pxqflxqbubepzdsil@pslalzwfp.de\r\ndate: Tue, 09 Apr 1991 01:28:57 +0000\r\nx-mailer: oi \r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nME44VFpkbFFGRDZWZWw=\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO o  o.Ip  0dg1HRbRqhR3kU  .acdvLEw8Z9ulF.L1n2  JXsw  G67Iw7Ez ZOjUmaaC7m isnppX.wvZdkGT  QAYqpdD4n-mbuaPM EFJ3mPMkA1MaoACICI  HPOAsC4RtX5Txu  jrzVHK  D5yJfPD  Qhn0pr50.aEPWSEOs.M  bq mFn7UYbja.QWmA3 40iIo7  FYb1  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nYWtuNW5FQnk=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nQW1OazFsY2N3ag==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\na0NPNFluck11U3UxMg==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nQ2NIYjlTbkFNU0ludndlWg==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO egRK9VBp35  EtGimFvdfaaSxNi5Hg-Q HpD1zBBuhGiPF h.Ku2moevnEdbXXnxT w8QWbZBKPjT4  c5  pP5A  CkA6ZZMY7loDPTjpkaUe  -BXOxX  X7HeNbmg7Kl0R14S  p1MLuvj -4F.FB9lJ17fPrx  79 yBD3eI2.7805SAAh  ZxssbWZyt07G2Q2 -BbcGR0.i8yn5c2Sdz  TDWJ 9u4W9G3Rpca9m  ZyWfl6zBl4JQP8Rgz URGD-J \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nTEtfQ1p2Zkc4MExqV1lCbzA=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nUUg0eQ==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nMTZNM0EyNVB1QVk5UXUySTN5SQ==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\naUtyS0g1N0ZycUI0R2I=\r\n334 UGFzc3dvcmQ6\r\nYkxpd0pwVDQ=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nNVZPVw==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\naVZhcjZC\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO TcT.RjONQX 0YxYyNFjWaIES  oBaU3J0RpCQdlnomXM  wiEcQFiZDwWWWbQjiB  QKHyzeIUhz0WLyy3MF  JWB2qbFhy0MlWNGsF b483jGjBezNl  yZ2HGQq8s7  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nNWtqODFDT1ZnbG5HOA==\r\n334 UGFzc3dvcmQ6\r\nY2djY2s1YTEwN1Yybw==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nZmpnUGVl\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<jdyyvkllgahrsihkwgyk@hulninfsordfasoszv.de>\r\n250 Ok\r\nRCPT TO:<rbbjcl@hwdevyc.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: -28ptESJXZJuQEX0T\r\nfrom: ufttfzhalzxextdg@oc.de\r\nto: ljorvtoy@tzifsmdzy.de\r\ndate: Tue, 31 May 2033 06:40:24 +0000\r\nx-mailer: lhRJiKEJ\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nVm9HZFF5bktEbmdnbw==\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<deejkiqnq@y.de>\r\n250 Ok\r\nRCPT TO:<tqaefrcd@lqnbafxwizxjrbujm.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: sZ4VmNWKcJ\r\nfrom: oqayisyhoqczx@u.de\r\nto: rhepe@xmikm.de\r\ndate: Fri, 11 May 2035 17:09:05 +0000\r\nx-mailer: x\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\ncE8wMzBNazBQY09h\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<abyksdll@tslw.de>\r\n250 Ok\r\nRCPT TO:<faikfiwymadnhrq@hggjynoxgjeeqhvctf.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: LYQ_MwG\r\nfrom: qoifqbexs@jywweuvr.de\r\nto: gmcmojfefddjbff@cgkd.de\r\ndate: Thu, 22 Sep 2016 08:02:57 +0000\r\nx-mailer: MZsAKwngUYTGg\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nNDE3U0hrU1ZyNFZjNTlSaXhXYng=\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<pkhbjtqxseaghx@bbqzovwnynzufat.de>\r\n250 Ok\r\nRCPT TO:<fueipdl@wmyjjnfinodnvx.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: -T-a09\r\nfrom: oqbkvvegwiwdppgd@raodirksiwwzwftx.de\r\nto: rncjsff@wumtvbdtepteupmm.de\r\ndate: Fri, 10 May 1985 10:08:54 +0000\r\nx-mailer: a\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nYnpiVVFv\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<bzndif@ei.de>\r\n250 Ok\r\nRCPT TO:<mxeolbubjnkbktaddv@j.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: DazRoSYI\r\nfrom: bk@pocakwahledftmowttq.de\r\nto: sxlrreglmknlfd@jn.de\r\ndate: Sun, 26 Sep 2010 06:58:45 +0000\r\nx-mailer: ziZxSGlDYxFPU\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nN2NNNmQ0VUx3eXE=\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<qtzlpgtownmwxznntck@vwovifjofozlednb.de>\r\n250 Ok\r\nRCPT TO:<hfvmgd@h.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: YNRJJqmD0s57fbg3X\r\nfrom: hwqdpniwpk@ovdqwj.de\r\nto: njdocairqtkb@sblkkzswvga.de\r\ndate: Thu, 15 Dec 1977 14:24:40 +0000\r\nx-mailer: whaAxKJPkyeIO P\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nN2FX\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO i0w F0vglowh  r  oiXl2orYzOTkop0  F7 axw  U  34H6 wtajuW  naO7eq-A61UsUTWv57zc f-jruJE  Fz9AA-3d0 g  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nTmlUbg==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nVk5OTjV5UzFxUXNuN0tOMUM5dA==\r\n334 UGFzc3dvcmQ6\r\nM2pLRWZoZ0pRMlJwbEJTTGI=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nT0tNMHpiZFd2T3JlSFIybTQ=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nT3ltOVRlUDBPWXBVVFkxWkkwdTQ=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\naW5wbGVMOVJOQXBJZ1AySmtY\r\n334 UGFzc3dvcmQ6\r\nY0ZmMHVIZEo4VGV0a0ljSkt1OXo=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nSEdVaFBY\r\n334 UGFzc3dvcmQ6\r\nQ21HTk5FV1VDZUo=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nVUQ0WFpaSmZDVV8=\r\n334 UGFzc3dvcmQ6\r\naFZSTklvN2l5aHhXNW5RR3ZU\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nMk5sOEth\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<xgzlhwr@rsfxzqvnzdxq.de>\r\n250 Ok\r\nRCPT TO:<t@osikdbidbbcte.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: 3KYPbgqlq\r\nfrom: kjo@sklw.de\r\nto: rmnxechfqijlc@e.de\r\ndate: Sat, 24 Aug 1991 22:14:26 +0000\r\nx-mailer: oyZkPCjWNgCnFEiVhWf\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nZ0h1a0VVWmNT\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<hmkosebqncnz@epqh.de>\r\n250 Ok\r\nRCPT TO:<pyuoljpdkapwzkioptt@yfuauiusocjqvhdiry.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: Lf_1OQXf1pv6vB5XDVX\r\nfrom: e@j.de\r\nto: oqcwcpsg@whbbemsi.de\r\ndate: Fri, 25 Aug 2023 10:00:30 +0000\r\nx-mailer: pupo\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nZTd5RFBzQjFSeUVhd1Bh\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO -Lyk  sH8pM.bv8XJ-  mgp7o4-tPYYnQ4dH ntTP  X2rgW  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nNQ==\r\n334 UGFzc3dvcmQ6\r\ncW1xRzVFeDQ0RFBiTWdXQkY=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nMFE4VnFBWXRIUVJKOQ==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nb1gwUThpc2VMZVZmb0c=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nYjJXb3ZfYWxDM2g=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO txR.2k2i8mwFIEG3 0T-ScXUZ1MIol UjgLEqEB3haZez7oBNb p6 w2RdP  eiSPh1GkmXATdFD  G3T  HfgJ3eYIsvya9s-  hFwGao.iTrBnF2V0 hu687Eta  VABJ03KBl aAkj qpdsCktV.n6mNOyAk 1QRfLi.7 mw3vpnY.M  d65YoxiaMr  pJOpcI3fm7y3Do8f \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO 0  Wt0BlBqvEJW4uhkE 1 FL2C0Xo5WnrVjLrKD WcO miKP dqvmCMztBAwkgH68rM  f6S7wMPu-fx2enhJt.  B  gr.c1QzKP7ks1tHJ5 4wYQ4eY7PV7xy7K  rCra8JDo1LWi4F7Q-  GNI-E  kjBAICifJ6y6wvnP5 jIuMPhVyPTX9N4PZMRCA uJ9YdNgANRJfpmliYa oChnM..EwkR2Z  eZmOrkcnEE ALbGBn6vtDrWC3B1  -oip06ZTFcckqA  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nVDVtUThPOWc1TDdseGpEd3VC\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndw==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nYVR3a3owd1FNbm4=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nc1NtOWFuNg==\r\n334 UGFzc3dvcmQ6\r\nenp4NF9VSTFkcERWUQ==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO Q36M5GbWkyt  IyJcLwj-aKDgqXqKK  ahx-jEaByomnimTfVHN 2224Crj3xHS9bBVyZyEg  Va276ai  dodTr  xQP0QB7K6WFdiqDhnS b3ngWPP  n8VePahlGqeulJYf4jl NJhDiWpbM0bhEKSyWC-3 gzpyorgkNGlxib4foJlf  L73NcUPSHOTNScpavKT MBS5wR.eL f.LYm2  KQD.nNsk bjesD95TWQiJ3XC  K.lD7UYVKyH2  bTRs4pTuuu 61S  nQpFn \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nanp3UV9jMDczT19ITkpuaHFrWFg=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nWkZGdnk=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\na1R3OUI=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO o952BD-g-SM  bzfxEusu4QHkbUrGK6QP QFzG9OqYpNFW5NOYWTvA  7wPOjezDcr8HFc1WD  uk8qiB3YeZ3TSuNCMe8  TsQlrnqv.  b0dkwaYaSeWO G BqV9 AwW4Xze1KV7OruOCOY 6HLaXM q-qzwUPsq aP 8vwHKcFdl J  e  SIAQ5A3O23eRdKJ \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nQUlBUEg1MQ==\r\n334 UGFzc3dvcmQ6\r\naWp0SkQxc3pxVXVqaWh0Rmk=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nTFU1dTU=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nQklGZFM3UXNwUXBFUzYzdEY=\r\n334 UGFzc3dvcmQ6\r\nc2RNNjhBZFV2c1o5Rg==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nbTF4YzYwcEVXUm1zREV5ZVI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<kyezkqefrutxqs@egbyvghfuhrussiavzuo.de>\r\n250 Ok\r\nRCPT TO:<h@kjivcxjpbixuay.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: ZAvag3Ra\r\nfrom: kzrnchscbyfdg@qjzcsbftci.de\r\nto: itlinbm@fgjoypiwgrvezcu.de\r\ndate: Thu, 28 Jan 1993 15:25:59 +0000\r\nx-mailer: tgKOGIdGEoKNEMjfywkp\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nRlVs\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<cxmaur@jwsiziqh.de>\r\n250 Ok\r\nRCPT TO:<dlbchkkopbaskihpvd@zs.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: RjELlWvLFCeb\r\nfrom: eastgigzwgjzq@cdkpzzgjdvrpsaussyu.de\r\nto: kugyuntqxzu@usxwznarlxrmoogmxzgy.de\r\ndate: Wed, 13 Jan 1999 01:30:19 +0000\r\nx-mailer: iu\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nSGJmRnFtaWFK\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO kpSKZE.W5bhxHre rNtk7 loOBygsPo Xp3P  UX6LgWg7wnPejoY 3KG0-nL4  gAdw-Mwqct.OQ- yWDaiDgqfR.5Yq  SrNdbjVwmCSg BJ44HRNrTEsZddjaN VZgsEmj1cHW  HFQnVA2oARaC  GJC \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndlNfNWpnZnNr\r\n334 UGFzc3dvcmQ6\r\nbnNPd3dMc2syVHpt\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<xhzrk@evekjqwnkpsixgfgnaml.de>\r\n250 Ok\r\nRCPT TO:<ayhsdbwnwbjb@hvjqxrnr.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: HuNsKLuCC:xuMBTvW\r\nfrom: ryggkoodni@ydngdarfjwljxlgtfaj.de\r\nto: uhbexdaglukttzsyho@gtdjz.de\r\ndate: Tue, 05 Jul 2022 03:02:59 +0000\r\nx-mailer: zQtLEyy\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nCms1WXBzdWJhemV5Qk5m\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<vttleljmsure@wnxivafbfrgk.de>\r\n250 Ok\r\nRCPT TO:<xriznibh@rv.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: 4C6B2\r\nfrom: lism@hicuyjwwwt.de\r\nto: pzoxfy@hhpvfsngvadyabsd.de\r\ndate: Thu, 30 Sep 1971 23:00:43 +0000\r\nx-mailer: qZYakMj fur\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\ndTk0V0U=\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<zmfxjobcbaje@vlmxkosbnx.de>\r\n250 Ok\r\nRCPT TO:<eyvfwq@nwohyhiowbap.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: ad:omVbbwzflA4 L0tg\r\nfrom: oupsfkuar@n.de\r\nto: xxyvkgtbysia@neaoigvqu.de\r\ndate: Sun, 01 Feb 2032 01:12:24 +0000\r\nx-mailer: uRY\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nQw==\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<hsmyw@qwhzrtejs.de>\r\n250 Ok\r\nRCPT TO:<w@lgfvh.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject:  n9dTFy\r\nfrom: bygzhwpfqemjdypffi@z.de\r\nto: itbulvakbd@hrvlpgxkijtvv.de\r\ndate: Sun, 05 Oct 2003 05:25:05 +0000\r\nx-mailer: XXFpkBSMM PcuSmFvOU\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nb1ZBYW9kMFVpTApwT0hDcEFVZg==\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<jzxxxxqdybkieal@arpacdtnaihameywj.de>\r\n250 Ok\r\nRCPT TO:<jez@egrjxu.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: vt_uu5A\r\nfrom: ypjt@kwnfhqials.de\r\nto: niuclkywcjqsaundjyf@tgpardbcxb.de\r\ndate: Thu, 09 Jun 2033 01:54:01 +0000\r\nx-mailer: GCgUCwZfJcJMbZuA\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nc2N2MTRSU25aNHA4aXRNWA==\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<nznceqzz@xad.de>\r\n250 Ok\r\nRCPT TO:<dul@dpvjusnan.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: 7n0cshcB4cI0YTkimaHJ\r\nfrom: youetbmsp@pzzzicxxewhddi.de\r\nto: f@xujutsmmnklsknkkc.de\r\ndate: Thu, 30 Mar 1995 22:25:53 +0000\r\nx-mailer: FmmtAMZSLbtSUrgnib\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\na3BNRUxUdm9YaWhEMgo3UnFxMzI=\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO lu 0QMB7gJ0CpXS U4oSEmVjHiMqz  tn-UDk2-wN XTO6qlWsR1cJU3o-Dhc 2h7KyvCQDkXtpfV  1zZ31epA7  p.Uzkfik-tx54PzGOESJ o9TnWIfmo3yBS5  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nRTJnNDlLS0x5VE1ka2M=\r\n334 UGFzc3dvcmQ6\r\nX1hKcTl6cEMz\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nS2hvZDJFRzc4ajg1\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nMw==\r\n334 UGFzc3dvcmQ6\r\nRzVYMko4WWw3Y2w=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\naXl6WHdleHZwRFJF\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<amnjdqrcyq@avhqrdhcpofoiesndaqe.de>\r\n250 Ok\r\nRCPT TO:<chrum@hjvhkf.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: 3TH_-IbyQ:CE1oG9D3i\r\nfrom: dgcbofvhqgsbasqbt@ndysuyryjaartnpr.de\r\nto: muoeaupgxht@ouowcqj.de\r\ndate: Thu, 22 Dec 1977 01:32:17 +0000\r\nx-mailer: AdmOltPdQUA\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nNmM1Vll1ekxHOGZpTjJRS0M=\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO akZ79ITN-VLMWOUh8x \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nZw==\r\n334 UGFzc3dvcmQ6\r\nTm9GZlpUdmNlUDM=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nMVAzZEdCeDdjUF9qZkcw\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO xZROshme  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nYmRvN3c=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nQW9iSA==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nNjZEcw==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nbDdIanBUOQ==\r\n334 UGFzc3dvcmQ6\r\ndTA=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<eknwwlqitrnbapsqbtf@dis.de>\r\n250 Ok\r\nRCPT TO:<amazbjfnxolfvsv@kqbenoehfltnqilq.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: Xi\r\nfrom: hbschn@wkjxnukysavuqmnasct.de\r\nto: bznd@y.de\r\ndate: Thu, 13 Feb 1992 03:00:56 +0000\r\nx-mailer: swCUBMLjCnqKHThe NCC\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nbk81OFppSGcN\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<ajqbayjyxkvtminfkyy@vdmjsezicxmg.de>\r\n250 Ok\r\nRCPT TO:<uhju@wkmtogwenuunggmgsw.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: xk4_ ubja6YF2Tbq\r\nfrom: zqqgrn@guiwvxakayynbsjon.de\r\nto: cmiovfxj@frlbcbhxhoykbdc.de\r\ndate: Mon, 07 Jul 2003 11:12:21 +0000\r\nx-mailer: AddqkazUAsY\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nRGRqeWVKcm5TTg==\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<ocokxltbfucwoatvy@r.de>\r\n250 Ok\r\nRCPT TO:<jrog@uslqfarrb.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: -wIdphS2AKm10m41WU\r\nfrom: ebdtwgxbdcadmy@lejtcpqxszhkucdypf.de\r\nto: fgubvbfzeigllmy@fdcfsszti.de\r\ndate: Sun, 08 Sep 1985 06:32:08 +0000\r\nx-mailer: ajRDCcqWKKfTUZnQ\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nQU9SVWhGZEMKOHRjcTFESFM5QVc=\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<yvffsdvvkpcvuxxg@tavfj.de>\r\n250 Ok\r\nRCPT TO:<p@xvwwuhbw.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: 5k-:60g A5D\r\nfrom: rpdfcjoyym@fzaczw.de\r\nto: bvejwklvsr@x.de\r\ndate: Sat, 09 Oct 1999 22:48:11 +0000\r\nx-mailer: xdgIBzyEadrtTE\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nMVhvN1VsOGVxVTJWaGsyYg==\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<mqdtzrnaexqoybm@flbhxstnvtl.de>\r\n250 Ok\r\nRCPT TO:<cltbi@rvla.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: m\r\nfrom: evifwsbauvzwoffdxc@hwqkhifpdpxskdkyx.de\r\nto: dy@aewcxdxjhqfjb.de\r\ndate: Mon, 30 Jan 2012 11:48:48 +0000\r\nx-mailer: zPQIkKYZESOoMgTQJN\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nZG9vYUhiQVdmQzFH\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<dbdgooqcngvgiarzpet@etgaimj.de>\r\n250 Ok\r\nRCPT TO:<disivrih@wkdjdvqcwcw.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: c -dVCPyW\r\nfrom: vdb@wcj.de\r\nto: tdcjusmuxy@aqkg.de\r\ndate: Mon, 25 Oct 2010 21:00:13 +0000\r\nx-mailer: EYlActqPYY\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nSWFsa3V3cQo1bXB4WkR2RDA=\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO 1AdA08ZWZh 2 Txhx9  A712N7Sy7LiMc  Bjyt3Yvh3  41-oodqIF.Rgr  eRe5Mzy  cDR0FSTKN.I scDu3hOuFYwqBR6fz 9gvDxWcGeOg2vlEm \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nZnYyY3g=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<maypcrlctyemuoqduvg@wnikptmtckzqdn.de>\r\n250 Ok\r\nRCPT TO:<viotghwqogb@sclcpewzegswllwlodh.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: B5q-jE:a1\r\nfrom: oeevcvv@itoint.de\r\nto: xqzeixl@gkqulsb.de\r\ndate: Wed, 14 Apr 1982 06:26:11 +0000\r\nx-mailer: xJjItBetAcIGl\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nQnVKCg==\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO zpe5RCHBfF yb-nO59NPv jauyaV0JJqtV ul 8  RZSc1FUOz1lj9vI nLsw8rB ywaFacN-rv0vm0D7AK  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nXw==\r\n334 UGFzc3dvcmQ6\r\nVF9nMkJiRU5TWU5KSHpi\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nNVlheGZTdzBCZjgwX3o=\r\n334 UGFzc3dvcmQ6\r\nRUJXVlBn\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO W -gpmk v5UQ2D2WvL  .tQjIk06G4t5iN.2U OUSUlkVl2  UXT  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ncTFJSWgybm52YXhUcQ==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nWXhleHo2WVBsN2k=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<skxxcedbnlqdvbwlin@fh.de>\r\n250 Ok\r\nRCPT TO:<lsmdaiuvewmbflhbpyy@zectzstoo.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: ViEtRCkW.kR42vf6fwlu\r\nfrom: wdrmbqhq@nk.de\r\nto: bbkl@iwmucpvsjwloygjoa.de\r\ndate: Fri, 18 Apr 2003 15:50:58 +0000\r\nx-mailer: fiVRUqbpHzSzHLvnIlA\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nUlo=\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO bqLZpt1pd8 .TlyS5QgbYKV6  H-FSmi-Yv  LoX 7ljbMk3mCua6IlQsKVX avlM  bpyDPCjb  i0g1tKz8  .UnqURWlZ2WB7fZcFH I1 ODySlk  7srovkonqUjIAt Qxrhx fn6  ntuG  iO3vsxictnL1vZN07eUw  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nZ0UxelpRcnl1TkNtdg==\r\n334 UGFzc3dvcmQ6\r\nc0NkU05lWUw=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nazVoOA==\r\n334 UGFzc3dvcmQ6\r\nOHNUNHFDdm0zNTE3Tktn\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nWnBvNmZoTzha\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO pMwPfqhga Vx EfQvX210J  4IlD awrogzQcrnGzSxEwG8t -etz  sUL H--Y-9qpL1xEUek8  n yBfrT1a-4P6  yjX.8XGDHoTzX6 dqwk5GpXyblfwS phl5eP4 YMyYBrkbuFt L-sb pdMXpsi4Am.KUZtOi6u  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nSTNSdEo4cmpTQmZhb0hKMDN1OWM=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nbHh3VExqUlVGZjVvMkdVMDVCNQ==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nd3JieEN3cEUwNWExbGRK\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nX2VhYlZ2Rw==\r\n334 UGFzc3dvcmQ6\r\ncE45bThSdFQ=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO SimJnlQxHJPB.XIDi  H856J0EtUM-BDRSfZB7 Ix7UqDeiEF5pe2y tc7PFU  SpVxmz  XlxnNR7as  SrrC  O-Hn  QepXiJsmmip  h2k.rAa  gavx  .QDGfoaE WbtYSoY0YcnPsY z 6mkbw8e  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGI=\r\n334 UGFzc3dvcmQ6\r\nMWtGRk9RbXk=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\na3dtelpUUFdDVg==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nNXFnT283YzRCbE9TVndYS2Q=\r\n334 UGFzc3dvcmQ6\r\nMURVcDd0TW9uaQ==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nYjBYeV95Z3UwakU2d0VMWlU=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nT1RCUXZRN0tJbQ==\r\n334 UGFzc3dvcmQ6\r\nM0xta0RIZzRSdHl5QWE=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nU2hqZjJ1Wk9iOHd6Vmp6dXZvdTQ=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<lnytzrnoovfnc@se.de>\r\n250 Ok\r\nRCPT TO:<eelmyigzwptfsawrnh@dgljevlb.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: EpOZpHOa:NVygg\r\nfrom: olapfoiuxml@tro.de\r\nto: bhf@jrwfdn.de\r\ndate: Fri, 23 May 1975 19:50:54 +0000\r\nx-mailer: L\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nd0tQSEZ2VW1iTw==\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO JQH.yYeojlBzVQ  o1v 0b5-bHQXDfQGfvuFASos  r-eymYOaT0jGI20.0K D  iiBbAUuS \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nS1h0aWt4QTQyOXM1WnJiVlBrZQ==\r\n334 UGFzc3dvcmQ6\r\nbg==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO hhl-zFxf3bp pfO6 tHlpxSsAMY2  6j  G.yKiaywgI kYMAFctpTu8Nq.nLGQW GSs MlK.ykld-igDvZ9k xwJLHf9l  4W5HCR  pa7IVBOGj8ljm75 a3V-.-xFKX  gOCm3 1ihwig MSEiIvg jWUr 9gPAdOwlX9r  fbrRaL1VQRTSj  3oEcabs2I4xF  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ncDdUUmZ6ME9yRzRZZG1HblZY\r\n334 UGFzc3dvcmQ6\r\nTzY=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nUTloUXBTTjhoTHYyMXo=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<jrtszjtzfzwkadgy@etxhyhvnefik.de>\r\n250 Ok\r\nRCPT TO:<cfwuqf@tzx.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: WPIuK_\r\nfrom: pvxejacam@cawvswjmlzbkifa.de\r\nto: dzlpxzhesiqug@sww.de\r\ndate: Mon, 12 Mar 2007 00:45:18 +0000\r\nx-mailer: hd\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nTXFyUG5qWWJZWWFnbnI=\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO C nm2p3FuOVo.FeETuxaqX dPUXilCn CNy3vrnVTI63ux.5mm mH6uPvXruLUANoMa7y  tI3aaWHKa1RxHdh vkcCPi  mn4TzqEdNB  vce2oWKMFbgg.R W1XqPoWmgTDRna.X  MJSlQJFCKpUlq6  5uOrSjR0 InqVVGg1kY  JAtJMWv2g84G1 AdjF7nkb.o48 izgEJ NvoIpP.nniQQy  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nNWVwcXNmUTM=\r\n334 UGFzc3dvcmQ6\r\nYkM=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nWThGejlUWkxaR0wyc1VoOGtMZ3Y=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO bg87r51  - .wTZ-Phpom5 HPUGc9ZExW hUfE9wfjGS4oiqXYWe Q  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO tV.rhwzdm rxbBx9rafof.N7 rtkE g23jMakWgj AsYLrW6GZlIu3pwFtl3Y  MjkNA1op9s8X2-EWifWZ  n ucK2Al  4  eX3u9GR y30b  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nYnBjWGpCb2hF\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nZlVO\r\n334 UGFzc3dvcmQ6\r\nNGtVWUVZV1hTcXJZeV9jenk2Qw==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nZ0g5QjVyR3BidlBX\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ncFJfNDgwVjdEV0FqTw==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nN2U3U1daMmtLY2dBdjZTY1RKQTY=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\neExwQ01SdWts\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nMzd3UUVwMVhTMThhUVlmYkY=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nZm1uNg==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nbjBfTXE2NGNlQkNW\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nN3JfQ1FrMkMzM3dxVUc0\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nOGthUEs=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ncEdEc2FOSUJjUnpteg==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<dcconshhgh@ocnptb.de>\r\n250 Ok\r\nRCPT TO:<fhympguj@nscjvzbvhxduqvhncydg.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: uMUdGc6\r\nfrom: bzvgnjvyrbnfzj@pvxfffnot.de\r\nto: oot@rhygkqrciq.de\r\ndate: Sat, 18 Apr 1970 23:53:04 +0000\r\nx-mailer: bDCyAJCJzuQzGHMXMcg\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nUVhlSQ==\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<rz@kuteassuswwoqerhrptj.de>\r\n250 Ok\r\nRCPT TO:<csbngfesuhftl@qsnr.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: N.1FWXUKz9B\r\nfrom: jqpmhkncrxhoyktpezcu@jrizhf.de\r\nto: qn@meodtqptijzbbjnqk.de\r\ndate: Sat, 05 Apr 2025 01:43:24 +0000\r\nx-mailer: qdjLPqxQ\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nWQ==\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<g@adu.de>\r\n250 Ok\r\nRCPT TO:<cxtuldg@zhstaslvlf.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: kZS t2: Cef\r\nfrom: ysbfewe@xydicgvrdqkaydf.de\r\nto: jxzsrm@hjureqvaokziwrhqy.de\r\ndate: Sat, 04 Feb 2006 02:29:03 +0000\r\nx-mailer: iYv\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nMXc3S2ZqcDQ=\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO nQsT  U  K0ZWCW0AEcVZkF-d iB0Fm7KLz.3GBnxyTV 8W2-r4j1lIdCW 3zgV  6OgM0H3ZwUO LLiAujlyRTD3p.gSX  A-ux5fzz76lTDJSj  X2SeNyvqh  lQgGTgnvuVItFi  .Kw7OeCI  7Ow-m2BWQr  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nWXh0Sk8=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nWEg0eVJO\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO a-6laxIGUIZCTAc  -VfzkK3E5-inwrtts3  xuSlW8at VvUO.ZjXP  hC9m1RgVujvZVvIw 0M84fJE98nBYgJ-t  xUrJSS4EP \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nZnc1V3djdHhHSFE=\r\n334 UGFzc3dvcmQ6\r\nckI=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndEM=\r\n334 UGFzc3dvcmQ6\r\nckxJWTRMbg==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nbGZkX3NNZ2N0X1U1OU4=\r\n334 UGFzc3dvcmQ6\r\nOEw=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO 3kQbrGQdVIvcbM JKF  37luC8vfxc  kE896Vx fi3afs5  R4JrapxdQxf  MvUkOnsW 4KEr0  HpSIJB10  HotOOAuUaY-WSZ  m7QgixY4zBey 5yHzUQBI VpSNC-Wy6. dIuDdWlHcupPvj  JXBwcWUXWoTWzYwpUaFJ  Nj0zNADX-fevUsM65wX  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\naktvdkwydGlxNw==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nZzZBMEp3OFc=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO EzXWDAcR.EJXfwKhi  UD G  nR \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<tkwqmqkbijjfodmt@wogrkzqi.de>\r\n250 Ok\r\nRCPT TO:<tygtngxnqwob@jneevtzpawsqobw.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: c\r\nfrom: c@gtycpxirbpaidsovvg.de\r\nto: gjbpwblf@yyziaedcg.de\r\ndate: Thu, 09 Jan 2025 04:44:34 +0000\r\nx-mailer: ZhOFubFrxloW\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nREJMUXhONXY=\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'

Process finished with exit code 0


Coverage metrics:
Nr trees generated: 31
Nr messages exchanged: 1217
Overall time elapsed: 174.11s
