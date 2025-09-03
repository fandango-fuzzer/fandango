/Users/alexander/PycharmProjects/fandango/.venv/bin/python /Users/alexander/PycharmProjects/fandango/evaluation/experiments/smtp/smtp.py 
fandango:WARNING: Symbol <pass_incorrect> defined, but not used
fandango:WARNING: Symbol <unix_time> defined, but not used
fandango:WARNING: Symbol <mail_contents> defined, but not used
fandango:WARNING: Symbol <user_incorrect> defined, but not used
fandango:INFO: ---------- Initializing FANDANGO algorithm ---------- 
fandango:INFO: Generating (additional) initial population (size: 100)...
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Initial population generated in 0.00 seconds
fandango:INFO: Current coverage: 0.00%
fandango:INFO: Server: <response_setup> '220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\n'
fandango:INFO: Current coverage: 0.03%
fandango:INFO: Client: <request_ehlo> 'EHLO o2whGz4p-iUwPJBo xj1h6  L  sIT0.4Gb.0oGHMgQJ  \r\n'
fandango:INFO: Current coverage: 0.05%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.11%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.14%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.15%
fandango:INFO: Client: <request_auth_user_incorrect> 'amhENWxGMTZHcEFxRm5hQ0xFX1M=\r\n'
fandango:INFO: Current coverage: 0.18%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.19%
fandango:INFO: Client: <request_auth_pass_incorrect> 'SUtBbVdpSE9hSVZScQ==\r\n'
fandango:INFO: Current coverage: 0.22%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.24%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.27%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.28%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.28%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.28%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 0.31%
fandango:INFO: Server: <response_auth_success> '235 Authentication successful.\r\n'
fandango:INFO: Current coverage: 0.34%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<vaniurjsmbtgac@bkqtcjf.de>\r\n'
fandango:INFO: Current coverage: 0.39%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.41%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<hz@uuqf.de>\r\n'
fandango:INFO: Current coverage: 0.44%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.47%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.48%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.49%
fandango:INFO: Client -> Server: <mail_data> 'subject: 4di8.vzT02P\r\nfrom: ael@cifagajtwevkxzqg.de\r\nto: tqhqquvyxeyimewix@wjvglhyffmepshlga.de\r\ndate: Tue, 18 Feb 2003 04:32:43 +0000\r\nx-mailer: apVg\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nMg==\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.74%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.77%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<pucjvkazlbedrturgt@dcvfk.de>\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.79%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<dlljsgnkbt@zktbrtodrnwhoa.de>\r\n'
fandango:INFO: Current coverage: 0.80%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.81%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.81%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.81%
fandango:INFO: Client -> Server: <mail_data> 'subject: fTKlYOWXg:Ojou63\r\nfrom: pkorhqfvdcyeyehnyyqp@zuqtcoi.de\r\nto: hwvfwigqk@pogl.de\r\ndate: Thu, 24 Sep 1992 14:12:32 +0000\r\nx-mailer: DPDVY\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nNnJQ\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.82%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.83%
fandango:INFO: Client: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.85%
fandango:INFO: Server: <response_quit> '221 Bye\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.88%
fandango:INFO: Server: <response_setup> '220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: Client: <request_ehlo> 'EHLO Ii4HHYqUzfrYe0QjIq  0ZockNbq7 xluCoiMo uYw4hDkn5cvy 9gbwYGX oPWXPbvlmJkSUmBV9-fb  msF ulv-nvmWvS4vnAmyrZt  N6PIjndJ4J47 Awg6pLj09OR2IglcCrm  .FQvKgUHPV.A17V  fgNjhRD0fAWe6MWj8v sgvy9-CZ.MKJR  D-iK7XTQZmW5xgyV  89lUPfGOjSZBVr  aqaThDW3IdK2qYbv b0p6B7B2IWZiem1136  \r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: Client: <request_auth_pass_incorrect> 'WWliMENhWHBLMVdjOTBsUnhaTmc=\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.89%
fandango:INFO: Client: <request_auth_user_incorrect> 'c0I0TmI2ZnRzblQ=\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.91%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 0.92%
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'MkNLS2U3NQ==\r\n'
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
fandango:INFO: Client: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.95%
fandango:INFO: Server: <response_quit> '221 Bye\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_setup> '220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_ehlo> 'EHLO MyIbXwlM3qDfnbvx-FI  O9edlI5o9GuakINcNQDN P. eJn R87aTKRge0ubJ  U8AfBl5rRRk..zrCysQ 7MLCc-vegxo5.Jv LRE9398l1In MNenRV \r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'c0RGSA==\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'TXRzN3NJYnI=\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO hRPdwqes 1r7QKIZ8jzzZ  lEX9bVdto1 a7xOnailwNeYUwa  d  dbEgq7ccWk  7fpl  e1ugXyoP  ms.PB6yXYSELCyQFr6L x5yqU0fj5Pw  AGXBonovtw  7TeobGgm  gGf0L  4Xp4SJs4Q  dDR2h uQASOAZ7cbY1voc 5Bs316huOfMh-  6-1y6tcSC \r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Client: <request_auth_user_incorrect> 'TVd2U08zOVlqYVFSbVBGcVFVNw==\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<qxlnzhrn@u.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<chjhhxxiaiebquo@gzbgow.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: 65jb1-9eObog0\r\nfrom: sajpnlzgyyac@mgoprbqvncpqtzwh.de\r\nto: adcigtcfg@uvqaklkmcybbfitosi.de\r\ndate: Wed, 02 Oct 1996 10:52:16 +0000\r\nx-mailer: Q\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nQTB5RXhkOFB1cXg4Z01WSkg=\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<ckaqpmvdasmbu@osxi.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<qipxejlpgwzvmc@aed.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: 10V\r\nfrom: tnrafskoolysjaqm@kgrcdt.de\r\nto: ixrlqewypcgaxnbn@xsgnxs.de\r\ndate: Sun, 02 Nov 2036 13:42:57 +0000\r\nx-mailer: uLss\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nZ1M1UDFDZUpDTzNKVm95Q3ZSTQ==\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<zcl@zurnrk.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<jtzlynhmqfkvj@hqxkquqvpaarsvmgxi.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: dKmCHjVAK.DALXl\r\nfrom: hxw@ncteygpmhnvnwoidwirg.de\r\nto: snomhxtczymkkpcjt@rtqpzumtdogzsxelcnd.de\r\ndate: Thu, 18 Jun 2020 14:52:28 +0000\r\nx-mailer: vapkZAioXdRez\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nQzB5RDIyNDJM\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<huz@vugiacmna.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<huvr@tqovgwxdcq.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: LWlebwdA7iKUbvNh\r\nfrom: ybxshqkpji@qaqlqu.de\r\nto: xuoxcscolvsc@wucdljguwfdtnkod.de\r\ndate: Tue, 23 Jun 2026 08:22:54 +0000\r\nx-mailer: jUMpaxWlEwSfs\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nakRCVDUyTzd0WlQybzBnWkc=\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<xvh@g.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<uqjfsjsbfuvxnsrvewdv@iifbbwkvdzhhuujzozvv.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: wEnvx4WOTFKPjW8n\r\nfrom: pzemdvijcpvxbmq@yqihcswbcmgqxeq.de\r\nto: lutd@xz.de\r\ndate: Sun, 26 Sep 2021 18:56:00 +0000\r\nx-mailer: EmPyCYVuTPIyGFZA\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nd0hP\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO 8I5Aj0NSxh 70bToiVHL-XSNg  J5f6P 5Z15k.Mz1UtQYguDhJbG 1Q-XVOvHXS-  0.pv6CIvhdGKdwsf-  \r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'UlZnWk9Yag==\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'NXVEQWJRVHNrNlQ0\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'MA==\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'QVFrSkR2SHFqZkNPRGpzbGNYM1o=\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'NGZCVEI=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'ZnpxMVNxQjJHS24=\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'Wg==\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'b1hnSw==\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'ZEwwaUxSclVZODNFNg==\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'WWFLR0VHSGlTeVhUNEk1dXd4XzE=\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'Y1BrN1c2bWZXZURLaWtlY0RJWg==\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'QXFhc1MweFo=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'VFJwSg==\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'VEhzNzlpaG9QajFTdGhqZA==\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'c25hUFNLMjVHVmY0\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO kObAd  I3qBN  ZUOgWQtGrmVdOepOo  7cOdZZvGUMb93o-  MsKJifWXWF  SVea2M  Q7exS-R.rrMboGt-GW KXfzHCQ3r.AQcM kDzpQXSe1 argYsOt10gqt9hTf  EF3Q6Eo 1iRx pc4xqOc ybX1rWbkYTQtHGYI0A76  02bHN6T0vhLmlS3-tb qPjaJEJQJ-ivxF nFLppoemxnNieF 3SlGW \r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'eHBNNDFhWHZlemFFZjE4RTZF\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'bWtFZDFSTmp1bFJBcUY=\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'UWtKd1pmakVDd05ueTMwWTU=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'VHJOVkE4NUoxMTVnZQ==\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'Mg==\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'NHNDQkhqNWg=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'WDdTbEE4NWNjWDha\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'cWtiT0owdU9qd3hoOQ==\r\n'
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
fandango:INFO: Client: <request_auth_user_incorrect> 'VEdJeW1Yb2xrY1NZdnpaZ3FaVA==\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'SFozOHpBRHRuaFM=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'UWtSczVKWUFsbTZj\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'MWhLQm5JQmE4cQ==\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'WUxZRDN2NkNoVHZwYUZkNg==\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'dVFiRXNRanA4SXU1\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'UmU3ZEswN0JNQzVlSDU=\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'U2RHSEtERWZ6QThyYnU=\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<zjprqqxyuvqg@rexubymbwmfwhrqhufu.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<nemgapggaspmtqky@qdmzx.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: C6Au15SNJ603bC\r\nfrom: hse@wtsptphehbbn.de\r\nto: nuktsvqtvqns@njkrfteswomgeig.de\r\ndate: Sun, 10 Dec 1989 09:13:39 +0000\r\nx-mailer: jBAsiGjFXvRlo V\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nb2dhZw==\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<jlsxzbbo@kqnvxjyxj.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<jmtfaawx@xxgxjfmvreydbdnldru.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: 7SEgiwTuNROfcr\r\nfrom: esvkpmwfaizfy@vbbmjle.de\r\nto: wajgzhjwolyccnbguvek@ceuxzfiyjwo.de\r\ndate: Tue, 29 Jul 2014 16:35:22 +0000\r\nx-mailer:  wft\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nWWZTVEFNRXp4VUhpNTh0\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO CbLOhih2ic d5ugmq07eloAqJvq7UZ  zgKrX uDDKnT-DY44XkiSnoyhi  L9 1Q5P2j  M 1XfTx3Qk  TN-xcI8fXSQenYC7MvQW jAj5wAZH3L6wLp-iCal3  gcDE7  \r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Client: <request_auth_user_incorrect> 'b2RiU2FOT3Z1\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO iXF8bH  nmT jVFb npnnqoK2d bUdiQiPwmCV2  4XYGW  j3i6hp ILRn  Hzzb3-4zNCMOE Lh7PlT ikGRgtTRgdyJ  ZkEEHyE7nQWsZ  Na1z Vup3xA.96kJ z-kh3dFGqwwC7X s81AIvIRNnGj1cCUw-  \r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'UQ==\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'amhpdFloSGFQd2ZEbndz\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'eA==\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'dVFR\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'cjFZZEtYNVlvRW4=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'c2J1bWVoM2xwQUZTOHM=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'dQ==\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO 1g7S.Ik  Euf tYYdHq8w.LJUEV5WT1A Ia4QC2KgqtGodEHV  7kB9xid g2mjY33S p3sED8Uy  s-W3pJ AZ8ezxYhQludxy3vua9u g9  DGRG  Qcw58Amuw5RUyZ7H  X9Cs  BWxRY.AWbqZQpS3G3 14B.05b Jj7L rNj0ItDT0SMIjiH-  iBJ-6O  - \r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'b2U1ZjZLeWtwSXc4Tzk3WFZITFQ=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'TXB0X2FReXdoY1ZjOXBiek5vRw==\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<avzv@mqfzjrjsmyo.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<zyoqitywcydy@fdmokfjatkitkzqfxrrg.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: 1x.m6hpcgJ7b\r\nfrom: scw@gfhkrbidynthqo.de\r\nto: auiyez@zmspsowargopm.de\r\ndate: Sat, 27 Jan 2001 07:46:30 +0000\r\nx-mailer: bvNdoiFXRLlmCBOP\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\ncFJmc25BVzZpT2hSUW1lWHhYSU8=\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO 8AtI-giGV-1HehG2 RnTDeDOLv.e5  vc1  eKBN sjft2ZXNnboO58lESC  0ODeywnEG43 7WS9uYvKN10  fTAyU29xWH KdqTsZlx-V115oDuqdgH gxqcmsLQ761u mP lRl53BLSVsK29N4 U1  kHcI4vuX2NcSCBpsGOJ9  \r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Client: <request_auth_user_incorrect> 'dE8xUko5djRJS3Zi\r\n'
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
fandango:INFO: Client: <request_auth_user_incorrect> 'SjVzaF81WGNhag==\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO niFNliE0QztDYTsPfz M6-I rlPatc gLLZD1jRhuIjnCY5Ic  rZosRf  \r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'SQ==\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'aXVGZ3JjcGdGUmhMd1d2Tw==\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'RTBjbzBIdXhlaFNwSg==\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'WFROX0E=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'UXRzMlZSblh5VEl4QU5McXli\r\n'
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
fandango:INFO: Client: <request_auth_user_incorrect> 'Zll2dE1POGxsSTdfUDE1OGh3\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<qzrd@ffdkyez.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<ewkixflvj@lnhvzlvppcemigfant.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: g7p\r\nfrom: mnqlcarmcubcwpbd@l.de\r\nto: lvktntoftupmhltj@gvzpaodi.de\r\ndate: Sat, 12 Feb 2000 17:30:47 +0000\r\nx-mailer: QrsGDCfUWfFB\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nRnpWUHZVaUN0YlgzWnh0\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO .3z  0EsS27ESHbv  F3h HoTi0pOd 8CvJgqWRloNLatDJ7p  YDfb3Qc9MxTcgZFMdvSr  HkiWP-ZVQIAWvSjMHV Ik rsuIcsWOG  nc4T6eizy400h1X  8IC- 8lu8N8l3Ray1XQu  sK DqE40KvVIE2Tyos4RW wKc7tsC5rdQHrq  zKoBCI RUphPodgGmo  \r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Client: <request_auth_user_incorrect> 'ZDl4T3VBbFY=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'QWNUclVQYjZfeWI=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'alFyNVhUZ2Q=\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<pmkokevtbgz@quyznqmolujtcdltbn.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<waylzpszqpdztgwml@xejs.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: wuLbXkHn\r\nfrom: lnscm@tighmymarvim.de\r\nto: xhoyj@umohkivfjdvctcp.de\r\ndate: Fri, 23 Mar 2029 10:39:59 +0000\r\nx-mailer: RnpZwMMw\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nbGtEZGl5RlpxV002eQ==\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO ZzOQLPAma  .Fw8qYAqT8TMbM0P  KDwDhL12bG  PmsY-7ED9cwKpnwZ48w  3bPK9d6fa5Oj6yXQCN91 l.3EktqnVkyuj1r  uxN4  .wlwivkPNnpkygfCQX0X yHe Vv5aJb2YDuY 1lmmJB KqM5HFwzP  BYOhYRjSOnmhX 6X RfYGvAuwz  NC8S.iys3fGg OYizbRwgjPj -uyBi WF \r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Client: <request_auth_user_incorrect> 'cV9yVGNxZDY=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'amhZalA0b3hySEFF\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'Q3N5WllHVjl0aFg=\r\n'
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
fandango:INFO: Client: <request_auth_user_incorrect> 'OWJOdTI5ZDdmcGkyQTBtQnI=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'WnFweV9W\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<ddamevmjftcinlzu@sntiard.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<xakyxvrknw@bhpqkhkpfuhfjm.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: hsFs.m07xN\r\nfrom: dgaicihcvyeo@bfiesark.de\r\nto: ggdhvezctxwemtwnt@tgwylzegeyptqsvjp.de\r\ndate: Wed, 27 Mar 1974 06:46:26 +0000\r\nx-mailer: qOLffoxJZpZDRiqpbuG\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\neQ==\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<bg@bbkfcexavvnioofq.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<zqdqmzhldlxbpnums@tyqkxgxr.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: I:\r\nfrom: ycwf@rjyldbqwcoebcn.de\r\nto: pg@qdciko.de\r\ndate: Mon, 24 Oct 1988 07:45:14 +0000\r\nx-mailer: TZWhdVzSedYGn\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\ndkRTREJnWVFmTVpxMU9l\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO oA.  r1LnEtm1sg.XPvV  vL  42k  iQA oiJkyqdWB  bSYyc4cXjIsD6KuY4  181KsENR7emnJ0Q3v  7vVPWuVWNUgh 7F-ZHVx..wcaKyEwRRUU  68a8ML8fbD1SqE  Oi-G-iJGT wIDyX5mkyRgYrxkKG  \r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Client: <request_auth_user_incorrect> 'Y1NUdlJxeWxvYVhZbnlhNExkUg==\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<oozalnesoamdzxifqmsq@djjiwxfzzdsfvlt.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<bzhb@segzxseskgmbfuj.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: rsoSHq:12BPBQOp\r\nfrom: ei@gm.de\r\nto: oez@hek.de\r\ndate: Wed, 22 Nov 2000 14:30:59 +0000\r\nx-mailer: CUxCzbZZAwKeHU\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nbkZyc1oyWTNHelEKdDR0cmhsTQ==\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO a37NalC  V6cNILtG7oQ  OHyzHz3-oGe517QcI3b jl 3n 7  QHsg cy6wMGjgeRfaXXJ  X-voTUKH -D yvfHvEUXgB  2JPYTUOY  .CHN5V8-R9Qq3fv5s fNTUSYd OQz06fyV21KHwlncrX2 78t  41KTwCJEonAi5MJXRVC  vVQnrZzzd P-2rPmj0h2  \r\n'
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
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'ZlpsU0hKYzhTcWdWTGtBWg==\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'Ng==\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'RWFmNlR3\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'NU8=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'cHhvMXljTHU5Z3g=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'ck5mVkdlc3NTVFQ=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'eEpwekw=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'Tm5oWndNZ3E5dXp4ODNW\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO f .rXG7ypKPyDW6I36 \r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'eVRWS1ROdWJWbGU=\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'eFN6cUdYVWtFZTFJcmtRUFNOcA==\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'Mw==\r\n'
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
fandango:INFO: Client: <request_auth_user_incorrect> 'aVpFTnJyZXlHVA==\r\n'
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
fandango:INFO: Client: <request_auth_user_incorrect> 'R0tpTUNEQUE=\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<qystyzvnyuthl@xtumvsxy.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<tliargtlld@ewyciytmhcex.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: wJC.Diga\r\nfrom: kiuun@ygat.de\r\nto: lsubwqz@jvpicrfot.de\r\ndate: Fri, 18 May 2035 11:15:04 +0000\r\nx-mailer: wWZLvAJmwpajVwlo \r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nUFZNWDhn\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<vyppstmuwewwhi@acqsnwlhbi.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<gyb@aktauzyphmtjwt.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: IiyBlhmFiYRGchKFKY\r\nfrom: jfgecc@pkuwhbgbryxihuqhci.de\r\nto: xbximncpu@eslmrudvyrmvbusyy.de\r\ndate: Wed, 01 Jul 2037 07:25:33 +0000\r\nx-mailer: UvBaVjuryw\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nekdvMEszQVk1WW9Md1k1QQ==\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO pDDVNpYm.Lat sC2R2SgmJRbW.JZ5 40-lR1w US2HbPBbRaIXc5v- ra- 6Xe9k5dxmEWi 7x1QWwYijU. ACMIF9FIvrsLN  1Ip0kHvpwtp aqx8L2dIwXgqXtpXy Erj2uIvq  ARK5  RHOAxD  XEUJmpjehcpY8HQz7  UrP.gYBB-zqG-XImz6Zf 65Koni 8Fdi JAijURFHsvaJSgf7a5S e1wM1DxLE0UCu7FJXC0  jz5sA \r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'b213RlJqSFJNVw==\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'M0dlYTI0SXBMc2gzQUZvNkc=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'R2h1MTZfZElxY2pjeFJDOQ==\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<ihwaafuhxpqulznw@yevvmtgprd.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<bikuehtb@remr.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: p\r\nfrom: ceyzkvrtrywwjahntt@utfnjlmaenhbzrkxwg.de\r\nto: lurdxnno@vufxbxthzioynsl.de\r\ndate: Thu, 10 Sep 2020 11:20:23 +0000\r\nx-mailer: pIwATgrXX\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nc0x1CnlhSmNVSXFhSW0=\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<tirtxhbszsr@giyzwvzblq.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<fsaiey@rdkbhvvxahwfj.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: bYnj2VN-pCE_e\r\nfrom: lmyp@yjskbgfgwscnlroo.de\r\nto: kiuigck@jx.de\r\ndate: Mon, 15 Mar 2027 19:26:20 +0000\r\nx-mailer: VnGLRhzdjVYiwLuSBVp\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nNWtKQVJTa3hWOHU2MnFrVHM=\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO XEZrFAHvnFWDNnM  ZGP  8DN3.oMgyT1u UcaNvOtpbGT-.nlKkuZ4  XpoJ6QT6V \r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Client: <request_auth_user_incorrect> 'ZlRWNGh5ZGxoZzRQSVpi\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'VlNzWHJWTk8xcUJwV3BO\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'NEpubVZmSk9mclVucUZQV2g=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'WDJENQ==\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'TXlH\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO P3TinX6za PH0dVEs4N1c1Tp.wp  NZaGa7Hq  \r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Client: <request_auth_user_incorrect> 'eVl2\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'REJBcjRMMlVJeVZKZG4=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'Wk9ISA==\r\n'
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
fandango:INFO: Client: <request_auth_user_incorrect> 'NW4xTTVh\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'R2xjQkp5ZQ==\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'TGpSb2ZJRw==\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'cWNVTGVNX2pOdXN6aE01bg==\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'VjBaWDU4eXNvcEcyb09PVjM=\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'OWpqN2x1WGdM\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'SkhZZHhWRHFON1pjdzVKRjI=\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO 4Ki1NVxSNH1sA1Mo qvZbExM t16dTtRGByKA4PUjPlNj MAt3.TXC-64XL36Dn  0Qmuk  M9C R3ecUpnqO8tHBg  38m  9 LOI.w7  SaAb9CJ O  PUuf  K  aEPwRAtlZFAeP.VcCS  JvFOLTj6KFDkaH3KDWK  BIpL91pEdJ98z9B-Yv \r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'bnF1TUdveEdvakNWNEtoaUJIMA==\r\n'
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
fandango:INFO: Client: <request_auth_user_incorrect> 'SVdRS053a2pxTnRXSGFvOTRj\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'eGc=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'MWNP\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'bg==\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'dEw=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'TDBiZk5M\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'Sm9ZVkJEWnZWSFdCYTh6R3o=\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<nelyp@w.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<ukydjvakruns@wigonaoctdcliwqyvia.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: AR7zY7VsyL u5\r\nfrom: qmzjaexgyd@krwdoxohmnqrjavlsvto.de\r\nto: wyjqxytgmomhttfjupge@exzvsvfkezrhmryuch.de\r\ndate: Mon, 13 Sep 1993 07:58:56 +0000\r\nx-mailer: rrfVEcy\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nT2Q=\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO 1EI  \r\n'
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
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'b2VpWFBKcUVSQkIzTWd5dHpIdQ==\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'T0lv\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO u5FDZtBjzSiOduvUeE AG2a8VLXpiSrmROiU  UuU3zuBpWcEz3Ta  vFaBpFonNtEV2sxw8swB n2rwncLvP9RW-0.Nvh  F0-S.dB5rrth5LRW- NCJdpw  CJcqxlUb2Hgjw83i OLXq1XzVAwTE7ENuM  \r\n'
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
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'VU1NS2VqcWE3WA==\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO G5X j73A5ymCmM5JY.wLnCb  IVYMRKmTDeVLJwrdgpb8  K9hLM  Qy1fSy2BEw7mWMLsMD  vo5cFnp6 vT21O-cPly  OxmvmGnrDoCppbleji fIRu-Xen6KPXSfV6.f2v  SIGu U51J4u6zIU3NWFBbB  iyI  XKm4TxaAq \r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Client: <request_auth_user_incorrect> 'NFI=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'WjVMQmtaUGR1SU5lQg==\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'TmpIRjk0aWg0d1pZYTVs\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'Qw==\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'SjQ=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'WFB1b0lOcA==\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'RVdleGxUX2FxbnJMR1ZKaDZzdGs=\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<bzfmzit@hfaiiycagn.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<xsraabtozchklgt@x.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: Szf6HkEnc\r\nfrom: ezlufsnynhmft@wnkmlxvrbnhpflwfojby.de\r\nto: nt@o.de\r\ndate: Fri, 30 Nov 2001 08:35:19 +0000\r\nx-mailer: pXbQkCWlrjCdCEkOSp\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nVnpBRHNwRmw=\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO 4T9p8P.MLJCFS.oEg  YkONXbK0mwL  iC  hizLgD  XzMWb  SNCc Wr-hdEckgiK  u7lJuNnCxalxizoaIH 5qhNW8ZAhkPruP  X4O1SAaP1GKqL  \r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Client: <request_auth_user_incorrect> 'X0tF\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'dVhUcWg=\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<fhapzbfkrn@fx.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<lr@hzw.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: E0RSqoT2wd6h\r\nfrom: ocxqymgmhxgogbdzhty@mkiwzxakjmaevzyyrs.de\r\nto: zxfbvtjvin@i.de\r\ndate: Tue, 01 Sep 2026 03:53:54 +0000\r\nx-mailer: lqoXeWxEq\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\ndlNwaVZXUUNLUDNWCmp2azJW\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<dheymkjxlaaevoocl@mtetpstqfcvttyxfcm.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<jvhcakviwn@cveqrfkr.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: bTdclPaGyBv9P-wQ7r\r\nfrom: szoeqbezywjambqzqvw@mlrzqqeyefnzptdjmvc.de\r\nto: u@kzndfvqbyzzjpe.de\r\ndate: Mon, 23 Jul 2007 14:50:05 +0000\r\nx-mailer: HbfPDSKM\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nVURibGV2UndMM2U=\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO ypK968r.yEMz2  hGtZ85pKr3LQMQjx 4Z3QnWY  FwIf2OV8zSTn9HGuqu3Z  qpO14LxVu  BdAv8UyGf  h7zzYW-sSw7.jjkqiWX  Jv-y6KMWlVpNr  UdzFnZ DssW.12VJc2EBRFS .T6.  g2FI3HPt3 qUm71PDj7UMAK  ulia8-2RnhzGxfYX4f3  fS-GJbDjyuB2k.3U A5ovS  \r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'R2NRaVR1X0s1OGJxTVp4Ykhs\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO lu7cj28GynuETLal  0PtLypLhbGD aasKIjV04v9prdg C4GHbzDqUEqR0iLe  \r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: Server: <response_auth_success> '235 Authentication successful.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<qhgvofnpopnspxur@jrjbayybmuuv.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<pv@nxpchwuld.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: a2-8WeJNykgJb:37YD Y\r\nfrom: wsbf@gqnxsiictb.de\r\nto: ucoslwslhvmh@bcnepplqfsslcovnuudh.de\r\ndate: Thu, 16 Jul 1992 16:24:40 +0000\r\nx-mailer: fePXpmnEfzqouepo\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nZjMyVW9RMG8=\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO RcptT97N4ApKYgO0o  GSGGJENqm-Jpe9C SsgHgLKXzCvq  \r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<vdbg@ue.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<avvebeddto@hapacprkbseilooeks.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: bmknZ6\r\nfrom: mnzgcb@igmw.de\r\nto: irpfbefem@sfqppzwokwlmrk.de\r\ndate: Wed, 29 Oct 2036 04:13:30 +0000\r\nx-mailer: rxfWpPfHvgqcMZiGeX\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nOFBZ\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<vwuloiliqgutnkgybzdj@fmdr.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<ofxzrqvoljsfebln@bsiasqqmwvfjjhohe.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject:  Y\r\nfrom: lzdyueds@jvydrzbqznzieduswhsz.de\r\nto: tyqx@meduixkmpohfplzlczx.de\r\ndate: Tue, 01 Nov 1994 17:56:44 +0000\r\nx-mailer: fKoUlCdrldqsrtlYUq\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\neg11Mmp1SnVnRmloTjg5cA==\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO proKDbzM.oh8 4nnnk1bVJJjQEXTZ  .Y-A3a  g0hKNUHuH05Hy0DhIjK4 SspVuRg5  g i3M4fEPPGUURq R0xujrWq.vZD Dap0Imerud 8mHM8NUiPUcjjhc nByC9WIH.lF07  gZGaOli5T \r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'OExvWFR5M0o=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'SFpXMHEzag==\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<xlleilrevlouh@zmodefcuemsx.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<srhrmqzoeopd@xd.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: Q8LLILxQRz\r\nfrom: lymveuxorhfsxp@qnapqynzwzfdgrm.de\r\nto: tms@wqmyzdjxyrm.de\r\ndate: Sun, 23 Jul 2028 08:10:59 +0000\r\nx-mailer: c LNMlMp dIbHoPu\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\ncHVJNg==\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<ntnupzecshdxxrflgvhv@rfeucyv.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<wpq@sjcupfcdponfq.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: BV7w6K I-ot1FMjE\r\nfrom: mlzzqwmfvurkwwnuf@miobooakpahx.de\r\nto: ikttizvbdz@yvomvyk.de\r\ndate: Fri, 19 Feb 1982 05:10:46 +0000\r\nx-mailer: GYWT\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nN2VpR2RubGgzbA03TlVuemxEemQ=\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<yolqqkruex@yooareudfkvqedcd.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<zoozkbrmvcusliczs@asoi.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: j.-x\r\nfrom: bhmhhtefuyf@upzy.de\r\nto: rgikdxnhqjutd@opwdxmzalqlnbl.de\r\ndate: Tue, 28 Apr 2015 18:24:53 +0000\r\nx-mailer: S vyuqUf\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nVA==\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<qufcakympaberchivbbe@l.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<omcrltygerbgbdl@pheungtjbnbowo.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: Ie.:MqgtX\r\nfrom: hipdmppjjlezabznnw@qxhkds.de\r\nto: qbwnph@aahcdqopgcqdfldajdg.de\r\ndate: Mon, 16 Aug 2027 04:30:00 +0000\r\nx-mailer: DLeOfB\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nZVZoT3pjDVF6Cm5mWXhQdQ==\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO HcIsXPlEIqT-MF2S6e -fYzgqM  zmUNP  eXs3M-1M3M.gH.euq  AuvzKo4-IfhBihqLIh RkjDgYZne TjnExO5tNK1.6Abt0 kitovn0sF-lS kl.CBrRrJFte1  ui0mMih xrPrqHQJIPEHN  \r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'M1ptWkk1OUg3S0huOEh2\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO An4V-Eb9C16M KA53Rns572Xrow3TpP xT3tI-tq.NV9D602S m  TcaxLIzdl  I3DnM JtvV6db  pH5W.pA \r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'TEdhTlZ3cWpleDdE\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'QkJQWWxwS0oy\r\n'
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
fandango:INFO: Client: <request_auth_user_incorrect> 'SkJ2bEtIS3ZN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'TTYzYWZqckwxd0g=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'UVhEQTFhc3Vy\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'N3VmNUJxNA==\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'ak1UMld3SXZGc2xsTEVfQm1KVmk=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'ZGZFYUt3bmkyYjF2cUZVbg==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'a0FtU3VwUUZPS0d0S2dOWlNFbQ==\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO fjusqh. XceMk  FWQHiUH5e53T Bg2iZzoNl.n2q41ts  9c kwBSRPOocvNfi9  XWkC8uD7XV7 cUVrk3ekp4ntzFDM77L  386InDWNLFC EYHppvb2djg561T1R A8RMIJunDd0Lupk3t kYjd0.W.1YSrLG-I VW74PZgu6GlI  VPd MUk9gi.XQWJrGA3QHQz  M 5C9 HSFlWGlEoKf.XGcZA 41RlHtuyKZ9Q  rBEju1L5TzO-JJngOc  \r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'aW1POQ==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'cnBHR2h2Mg==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'ag==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'TEFkZDJkMTZyZHM4R2hGX3pR\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'cEswYVNEMVR1OE9ZRzc=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'Y2ZEZlJTY1hINw==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'ZkdHTlQ0Qg==\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'TzQ5aDJBRWRwcWdnQTJyVWEy\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO EP2RuKpJ451FRbwRZdHp J88N7S poj23rOGPNy5U AqGL83oE-q2tM7dEcY7  5DRjHHUGGZdDBnll WSPipjN9bQ3o7R5 9cO  ieHHsWPOaY0SM3tUdJXq  XB7iGp2cULnH69fc  eTdZ vLonnAJiE6 fGjy4w3  fS3jNg-gSlvYuLffw7U  BsegBeAh0tHs b EiJfF  o  At guGk-adFYcy cRK \r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'QkZFSTVi\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'bUZBZDVUNXBrSmVZ\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'cjlNR3NtN3g4MVp2MXBTbA==\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'RkFfQ0gyag==\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'eGd1Mnc5d0tNSQ==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'VW80SWFiMjFDa3BBY3d1Sg==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'NU9kTDU2bE02WUtv\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO nA0U-jWaKZm6wm Tqvguxu2wAlGnU  gtDc F p86  0oOhl7KZ004C  Wv  0iZ0wuaA81GroZI3UI  NjlgzH b6SoOhnTHRnxL7r  d  k8Kq  \r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'RmkxWHBadXRWTlJncg==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'Tw==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'aWE1WV9L\r\n'
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
fandango:INFO: Client: <request_auth_user_incorrect> 'RzZJVGs=\r\n'
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
fandango:INFO: Client: <request_auth_user_incorrect> 'YVZiVkREQTNGbExyTENjcTZZcw==\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'aXZyZXVHZERpc0t4a3Ra\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'aXpxTW9hMjN3Nmk5c2E=\r\n'
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
fandango:INFO: Client: <request_auth_user_incorrect> 'WURYclQ4d2RZQnI=\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO MKui5ExoRvlF3b4  ageZ77Lh  Ezc.p5X  F7YwvlipsrWlJLPDr3l  pJkLkp5  rH1zePI  tZgndVk3UysGDDbDe \r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'MFFobFFESXRwa1J3bDlySg==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'YmFxaE1EVld6Sjg=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'SnFTbXlWWXE=\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'NWRaMDN5MGc1dF9kRkFLWDM=\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<sbfquk@ltkzlxsqbp.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<pedvdj@zcgsunnhqfdzcb.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: Oks\r\nfrom: yygmgnjk@iphylajgpjmskqsvn.de\r\nto: cjyhks@lqcuzpkkperirocxobj.de\r\ndate: Wed, 16 Dec 1970 16:36:19 +0000\r\nx-mailer: GEGRbpPPVin\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nVnhMWGt5NVhYSA0KU3BuRXlT\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<kkapqbjz@nqogovyckhzjiindsfx.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<hzuocey@irzotizbgprslvcwg.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: QbW tn\r\nfrom: javrspnughmqlnp@jtmysnlia.de\r\nto: mkypghnoxjbjxpntthwx@tirywcbne.de\r\ndate: Thu, 14 Oct 2021 16:44:19 +0000\r\nx-mailer: zLGie lQjFIvgliFSqA\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nVWhUUmRv\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<mlgusgfldcuuruxxg@foqxshujvcjt.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<osqky@bbezmm.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: L 0jD_EUMdSzHUl\r\nfrom: lccqenrm@xoxu.de\r\nto: uobrpsmdugfjpyyfb@ochzpqqiksdfrg.de\r\ndate: Tue, 09 Nov 2027 19:36:52 +0000\r\nx-mailer: ZyejSnlaWEhWyD\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nS2NDUwp4dU50aVJPQ2E=\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO Uq3BGKPwV8e7lZoA  3vkD5ZDuNqWkzJmRIG9 ..cni..TFDtp7uVK51Pl 2x35FuqQBYvpwY fNUA6h7I3iIfYd6RZr JaHz2ctg \r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'YTdRZDUxNjVjRzVTS1BKTW1ub1c=\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'dE51MW1GdlpEYW5YWEp6Ug==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'cjV1Y0g3OA==\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'emhweXN3\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'ekxtVWNOTFUw\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'UDJhZFhC\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'RE52MEI0OWhDRnlWQlBzZW9u\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'aVpGUDF6MTVoOHdkWEdtZlpRVmM=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'eXlfS2p1ZWdNWjRPaEhfVnIxbGo=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'WW5SUkpXb3Jv\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'UmlvbGh1czFsWFp0OEdXUVBpQmQ=\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'Z3hSMTMxZ0w2UQ==\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'SmxaeTI=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'OUtfZw==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'UXZMM0tza3VNdXFVdmU=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'Qm11alU1RWNIQkF4Vw==\r\n'
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
fandango:INFO: Client: <request_auth_user_incorrect> 'NFNv\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'R0tJMVdrQkJ3UQ==\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<wfcaezedbnbcfxiqmh@nrcsfvblxiojofyeqkrz.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<rgpbybbrylnzqsrg@fuxlghjxcpnmmynv.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: h6k3gQdksAlM\r\nfrom: ikkrravokivgntnch@qnh.de\r\nto: wqkpla@uyfkleqqsbv.de\r\ndate: Mon, 24 Apr 2028 06:57:36 +0000\r\nx-mailer: MeYQSevGOTXyMk cQ\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\naA1rMlVLR2hiS1AxTA==\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<imyyp@mtwswxuqcvylvc.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<lyqwqgyy@h.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: IaWGv.5mvUxDDu1\r\nfrom: oiawh@xuhkkllwlilasfifafec.de\r\nto: gahzuldtgvmcqjyats@oitbwhnzzpb.de\r\ndate: Mon, 31 Jan 2005 00:31:20 +0000\r\nx-mailer: eZI\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nQ0hEWEpYSw==\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO j5IyBTIjCl-9D2B09u s3hqPPVo9EfJ5lhO  wOB  kvR5rtcb1R  C8PMXZsX1UwtkOV  rx2Q79b HbNv-9cIgM8 mKpwDBr  XUeY9xUNL18Y0 zCjky  vtMlHv20 sFQAq3 4zj9ZKBuD Fi897PY0  gVZaTbGkmY8MqIqW3 8lu-kLUW \r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'UlRQYWN3OGJ3anlIQ3cxdFg=\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'bEpjZWdv\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'ZWZqOG41X0xRQmI2STRmekM2TkI=\r\n'
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
fandango:INFO: Client: <request_auth_user_incorrect> 'RkZKQ3dUdHN3RXNMQw==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'RjdSZnh4V1Y5\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'VFhteDcxbkVFeEhIckhENW1wOWU=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'dUNCaEF2UFEwdHI=\r\n'
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
fandango:INFO: Client: <request_auth_user_incorrect> 'ag==\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<uhzyqkziujeeuea@rlgvr.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<iicmtdqmtoeklw@dswqlwqahczhkm.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: tC s6uPxzDt\r\nfrom: wbyivqguwjrh@tocdfigawhfwngaqkkn.de\r\nto: pmtiqwhbnstkfeje@ygaa.de\r\ndate: Fri, 20 Oct 1978 16:53:04 +0000\r\nx-mailer: elAKq C\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nDTk0ckI1NGY=\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<xgtfajttt@zlhfkbbnoe.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<ysoovlitpu@sjombutvuuqz.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: Zxfi\r\nfrom: mlymhirhqbbzo@qcagxcwmanfwbgwlno.de\r\nto: fdth@adwyf.de\r\ndate: Sun, 04 Jul 1999 21:29:33 +0000\r\nx-mailer: T\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nNjl5TFk0VWVN\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO Coft  ytK JHNa99xVqbgB-w5xYvA xDbhXgSttelbDWQgzb  qB5c  Pf6VSZJc3sceIY0CKnK  JtFIr1RTp yLyCPIIPm4ulzVi2  aPjQCEHYIHx15v  PSmrFZrA6L9aLGnN2W NPz  T \r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<z@t.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<bbabgemvaeourujsargk@fhiexxe.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: U1vzvvQVh\r\nfrom: nwwoydxrahxuwuls@rtvxmqlxigurgqoagr.de\r\nto: gnhgcxjpcejk@zltwinbci.de\r\ndate: Fri, 27 Oct 2028 05:00:29 +0000\r\nx-mailer: fivnOBkXLV KBVrAC\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nNndXb2xlMGpnZGlaaXdHUg==\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO acs8VBmgEDkLcfs7bIl 6Hifm-c-XHzt3u5AU7a  2bs2VW6MO.vkR7Ll9 e-hqAW kJSfypPsKc8Q 8Ya3HMwfu---h1ZoM  YEu  H  NtEx  sTboFPTuzt q9yxJFUcMjzbdJD  99jRl  GfFPeRtDYd7sIRIc OaZJn2B3CJqIte  xkftNxzvxz  sG89G6cscdY9g \r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'VUJ6\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'UkVxemRWNnpHbUxMSVJUdk1fcw==\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<itrqmfga@igngpws.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<eav@ddjdsewxbb.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: rsaf-XXmwjYSLgi\r\nfrom: lvlbgxlruxwgwrlwvozu@thxzctggfcfj.de\r\nto: wz@turohitijwogubx.de\r\ndate: Wed, 27 Nov 2019 12:04:07 +0000\r\nx-mailer: jwqC\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\naEJOWWxBN2xXTUdv\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<boiyurpszbit@iywugpeg.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<zyykzube@kbbuemly.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: G0r.DtYFbf\r\nfrom: uhoatkwnhmsmpnr@inmbqndsai.de\r\nto: mcnuowfnqihyy@jljhhgytgls.de\r\ndate: Sun, 05 Dec 2004 20:40:37 +0000\r\nx-mailer: OkyIOGVcjpyViWufntY\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nTlNPdFdtZ3FqTlR0dmdK\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO BzVYvbndh  JEfsETWa-V  uO1g-2BX-Xc \r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'RDBuRzByRA==\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO I3  \r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'czk=\r\n'
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
fandango:INFO: Client: <request_auth_user_incorrect> 'dFI=\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'SlV6Q2FWWGdh\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'SGxsdzA0ZA==\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'QWM4Vw==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'YkdJUlNxVU5sZUdrZjNfQm5P\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'UHF5dnA5NU5XTW0zWUZRVA==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'TDl3Zm1lZHpWdzVK\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'M2YzaTF3ZlRUYVI4\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'X0kwcU4=\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'ZzRBZWptRkRiaVVfbjdD\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<buisqsiikixeq@poecimxdzngqkxaxldcc.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<cdrsrfjrzvdj@yuj.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: EHdoxvcxUDteNf\r\nfrom: uaiyvtwqugejonnpgc@exfqjodmymhgszb.de\r\nto: icagfsut@jvmbgugjofbo.de\r\ndate: Fri, 17 Dec 2010 22:41:39 +0000\r\nx-mailer: MQEqzaJOw\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\ndGNSSTk2Qjh6Zw==\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<kjmgxbysmxlagpw@buresunywmcgbefho.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<mt@wjswzitwkrhoyfhcpzj.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: D2lcq0Azqgw9wuneL5\r\nfrom: rtfteucqgl@qnih.de\r\nto: kijjmsngiaslgyj@gcqmrubvg.de\r\ndate: Sat, 02 Jan 1993 03:11:29 +0000\r\nx-mailer: IlznfxOwAtfCL\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nOVc1bFJDY2lXdlE=\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO qBAUcYnPny VdRTx5FpCeJ6kX1DCRi jPl0pNHtHbS3XQHd IcN  pd MAXyN5HpnEeg0 kuHxGGb0xUo  cLuHFU TOx 7kOEtyx j4ePTKyZA4g4y YyMkr  BeGnxKQWIMRIzqkpjzVt  8HZ Qyw  AvQj  \r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'Sg==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'TDdqQjhVbQ==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'cVBKWlpFT0RPM0ZJ\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'M0FWYnJ3a0RyV25MV1dRYllDWg==\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<wzzgvcn@swvomnvqzbcxqme.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<n@rcrwasyzbirqoszxyose.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: IDNDqN .j7I\r\nfrom: ftybkmmkzslkoakdtv@tqgndlrjwd.de\r\nto: aehaeztlqnst@w.de\r\ndate: Wed, 09 Dec 1981 02:08:59 +0000\r\nx-mailer: psNqqqDaIaIg\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nWlhUZDczTE84NkNTWFFKT3U=\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO MWhFZUO4SBJbjd  \r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<xrthmeqldpwhdipnz@mlvduinhqkxdedimuw.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<hkixgvpzkluzlkmatus@afgze.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: u3zC4c\r\nfrom: py@smbndyyvrdfdfckivetd.de\r\nto: krbwhvabruj@ieagecow.de\r\ndate: Thu, 21 Jul 2005 12:26:42 +0000\r\nx-mailer: UuGAIYsStjnM\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nSmZKY0cyNGI=\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<osdtryljnk@wkoyq.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<hxayktpohb@wjieqexrdshrrvvrvym.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: y1Sk_X7A\r\nfrom: cnonzigelbm@ebuytte.de\r\nto: ndznwnlyfxacy@mzbkgpkclzmrk.de\r\ndate: Thu, 13 Aug 1981 00:45:40 +0000\r\nx-mailer: m\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nblFNUkxQRQo=\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<fsbtgeubpjpyftc@s.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<quwsadmbqiuyszgluczp@cygyegyrjrbyrjsmqk.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: dhAHGdvqJIlSJ:\r\nfrom: qrbdtcl@gnrr.de\r\nto: rbzhlz@cqrarsdodytisfpky.de\r\ndate: Fri, 04 Aug 1978 08:30:51 +0000\r\nx-mailer: cWeMrmhYRdvORcSpT\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\ndw==\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO d  UVxnn7F  FigLkDbm  HME4g.2AeX  TLwJw-MfljV8N  VkKwtdhwD02v yjv30bZo 9vjNcF01XGmp U7f2h0nGE6xNFOD-  wX8kSFwrjY  PCV4FOylbdqhZ4 c \r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<ymhkc@hkabpujqlavxjrf.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<d@baybezad.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: 9xj6Ux\r\nfrom: etvahzfygeqipbsmkm@luuujsizpqiclgknzr.de\r\nto: fpghxtjbxdly@jmb.de\r\ndate: Fri, 18 Dec 2020 09:12:30 +0000\r\nx-mailer: xakeyAGUkL\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nSmtxdWhMOGVC\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO k4d  QYNCT u \r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'cnk0UGh0RlY3ZDg3eEo=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'SWdBclFW\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'Y3Fkdm5LSWhrYVFWNkNoNjQ0eQ==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'S21GekV1Q3l6QmtjVmFJMHdoMnI=\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<zvukjcfzj@aczkbzvbainfsuqtysn.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<vzomzoaqbxmvtwmz@vealbktbiim.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: PFIHrLi3gqfA64T9\r\nfrom: clxvjfjkygkoslcxazs@aihsvanxyfyjlegf.de\r\nto: igtg@fd.de\r\ndate: Mon, 21 Mar 1994 00:46:52 +0000\r\nx-mailer:  GoEjwtDzjwehMraTwn\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\neWU4dWdGeVZEY0t0QmpWUjVI\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO P.2Dps9  9TcP UAPJmPdJ00W  \r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'XzJQQm13Q3lrWE1DYk9LeWFMUw==\r\n'
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
fandango:INFO: Client: <request_auth_user_incorrect> 'czliRWl2N1VmSjk=\r\n'
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
fandango:INFO: Client: <request_auth_user_incorrect> 'enFLWTI0RW9GT1lYQw==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'dnZIckthRFdPb3J5S0c=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'aE5RTmpfRWd0ZWVC\r\n'
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
fandango:INFO: Client: <request_auth_user_incorrect> 'RmRQbXhWMmZrYWZFeVBmYg==\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'a2NvS2N6bkx6TmRfY0M=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'WmJrS0p5U3c=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'V29lb2hSeDN2MEFINDc0Xw==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'ZnlqbXQ1U3FLQ1RYTlhiM2s2aQ==\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'ZVZvb3pNd3c2dHBxWG1HMUc3ZG8=\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'NTNIRnVDczdKOURMb3ZNeDB5RXE=\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'X2pX\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'elVYb2t6S3QxZm9CX3Y4eVZI\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'clNiUmxjWg==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'WWNxbHQxWQ==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'VFE1Wl9yMWxyM0dmeXVOZzR3M2w=\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'YUhMeHdOaw==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'aE91YWpSYzBUUg==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'UUprYQ==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'VEtRN2k3Y2tTU3J1aVZS\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'eXFVOVFqcnExODRfVkN6Tk8=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'RkdTNkk=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'RUN3S1MwRjNxbmRpNVFFcUQxNg==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'S2pzUXpsc1lJdQ==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'YlVfelpMZg==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'NGhUZGRk\r\n'
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
fandango:INFO: Client: <request_auth_user_incorrect> 'X0ZkaU9EWXd5QWU1Qg==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'UEtScjJZTkJlQjZEOVNlOXNvODE=\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'MGFOUk1Fc011cGdk\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'ak52VFBfckE=\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO c5ZE3  Zlfy3pnGU9sBs FvGlu83Ae  legAVGL6 SV9S6-x9ceInj8D6cqNj  UuzzEtQuzNrZO-IF0  CmCjGAMorB6yN cBmf.3LHTZZOUXoVS Ipcg6s9-jWc  hqcPKukB4j8AEXKS  IK0.UHXQDFHz Z22z HUcr4BjEqo7td3cUhpIY A1wZVhSinn PwDY1 m.ynu3kVeXFv9kyS1p- \r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'Ug==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'dzM1QjVDWGYzbHI5T3RXTXRfcnE=\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'dGFIb0J2UGVTbUU=\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<ttnfkfoajw@epdswmqljymhfsux.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<azlvsrwje@djmxnhu.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: aTT\r\nfrom: zbichaechtotrhbtxk@rii.de\r\nto: pmfcajfmjvlih@owcyfmsatz.de\r\ndate: Fri, 23 May 2003 07:04:18 +0000\r\nx-mailer: iVrk\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nSDN1R0NmMkFwaVVUV3NJWmxo\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<njxjah@xongqjlinfumt.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<vjdqtdyioegjsh@yjlr.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: stikAFxC:4l\r\nfrom: efyybbluzoc@mrzgfzpejsnndifkpdk.de\r\nto: oxjhutv@scyikgkcavrv.de\r\ndate: Sun, 06 Apr 1997 20:33:29 +0000\r\nx-mailer: LiEbmuTX\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nY3RmCkRRDWo0QVo=\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO M tt9AllR4plAcuaL  zp9BmYd2y 8-5n4KN3J4KoVZR39 zQX0  5RA5Oc iY4 YO 51V8h7 DY4BWaYoxaV5  q  D xILELN2unj2mko6Ur  HwjZ  Rrjm84YJ7Duh  PPE2q7HCQZo6kArdmN  bkgca0P2znSTyP5P30 nuS  gA8a9MbgkbhRCQG MlLl2yHWBq-F  \r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'SzFMdnFGaE1wSQ==\r\n'
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
fandango:INFO: Client: <request_auth_user_incorrect> 'dGNHNThhX3F4b1dtMlA=\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<miqmh@rnrpakmapieudqlssos.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<gfgsejzeukxkgkp@cslziiulecbt.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: uU7bge3.0\r\nfrom: yvvnibggtmhnrpwicdo@iorwqlr.de\r\nto: prtbpf@mzlyjyskcjhubpv.de\r\ndate: Tue, 10 Jul 2029 08:27:56 +0000\r\nx-mailer: hExWUoSO\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nOFRuMUt5bE96c2E=\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO tuLu6LZvroGA0UtDMloA  ZKY6DC46N N  GtBjxZsW-yHvfaH3pcHx oDmXHb6j54atouN6rD. j 4p1RMG3eITV3a Kkcs3WqbMq0ICT V.Wbbe BEtOwbYeI  zr6 \r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'S1A0TldDU2N1NERYbjFJOQ==\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'UlpVNTN5\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'VkVaWWdHSzZ0\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO g6ggZzyYv6  6yldE1LzJrG GojLph2  4tyEMC-Jyo  eMu-sjM8nckcU OXk zypp8b9BHFD5UrGi WvQ l3eKiaNgbuSMWpux QIT6-Dif6gH EQFNlb-JMzlAQGo  .SOQw2lVn6aAo9EeVV9 y5oKtzjb7IYp3  Y a2dU0UvV6Y9  CZWbeijvqUp ObpvP0pjupPmNg \r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'dzdqaHBibkY0N1BCQXRQT2Q=\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'aA==\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'MHFITGZwMFpISTFLNHo=\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO f  lLbcpWuU7npCYm0Ux wOx  -SAaGGqc  pozIJ0m76HSod8tUlKnx i8DOLexW9cRsuo  q4  ZGxm- Mam  S0R 0nGN WDHrMlYXaFuKnm z9iwfyptn1DUcWRFF \r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<ougwpce@dprnrkfniljvursccpeb.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<rrx@cuaxsxryct.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: aaCkCNQ\r\nfrom: fbdihupazcer@f.de\r\nto: ofwsdbrcrrxu@oxjywahoyz.de\r\ndate: Tue, 25 Dec 2035 10:17:24 +0000\r\nx-mailer: peC\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nQ0c3OXlWRk45\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<cxjaaitnye@hqvxocmlbeygybjzjcy.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<yrihtnpfurdw@glwuxwsvvei.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: fQ7itvCAuxPVRGb1\r\nfrom: rqnzphr@x.de\r\nto: kpufvfjewuvhxgjpehn@phwqcrm.de\r\ndate: Wed, 22 Sep 2004 02:18:28 +0000\r\nx-mailer: OfQqre\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nZ2RsczNDRW45TXdpdw==\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO c Pd.U pPz  hUSKGTEnVXVjwaEz YaS6 ZN9.tI9lpj.EOEH6-el  QAhrd6ybE-Vez0rjlL  HAIb5VRbbWaS PZE.n6NqAWffObE7 LKlVwJDgZTabzw  \r\n'
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
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO o2whGz4p-iUwPJBo xj1h6  L  sIT0.4Gb.0oGHMgQJ  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\namhENWxGMTZHcEFxRm5hQ0xFX1M=\r\n334 UGFzc3dvcmQ6\r\nSUtBbVdpSE9hSVZScQ==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<vaniurjsmbtgac@bkqtcjf.de>\r\n250 Ok\r\nRCPT TO:<hz@uuqf.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: 4di8.vzT02P\r\nfrom: ael@cifagajtwevkxzqg.de\r\nto: tqhqquvyxeyimewix@wjvglhyffmepshlga.de\r\ndate: Tue, 18 Feb 2003 04:32:43 +0000\r\nx-mailer: apVg\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nMg==\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<pucjvkazlbedrturgt@dcvfk.de>\r\n250 Ok\r\nRCPT TO:<dlljsgnkbt@zktbrtodrnwhoa.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: fTKlYOWXg:Ojou63\r\nfrom: pkorhqfvdcyeyehnyyqp@zuqtcoi.de\r\nto: hwvfwigqk@pogl.de\r\ndate: Thu, 24 Sep 1992 14:12:32 +0000\r\nx-mailer: DPDVY\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nNnJQ\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO Ii4HHYqUzfrYe0QjIq  0ZockNbq7 xluCoiMo uYw4hDkn5cvy 9gbwYGX oPWXPbvlmJkSUmBV9-fb  msF ulv-nvmWvS4vnAmyrZt  N6PIjndJ4J47 Awg6pLj09OR2IglcCrm  .FQvKgUHPV.A17V  fgNjhRD0fAWe6MWj8v sgvy9-CZ.MKJR  D-iK7XTQZmW5xgyV  89lUPfGOjSZBVr  aqaThDW3IdK2qYbv b0p6B7B2IWZiem1136  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nWWliMENhWHBLMVdjOTBsUnhaTmc=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nc0I0TmI2ZnRzblQ=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nMkNLS2U3NQ==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO MyIbXwlM3qDfnbvx-FI  O9edlI5o9GuakINcNQDN P. eJn R87aTKRge0ubJ  U8AfBl5rRRk..zrCysQ 7MLCc-vegxo5.Jv LRE9398l1In MNenRV \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nc0RGSA==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nTXRzN3NJYnI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO hRPdwqes 1r7QKIZ8jzzZ  lEX9bVdto1 a7xOnailwNeYUwa  d  dbEgq7ccWk  7fpl  e1ugXyoP  ms.PB6yXYSELCyQFr6L x5yqU0fj5Pw  AGXBonovtw  7TeobGgm  gGf0L  4Xp4SJs4Q  dDR2h uQASOAZ7cbY1voc 5Bs316huOfMh-  6-1y6tcSC \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nTVd2U08zOVlqYVFSbVBGcVFVNw==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<qxlnzhrn@u.de>\r\n250 Ok\r\nRCPT TO:<chjhhxxiaiebquo@gzbgow.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: 65jb1-9eObog0\r\nfrom: sajpnlzgyyac@mgoprbqvncpqtzwh.de\r\nto: adcigtcfg@uvqaklkmcybbfitosi.de\r\ndate: Wed, 02 Oct 1996 10:52:16 +0000\r\nx-mailer: Q\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nQTB5RXhkOFB1cXg4Z01WSkg=\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<ckaqpmvdasmbu@osxi.de>\r\n250 Ok\r\nRCPT TO:<qipxejlpgwzvmc@aed.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: 10V\r\nfrom: tnrafskoolysjaqm@kgrcdt.de\r\nto: ixrlqewypcgaxnbn@xsgnxs.de\r\ndate: Sun, 02 Nov 2036 13:42:57 +0000\r\nx-mailer: uLss\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nZ1M1UDFDZUpDTzNKVm95Q3ZSTQ==\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<zcl@zurnrk.de>\r\n250 Ok\r\nRCPT TO:<jtzlynhmqfkvj@hqxkquqvpaarsvmgxi.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: dKmCHjVAK.DALXl\r\nfrom: hxw@ncteygpmhnvnwoidwirg.de\r\nto: snomhxtczymkkpcjt@rtqpzumtdogzsxelcnd.de\r\ndate: Thu, 18 Jun 2020 14:52:28 +0000\r\nx-mailer: vapkZAioXdRez\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nQzB5RDIyNDJM\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<huz@vugiacmna.de>\r\n250 Ok\r\nRCPT TO:<huvr@tqovgwxdcq.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: LWlebwdA7iKUbvNh\r\nfrom: ybxshqkpji@qaqlqu.de\r\nto: xuoxcscolvsc@wucdljguwfdtnkod.de\r\ndate: Tue, 23 Jun 2026 08:22:54 +0000\r\nx-mailer: jUMpaxWlEwSfs\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nakRCVDUyTzd0WlQybzBnWkc=\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<xvh@g.de>\r\n250 Ok\r\nRCPT TO:<uqjfsjsbfuvxnsrvewdv@iifbbwkvdzhhuujzozvv.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: wEnvx4WOTFKPjW8n\r\nfrom: pzemdvijcpvxbmq@yqihcswbcmgqxeq.de\r\nto: lutd@xz.de\r\ndate: Sun, 26 Sep 2021 18:56:00 +0000\r\nx-mailer: EmPyCYVuTPIyGFZA\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nd0hP\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO 8I5Aj0NSxh 70bToiVHL-XSNg  J5f6P 5Z15k.Mz1UtQYguDhJbG 1Q-XVOvHXS-  0.pv6CIvhdGKdwsf-  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nUlZnWk9Yag==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nNXVEQWJRVHNrNlQ0\r\n334 UGFzc3dvcmQ6\r\nMA==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nQVFrSkR2SHFqZkNPRGpzbGNYM1o=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nNGZCVEI=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nZnpxMVNxQjJHS24=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nWg==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nb1hnSw==\r\n334 UGFzc3dvcmQ6\r\nZEwwaUxSclVZODNFNg==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nWWFLR0VHSGlTeVhUNEk1dXd4XzE=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nY1BrN1c2bWZXZURLaWtlY0RJWg==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nQXFhc1MweFo=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nVFJwSg==\r\n334 UGFzc3dvcmQ6\r\nVEhzNzlpaG9QajFTdGhqZA==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nc25hUFNLMjVHVmY0\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO kObAd  I3qBN  ZUOgWQtGrmVdOepOo  7cOdZZvGUMb93o-  MsKJifWXWF  SVea2M  Q7exS-R.rrMboGt-GW KXfzHCQ3r.AQcM kDzpQXSe1 argYsOt10gqt9hTf  EF3Q6Eo 1iRx pc4xqOc ybX1rWbkYTQtHGYI0A76  02bHN6T0vhLmlS3-tb qPjaJEJQJ-ivxF nFLppoemxnNieF 3SlGW \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\neHBNNDFhWHZlemFFZjE4RTZF\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nbWtFZDFSTmp1bFJBcUY=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nUWtKd1pmakVDd05ueTMwWTU=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nVHJOVkE4NUoxMTVnZQ==\r\n334 UGFzc3dvcmQ6\r\nMg==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nNHNDQkhqNWg=\r\n334 UGFzc3dvcmQ6\r\nWDdTbEE4NWNjWDha\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ncWtiT0owdU9qd3hoOQ==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nVEdJeW1Yb2xrY1NZdnpaZ3FaVA==\r\n334 UGFzc3dvcmQ6\r\nSFozOHpBRHRuaFM=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nUWtSczVKWUFsbTZj\r\n334 UGFzc3dvcmQ6\r\nMWhLQm5JQmE4cQ==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nWUxZRDN2NkNoVHZwYUZkNg==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndVFiRXNRanA4SXU1\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nUmU3ZEswN0JNQzVlSDU=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nU2RHSEtERWZ6QThyYnU=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<zjprqqxyuvqg@rexubymbwmfwhrqhufu.de>\r\n250 Ok\r\nRCPT TO:<nemgapggaspmtqky@qdmzx.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: C6Au15SNJ603bC\r\nfrom: hse@wtsptphehbbn.de\r\nto: nuktsvqtvqns@njkrfteswomgeig.de\r\ndate: Sun, 10 Dec 1989 09:13:39 +0000\r\nx-mailer: jBAsiGjFXvRlo V\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nb2dhZw==\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<jlsxzbbo@kqnvxjyxj.de>\r\n250 Ok\r\nRCPT TO:<jmtfaawx@xxgxjfmvreydbdnldru.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: 7SEgiwTuNROfcr\r\nfrom: esvkpmwfaizfy@vbbmjle.de\r\nto: wajgzhjwolyccnbguvek@ceuxzfiyjwo.de\r\ndate: Tue, 29 Jul 2014 16:35:22 +0000\r\nx-mailer:  wft\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nWWZTVEFNRXp4VUhpNTh0\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO CbLOhih2ic d5ugmq07eloAqJvq7UZ  zgKrX uDDKnT-DY44XkiSnoyhi  L9 1Q5P2j  M 1XfTx3Qk  TN-xcI8fXSQenYC7MvQW jAj5wAZH3L6wLp-iCal3  gcDE7  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nb2RiU2FOT3Z1\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO iXF8bH  nmT jVFb npnnqoK2d bUdiQiPwmCV2  4XYGW  j3i6hp ILRn  Hzzb3-4zNCMOE Lh7PlT ikGRgtTRgdyJ  ZkEEHyE7nQWsZ  Na1z Vup3xA.96kJ z-kh3dFGqwwC7X s81AIvIRNnGj1cCUw-  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nUQ==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\namhpdFloSGFQd2ZEbndz\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\neA==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndVFR\r\n334 UGFzc3dvcmQ6\r\ncjFZZEtYNVlvRW4=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nc2J1bWVoM2xwQUZTOHM=\r\n334 UGFzc3dvcmQ6\r\ndQ==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO 1g7S.Ik  Euf tYYdHq8w.LJUEV5WT1A Ia4QC2KgqtGodEHV  7kB9xid g2mjY33S p3sED8Uy  s-W3pJ AZ8ezxYhQludxy3vua9u g9  DGRG  Qcw58Amuw5RUyZ7H  X9Cs  BWxRY.AWbqZQpS3G3 14B.05b Jj7L rNj0ItDT0SMIjiH-  iBJ-6O  - \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nb2U1ZjZLeWtwSXc4Tzk3WFZITFQ=\r\n334 UGFzc3dvcmQ6\r\nTXB0X2FReXdoY1ZjOXBiek5vRw==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<avzv@mqfzjrjsmyo.de>\r\n250 Ok\r\nRCPT TO:<zyoqitywcydy@fdmokfjatkitkzqfxrrg.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: 1x.m6hpcgJ7b\r\nfrom: scw@gfhkrbidynthqo.de\r\nto: auiyez@zmspsowargopm.de\r\ndate: Sat, 27 Jan 2001 07:46:30 +0000\r\nx-mailer: bvNdoiFXRLlmCBOP\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\ncFJmc25BVzZpT2hSUW1lWHhYSU8=\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO 8AtI-giGV-1HehG2 RnTDeDOLv.e5  vc1  eKBN sjft2ZXNnboO58lESC  0ODeywnEG43 7WS9uYvKN10  fTAyU29xWH KdqTsZlx-V115oDuqdgH gxqcmsLQ761u mP lRl53BLSVsK29N4 U1  kHcI4vuX2NcSCBpsGOJ9  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndE8xUko5djRJS3Zi\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nSjVzaF81WGNhag==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO niFNliE0QztDYTsPfz M6-I rlPatc gLLZD1jRhuIjnCY5Ic  rZosRf  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nSQ==\r\n334 UGFzc3dvcmQ6\r\naXVGZ3JjcGdGUmhMd1d2Tw==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nRTBjbzBIdXhlaFNwSg==\r\n334 UGFzc3dvcmQ6\r\nWFROX0E=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nUXRzMlZSblh5VEl4QU5McXli\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nZll2dE1POGxsSTdfUDE1OGh3\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<qzrd@ffdkyez.de>\r\n250 Ok\r\nRCPT TO:<ewkixflvj@lnhvzlvppcemigfant.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: g7p\r\nfrom: mnqlcarmcubcwpbd@l.de\r\nto: lvktntoftupmhltj@gvzpaodi.de\r\ndate: Sat, 12 Feb 2000 17:30:47 +0000\r\nx-mailer: QrsGDCfUWfFB\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nRnpWUHZVaUN0YlgzWnh0\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO .3z  0EsS27ESHbv  F3h HoTi0pOd 8CvJgqWRloNLatDJ7p  YDfb3Qc9MxTcgZFMdvSr  HkiWP-ZVQIAWvSjMHV Ik rsuIcsWOG  nc4T6eizy400h1X  8IC- 8lu8N8l3Ray1XQu  sK DqE40KvVIE2Tyos4RW wKc7tsC5rdQHrq  zKoBCI RUphPodgGmo  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nZDl4T3VBbFY=\r\n334 UGFzc3dvcmQ6\r\nQWNUclVQYjZfeWI=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nalFyNVhUZ2Q=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<pmkokevtbgz@quyznqmolujtcdltbn.de>\r\n250 Ok\r\nRCPT TO:<waylzpszqpdztgwml@xejs.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: wuLbXkHn\r\nfrom: lnscm@tighmymarvim.de\r\nto: xhoyj@umohkivfjdvctcp.de\r\ndate: Fri, 23 Mar 2029 10:39:59 +0000\r\nx-mailer: RnpZwMMw\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nbGtEZGl5RlpxV002eQ==\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO ZzOQLPAma  .Fw8qYAqT8TMbM0P  KDwDhL12bG  PmsY-7ED9cwKpnwZ48w  3bPK9d6fa5Oj6yXQCN91 l.3EktqnVkyuj1r  uxN4  .wlwivkPNnpkygfCQX0X yHe Vv5aJb2YDuY 1lmmJB KqM5HFwzP  BYOhYRjSOnmhX 6X RfYGvAuwz  NC8S.iys3fGg OYizbRwgjPj -uyBi WF \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ncV9yVGNxZDY=\r\n334 UGFzc3dvcmQ6\r\namhZalA0b3hySEFF\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nQ3N5WllHVjl0aFg=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nOWJOdTI5ZDdmcGkyQTBtQnI=\r\n334 UGFzc3dvcmQ6\r\nWnFweV9W\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<ddamevmjftcinlzu@sntiard.de>\r\n250 Ok\r\nRCPT TO:<xakyxvrknw@bhpqkhkpfuhfjm.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: hsFs.m07xN\r\nfrom: dgaicihcvyeo@bfiesark.de\r\nto: ggdhvezctxwemtwnt@tgwylzegeyptqsvjp.de\r\ndate: Wed, 27 Mar 1974 06:46:26 +0000\r\nx-mailer: qOLffoxJZpZDRiqpbuG\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\neQ==\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<bg@bbkfcexavvnioofq.de>\r\n250 Ok\r\nRCPT TO:<zqdqmzhldlxbpnums@tyqkxgxr.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: I:\r\nfrom: ycwf@rjyldbqwcoebcn.de\r\nto: pg@qdciko.de\r\ndate: Mon, 24 Oct 1988 07:45:14 +0000\r\nx-mailer: TZWhdVzSedYGn\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\ndkRTREJnWVFmTVpxMU9l\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO oA.  r1LnEtm1sg.XPvV  vL  42k  iQA oiJkyqdWB  bSYyc4cXjIsD6KuY4  181KsENR7emnJ0Q3v  7vVPWuVWNUgh 7F-ZHVx..wcaKyEwRRUU  68a8ML8fbD1SqE  Oi-G-iJGT wIDyX5mkyRgYrxkKG  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nY1NUdlJxeWxvYVhZbnlhNExkUg==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<oozalnesoamdzxifqmsq@djjiwxfzzdsfvlt.de>\r\n250 Ok\r\nRCPT TO:<bzhb@segzxseskgmbfuj.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: rsoSHq:12BPBQOp\r\nfrom: ei@gm.de\r\nto: oez@hek.de\r\ndate: Wed, 22 Nov 2000 14:30:59 +0000\r\nx-mailer: CUxCzbZZAwKeHU\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nbkZyc1oyWTNHelEKdDR0cmhsTQ==\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO a37NalC  V6cNILtG7oQ  OHyzHz3-oGe517QcI3b jl 3n 7  QHsg cy6wMGjgeRfaXXJ  X-voTUKH -D yvfHvEUXgB  2JPYTUOY  .CHN5V8-R9Qq3fv5s fNTUSYd OQz06fyV21KHwlncrX2 78t  41KTwCJEonAi5MJXRVC  vVQnrZzzd P-2rPmj0h2  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nZlpsU0hKYzhTcWdWTGtBWg==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nNg==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nRWFmNlR3\r\n334 UGFzc3dvcmQ6\r\nNU8=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ncHhvMXljTHU5Z3g=\r\n334 UGFzc3dvcmQ6\r\nck5mVkdlc3NTVFQ=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\neEpwekw=\r\n334 UGFzc3dvcmQ6\r\nTm5oWndNZ3E5dXp4ODNW\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO f .rXG7ypKPyDW6I36 \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\neVRWS1ROdWJWbGU=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\neFN6cUdYVWtFZTFJcmtRUFNOcA==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nMw==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\naVpFTnJyZXlHVA==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nR0tpTUNEQUE=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<qystyzvnyuthl@xtumvsxy.de>\r\n250 Ok\r\nRCPT TO:<tliargtlld@ewyciytmhcex.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: wJC.Diga\r\nfrom: kiuun@ygat.de\r\nto: lsubwqz@jvpicrfot.de\r\ndate: Fri, 18 May 2035 11:15:04 +0000\r\nx-mailer: wWZLvAJmwpajVwlo \r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nUFZNWDhn\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<vyppstmuwewwhi@acqsnwlhbi.de>\r\n250 Ok\r\nRCPT TO:<gyb@aktauzyphmtjwt.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: IiyBlhmFiYRGchKFKY\r\nfrom: jfgecc@pkuwhbgbryxihuqhci.de\r\nto: xbximncpu@eslmrudvyrmvbusyy.de\r\ndate: Wed, 01 Jul 2037 07:25:33 +0000\r\nx-mailer: UvBaVjuryw\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nekdvMEszQVk1WW9Md1k1QQ==\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO pDDVNpYm.Lat sC2R2SgmJRbW.JZ5 40-lR1w US2HbPBbRaIXc5v- ra- 6Xe9k5dxmEWi 7x1QWwYijU. ACMIF9FIvrsLN  1Ip0kHvpwtp aqx8L2dIwXgqXtpXy Erj2uIvq  ARK5  RHOAxD  XEUJmpjehcpY8HQz7  UrP.gYBB-zqG-XImz6Zf 65Koni 8Fdi JAijURFHsvaJSgf7a5S e1wM1DxLE0UCu7FJXC0  jz5sA \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nb213RlJqSFJNVw==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nM0dlYTI0SXBMc2gzQUZvNkc=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nR2h1MTZfZElxY2pjeFJDOQ==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<ihwaafuhxpqulznw@yevvmtgprd.de>\r\n250 Ok\r\nRCPT TO:<bikuehtb@remr.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: p\r\nfrom: ceyzkvrtrywwjahntt@utfnjlmaenhbzrkxwg.de\r\nto: lurdxnno@vufxbxthzioynsl.de\r\ndate: Thu, 10 Sep 2020 11:20:23 +0000\r\nx-mailer: pIwATgrXX\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nc0x1CnlhSmNVSXFhSW0=\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<tirtxhbszsr@giyzwvzblq.de>\r\n250 Ok\r\nRCPT TO:<fsaiey@rdkbhvvxahwfj.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: bYnj2VN-pCE_e\r\nfrom: lmyp@yjskbgfgwscnlroo.de\r\nto: kiuigck@jx.de\r\ndate: Mon, 15 Mar 2027 19:26:20 +0000\r\nx-mailer: VnGLRhzdjVYiwLuSBVp\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nNWtKQVJTa3hWOHU2MnFrVHM=\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO XEZrFAHvnFWDNnM  ZGP  8DN3.oMgyT1u UcaNvOtpbGT-.nlKkuZ4  XpoJ6QT6V \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nZlRWNGh5ZGxoZzRQSVpi\r\n334 UGFzc3dvcmQ6\r\nVlNzWHJWTk8xcUJwV3BO\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nNEpubVZmSk9mclVucUZQV2g=\r\n334 UGFzc3dvcmQ6\r\nWDJENQ==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nTXlH\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO P3TinX6za PH0dVEs4N1c1Tp.wp  NZaGa7Hq  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\neVl2\r\n334 UGFzc3dvcmQ6\r\nREJBcjRMMlVJeVZKZG4=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nWk9ISA==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nNW4xTTVh\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nR2xjQkp5ZQ==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nTGpSb2ZJRw==\r\n334 UGFzc3dvcmQ6\r\ncWNVTGVNX2pOdXN6aE01bg==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nVjBaWDU4eXNvcEcyb09PVjM=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nOWpqN2x1WGdM\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nSkhZZHhWRHFON1pjdzVKRjI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO 4Ki1NVxSNH1sA1Mo qvZbExM t16dTtRGByKA4PUjPlNj MAt3.TXC-64XL36Dn  0Qmuk  M9C R3ecUpnqO8tHBg  38m  9 LOI.w7  SaAb9CJ O  PUuf  K  aEPwRAtlZFAeP.VcCS  JvFOLTj6KFDkaH3KDWK  BIpL91pEdJ98z9B-Yv \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nbnF1TUdveEdvakNWNEtoaUJIMA==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nSVdRS053a2pxTnRXSGFvOTRj\r\n334 UGFzc3dvcmQ6\r\neGc=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nMWNP\r\n334 UGFzc3dvcmQ6\r\nbg==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndEw=\r\n334 UGFzc3dvcmQ6\r\nTDBiZk5M\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nSm9ZVkJEWnZWSFdCYTh6R3o=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<nelyp@w.de>\r\n250 Ok\r\nRCPT TO:<ukydjvakruns@wigonaoctdcliwqyvia.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: AR7zY7VsyL u5\r\nfrom: qmzjaexgyd@krwdoxohmnqrjavlsvto.de\r\nto: wyjqxytgmomhttfjupge@exzvsvfkezrhmryuch.de\r\ndate: Mon, 13 Sep 1993 07:58:56 +0000\r\nx-mailer: rrfVEcy\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nT2Q=\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO 1EI  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nb2VpWFBKcUVSQkIzTWd5dHpIdQ==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nT0lv\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO u5FDZtBjzSiOduvUeE AG2a8VLXpiSrmROiU  UuU3zuBpWcEz3Ta  vFaBpFonNtEV2sxw8swB n2rwncLvP9RW-0.Nvh  F0-S.dB5rrth5LRW- NCJdpw  CJcqxlUb2Hgjw83i OLXq1XzVAwTE7ENuM  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nVU1NS2VqcWE3WA==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO G5X j73A5ymCmM5JY.wLnCb  IVYMRKmTDeVLJwrdgpb8  K9hLM  Qy1fSy2BEw7mWMLsMD  vo5cFnp6 vT21O-cPly  OxmvmGnrDoCppbleji fIRu-Xen6KPXSfV6.f2v  SIGu U51J4u6zIU3NWFBbB  iyI  XKm4TxaAq \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nNFI=\r\n334 UGFzc3dvcmQ6\r\nWjVMQmtaUGR1SU5lQg==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nTmpIRjk0aWg0d1pZYTVs\r\n334 UGFzc3dvcmQ6\r\nQw==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nSjQ=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nWFB1b0lOcA==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nRVdleGxUX2FxbnJMR1ZKaDZzdGs=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<bzfmzit@hfaiiycagn.de>\r\n250 Ok\r\nRCPT TO:<xsraabtozchklgt@x.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: Szf6HkEnc\r\nfrom: ezlufsnynhmft@wnkmlxvrbnhpflwfojby.de\r\nto: nt@o.de\r\ndate: Fri, 30 Nov 2001 08:35:19 +0000\r\nx-mailer: pXbQkCWlrjCdCEkOSp\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nVnpBRHNwRmw=\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO 4T9p8P.MLJCFS.oEg  YkONXbK0mwL  iC  hizLgD  XzMWb  SNCc Wr-hdEckgiK  u7lJuNnCxalxizoaIH 5qhNW8ZAhkPruP  X4O1SAaP1GKqL  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nX0tF\r\n334 UGFzc3dvcmQ6\r\ndVhUcWg=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<fhapzbfkrn@fx.de>\r\n250 Ok\r\nRCPT TO:<lr@hzw.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: E0RSqoT2wd6h\r\nfrom: ocxqymgmhxgogbdzhty@mkiwzxakjmaevzyyrs.de\r\nto: zxfbvtjvin@i.de\r\ndate: Tue, 01 Sep 2026 03:53:54 +0000\r\nx-mailer: lqoXeWxEq\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\ndlNwaVZXUUNLUDNWCmp2azJW\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<dheymkjxlaaevoocl@mtetpstqfcvttyxfcm.de>\r\n250 Ok\r\nRCPT TO:<jvhcakviwn@cveqrfkr.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: bTdclPaGyBv9P-wQ7r\r\nfrom: szoeqbezywjambqzqvw@mlrzqqeyefnzptdjmvc.de\r\nto: u@kzndfvqbyzzjpe.de\r\ndate: Mon, 23 Jul 2007 14:50:05 +0000\r\nx-mailer: HbfPDSKM\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nVURibGV2UndMM2U=\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO ypK968r.yEMz2  hGtZ85pKr3LQMQjx 4Z3QnWY  FwIf2OV8zSTn9HGuqu3Z  qpO14LxVu  BdAv8UyGf  h7zzYW-sSw7.jjkqiWX  Jv-y6KMWlVpNr  UdzFnZ DssW.12VJc2EBRFS .T6.  g2FI3HPt3 qUm71PDj7UMAK  ulia8-2RnhzGxfYX4f3  fS-GJbDjyuB2k.3U A5ovS  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nR2NRaVR1X0s1OGJxTVp4Ykhs\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO lu7cj28GynuETLal  0PtLypLhbGD aasKIjV04v9prdg C4GHbzDqUEqR0iLe  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<qhgvofnpopnspxur@jrjbayybmuuv.de>\r\n250 Ok\r\nRCPT TO:<pv@nxpchwuld.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: a2-8WeJNykgJb:37YD Y\r\nfrom: wsbf@gqnxsiictb.de\r\nto: ucoslwslhvmh@bcnepplqfsslcovnuudh.de\r\ndate: Thu, 16 Jul 1992 16:24:40 +0000\r\nx-mailer: fePXpmnEfzqouepo\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nZjMyVW9RMG8=\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO RcptT97N4ApKYgO0o  GSGGJENqm-Jpe9C SsgHgLKXzCvq  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<vdbg@ue.de>\r\n250 Ok\r\nRCPT TO:<avvebeddto@hapacprkbseilooeks.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: bmknZ6\r\nfrom: mnzgcb@igmw.de\r\nto: irpfbefem@sfqppzwokwlmrk.de\r\ndate: Wed, 29 Oct 2036 04:13:30 +0000\r\nx-mailer: rxfWpPfHvgqcMZiGeX\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nOFBZ\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<vwuloiliqgutnkgybzdj@fmdr.de>\r\n250 Ok\r\nRCPT TO:<ofxzrqvoljsfebln@bsiasqqmwvfjjhohe.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject:  Y\r\nfrom: lzdyueds@jvydrzbqznzieduswhsz.de\r\nto: tyqx@meduixkmpohfplzlczx.de\r\ndate: Tue, 01 Nov 1994 17:56:44 +0000\r\nx-mailer: fKoUlCdrldqsrtlYUq\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\neg11Mmp1SnVnRmloTjg5cA==\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO proKDbzM.oh8 4nnnk1bVJJjQEXTZ  .Y-A3a  g0hKNUHuH05Hy0DhIjK4 SspVuRg5  g i3M4fEPPGUURq R0xujrWq.vZD Dap0Imerud 8mHM8NUiPUcjjhc nByC9WIH.lF07  gZGaOli5T \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nOExvWFR5M0o=\r\n334 UGFzc3dvcmQ6\r\nSFpXMHEzag==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<xlleilrevlouh@zmodefcuemsx.de>\r\n250 Ok\r\nRCPT TO:<srhrmqzoeopd@xd.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: Q8LLILxQRz\r\nfrom: lymveuxorhfsxp@qnapqynzwzfdgrm.de\r\nto: tms@wqmyzdjxyrm.de\r\ndate: Sun, 23 Jul 2028 08:10:59 +0000\r\nx-mailer: c LNMlMp dIbHoPu\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\ncHVJNg==\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<ntnupzecshdxxrflgvhv@rfeucyv.de>\r\n250 Ok\r\nRCPT TO:<wpq@sjcupfcdponfq.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: BV7w6K I-ot1FMjE\r\nfrom: mlzzqwmfvurkwwnuf@miobooakpahx.de\r\nto: ikttizvbdz@yvomvyk.de\r\ndate: Fri, 19 Feb 1982 05:10:46 +0000\r\nx-mailer: GYWT\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nN2VpR2RubGgzbA03TlVuemxEemQ=\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<yolqqkruex@yooareudfkvqedcd.de>\r\n250 Ok\r\nRCPT TO:<zoozkbrmvcusliczs@asoi.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: j.-x\r\nfrom: bhmhhtefuyf@upzy.de\r\nto: rgikdxnhqjutd@opwdxmzalqlnbl.de\r\ndate: Tue, 28 Apr 2015 18:24:53 +0000\r\nx-mailer: S vyuqUf\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nVA==\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<qufcakympaberchivbbe@l.de>\r\n250 Ok\r\nRCPT TO:<omcrltygerbgbdl@pheungtjbnbowo.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: Ie.:MqgtX\r\nfrom: hipdmppjjlezabznnw@qxhkds.de\r\nto: qbwnph@aahcdqopgcqdfldajdg.de\r\ndate: Mon, 16 Aug 2027 04:30:00 +0000\r\nx-mailer: DLeOfB\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nZVZoT3pjDVF6Cm5mWXhQdQ==\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO HcIsXPlEIqT-MF2S6e -fYzgqM  zmUNP  eXs3M-1M3M.gH.euq  AuvzKo4-IfhBihqLIh RkjDgYZne TjnExO5tNK1.6Abt0 kitovn0sF-lS kl.CBrRrJFte1  ui0mMih xrPrqHQJIPEHN  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nM1ptWkk1OUg3S0huOEh2\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO An4V-Eb9C16M KA53Rns572Xrow3TpP xT3tI-tq.NV9D602S m  TcaxLIzdl  I3DnM JtvV6db  pH5W.pA \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nTEdhTlZ3cWpleDdE\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nQkJQWWxwS0oy\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nSkJ2bEtIS3ZN\r\n334 UGFzc3dvcmQ6\r\nTTYzYWZqckwxd0g=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nUVhEQTFhc3Vy\r\n334 UGFzc3dvcmQ6\r\nN3VmNUJxNA==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nak1UMld3SXZGc2xsTEVfQm1KVmk=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nZGZFYUt3bmkyYjF2cUZVbg==\r\n334 UGFzc3dvcmQ6\r\na0FtU3VwUUZPS0d0S2dOWlNFbQ==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO fjusqh. XceMk  FWQHiUH5e53T Bg2iZzoNl.n2q41ts  9c kwBSRPOocvNfi9  XWkC8uD7XV7 cUVrk3ekp4ntzFDM77L  386InDWNLFC EYHppvb2djg561T1R A8RMIJunDd0Lupk3t kYjd0.W.1YSrLG-I VW74PZgu6GlI  VPd MUk9gi.XQWJrGA3QHQz  M 5C9 HSFlWGlEoKf.XGcZA 41RlHtuyKZ9Q  rBEju1L5TzO-JJngOc  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\naW1POQ==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ncnBHR2h2Mg==\r\n334 UGFzc3dvcmQ6\r\nag==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nTEFkZDJkMTZyZHM4R2hGX3pR\r\n334 UGFzc3dvcmQ6\r\ncEswYVNEMVR1OE9ZRzc=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nY2ZEZlJTY1hINw==\r\n334 UGFzc3dvcmQ6\r\nZkdHTlQ0Qg==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nTzQ5aDJBRWRwcWdnQTJyVWEy\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO EP2RuKpJ451FRbwRZdHp J88N7S poj23rOGPNy5U AqGL83oE-q2tM7dEcY7  5DRjHHUGGZdDBnll WSPipjN9bQ3o7R5 9cO  ieHHsWPOaY0SM3tUdJXq  XB7iGp2cULnH69fc  eTdZ vLonnAJiE6 fGjy4w3  fS3jNg-gSlvYuLffw7U  BsegBeAh0tHs b EiJfF  o  At guGk-adFYcy cRK \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nQkZFSTVi\r\n334 UGFzc3dvcmQ6\r\nbUZBZDVUNXBrSmVZ\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ncjlNR3NtN3g4MVp2MXBTbA==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nRkFfQ0gyag==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\neGd1Mnc5d0tNSQ==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nVW80SWFiMjFDa3BBY3d1Sg==\r\n334 UGFzc3dvcmQ6\r\nNU9kTDU2bE02WUtv\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO nA0U-jWaKZm6wm Tqvguxu2wAlGnU  gtDc F p86  0oOhl7KZ004C  Wv  0iZ0wuaA81GroZI3UI  NjlgzH b6SoOhnTHRnxL7r  d  k8Kq  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nRmkxWHBadXRWTlJncg==\r\n334 UGFzc3dvcmQ6\r\nTw==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\naWE1WV9L\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nRzZJVGs=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nYVZiVkREQTNGbExyTENjcTZZcw==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\naXZyZXVHZERpc0t4a3Ra\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\naXpxTW9hMjN3Nmk5c2E=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nWURYclQ4d2RZQnI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO MKui5ExoRvlF3b4  ageZ77Lh  Ezc.p5X  F7YwvlipsrWlJLPDr3l  pJkLkp5  rH1zePI  tZgndVk3UysGDDbDe \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nMFFobFFESXRwa1J3bDlySg==\r\n334 UGFzc3dvcmQ6\r\nYmFxaE1EVld6Sjg=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nSnFTbXlWWXE=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nNWRaMDN5MGc1dF9kRkFLWDM=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<sbfquk@ltkzlxsqbp.de>\r\n250 Ok\r\nRCPT TO:<pedvdj@zcgsunnhqfdzcb.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: Oks\r\nfrom: yygmgnjk@iphylajgpjmskqsvn.de\r\nto: cjyhks@lqcuzpkkperirocxobj.de\r\ndate: Wed, 16 Dec 1970 16:36:19 +0000\r\nx-mailer: GEGRbpPPVin\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nVnhMWGt5NVhYSA0KU3BuRXlT\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<kkapqbjz@nqogovyckhzjiindsfx.de>\r\n250 Ok\r\nRCPT TO:<hzuocey@irzotizbgprslvcwg.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: QbW tn\r\nfrom: javrspnughmqlnp@jtmysnlia.de\r\nto: mkypghnoxjbjxpntthwx@tirywcbne.de\r\ndate: Thu, 14 Oct 2021 16:44:19 +0000\r\nx-mailer: zLGie lQjFIvgliFSqA\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nVWhUUmRv\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<mlgusgfldcuuruxxg@foqxshujvcjt.de>\r\n250 Ok\r\nRCPT TO:<osqky@bbezmm.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: L 0jD_EUMdSzHUl\r\nfrom: lccqenrm@xoxu.de\r\nto: uobrpsmdugfjpyyfb@ochzpqqiksdfrg.de\r\ndate: Tue, 09 Nov 2027 19:36:52 +0000\r\nx-mailer: ZyejSnlaWEhWyD\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nS2NDUwp4dU50aVJPQ2E=\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO Uq3BGKPwV8e7lZoA  3vkD5ZDuNqWkzJmRIG9 ..cni..TFDtp7uVK51Pl 2x35FuqQBYvpwY fNUA6h7I3iIfYd6RZr JaHz2ctg \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nYTdRZDUxNjVjRzVTS1BKTW1ub1c=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndE51MW1GdlpEYW5YWEp6Ug==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ncjV1Y0g3OA==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nemhweXN3\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nekxtVWNOTFUw\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nUDJhZFhC\r\n334 UGFzc3dvcmQ6\r\nRE52MEI0OWhDRnlWQlBzZW9u\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\naVpGUDF6MTVoOHdkWEdtZlpRVmM=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\neXlfS2p1ZWdNWjRPaEhfVnIxbGo=\r\n334 UGFzc3dvcmQ6\r\nWW5SUkpXb3Jv\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nUmlvbGh1czFsWFp0OEdXUVBpQmQ=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nZ3hSMTMxZ0w2UQ==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nSmxaeTI=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nOUtfZw==\r\n334 UGFzc3dvcmQ6\r\nUXZMM0tza3VNdXFVdmU=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nQm11alU1RWNIQkF4Vw==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nNFNv\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nR0tJMVdrQkJ3UQ==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<wfcaezedbnbcfxiqmh@nrcsfvblxiojofyeqkrz.de>\r\n250 Ok\r\nRCPT TO:<rgpbybbrylnzqsrg@fuxlghjxcpnmmynv.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: h6k3gQdksAlM\r\nfrom: ikkrravokivgntnch@qnh.de\r\nto: wqkpla@uyfkleqqsbv.de\r\ndate: Mon, 24 Apr 2028 06:57:36 +0000\r\nx-mailer: MeYQSevGOTXyMk cQ\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\naA1rMlVLR2hiS1AxTA==\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<imyyp@mtwswxuqcvylvc.de>\r\n250 Ok\r\nRCPT TO:<lyqwqgyy@h.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: IaWGv.5mvUxDDu1\r\nfrom: oiawh@xuhkkllwlilasfifafec.de\r\nto: gahzuldtgvmcqjyats@oitbwhnzzpb.de\r\ndate: Mon, 31 Jan 2005 00:31:20 +0000\r\nx-mailer: eZI\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nQ0hEWEpYSw==\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO j5IyBTIjCl-9D2B09u s3hqPPVo9EfJ5lhO  wOB  kvR5rtcb1R  C8PMXZsX1UwtkOV  rx2Q79b HbNv-9cIgM8 mKpwDBr  XUeY9xUNL18Y0 zCjky  vtMlHv20 sFQAq3 4zj9ZKBuD Fi897PY0  gVZaTbGkmY8MqIqW3 8lu-kLUW \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nUlRQYWN3OGJ3anlIQ3cxdFg=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nbEpjZWdv\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nZWZqOG41X0xRQmI2STRmekM2TkI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nRkZKQ3dUdHN3RXNMQw==\r\n334 UGFzc3dvcmQ6\r\nRjdSZnh4V1Y5\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nVFhteDcxbkVFeEhIckhENW1wOWU=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndUNCaEF2UFEwdHI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nag==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<uhzyqkziujeeuea@rlgvr.de>\r\n250 Ok\r\nRCPT TO:<iicmtdqmtoeklw@dswqlwqahczhkm.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: tC s6uPxzDt\r\nfrom: wbyivqguwjrh@tocdfigawhfwngaqkkn.de\r\nto: pmtiqwhbnstkfeje@ygaa.de\r\ndate: Fri, 20 Oct 1978 16:53:04 +0000\r\nx-mailer: elAKq C\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nDTk0ckI1NGY=\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<xgtfajttt@zlhfkbbnoe.de>\r\n250 Ok\r\nRCPT TO:<ysoovlitpu@sjombutvuuqz.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: Zxfi\r\nfrom: mlymhirhqbbzo@qcagxcwmanfwbgwlno.de\r\nto: fdth@adwyf.de\r\ndate: Sun, 04 Jul 1999 21:29:33 +0000\r\nx-mailer: T\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nNjl5TFk0VWVN\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO Coft  ytK JHNa99xVqbgB-w5xYvA xDbhXgSttelbDWQgzb  qB5c  Pf6VSZJc3sceIY0CKnK  JtFIr1RTp yLyCPIIPm4ulzVi2  aPjQCEHYIHx15v  PSmrFZrA6L9aLGnN2W NPz  T \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<z@t.de>\r\n250 Ok\r\nRCPT TO:<bbabgemvaeourujsargk@fhiexxe.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: U1vzvvQVh\r\nfrom: nwwoydxrahxuwuls@rtvxmqlxigurgqoagr.de\r\nto: gnhgcxjpcejk@zltwinbci.de\r\ndate: Fri, 27 Oct 2028 05:00:29 +0000\r\nx-mailer: fivnOBkXLV KBVrAC\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nNndXb2xlMGpnZGlaaXdHUg==\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO acs8VBmgEDkLcfs7bIl 6Hifm-c-XHzt3u5AU7a  2bs2VW6MO.vkR7Ll9 e-hqAW kJSfypPsKc8Q 8Ya3HMwfu---h1ZoM  YEu  H  NtEx  sTboFPTuzt q9yxJFUcMjzbdJD  99jRl  GfFPeRtDYd7sIRIc OaZJn2B3CJqIte  xkftNxzvxz  sG89G6cscdY9g \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nVUJ6\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nUkVxemRWNnpHbUxMSVJUdk1fcw==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<itrqmfga@igngpws.de>\r\n250 Ok\r\nRCPT TO:<eav@ddjdsewxbb.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: rsaf-XXmwjYSLgi\r\nfrom: lvlbgxlruxwgwrlwvozu@thxzctggfcfj.de\r\nto: wz@turohitijwogubx.de\r\ndate: Wed, 27 Nov 2019 12:04:07 +0000\r\nx-mailer: jwqC\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\naEJOWWxBN2xXTUdv\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<boiyurpszbit@iywugpeg.de>\r\n250 Ok\r\nRCPT TO:<zyykzube@kbbuemly.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: G0r.DtYFbf\r\nfrom: uhoatkwnhmsmpnr@inmbqndsai.de\r\nto: mcnuowfnqihyy@jljhhgytgls.de\r\ndate: Sun, 05 Dec 2004 20:40:37 +0000\r\nx-mailer: OkyIOGVcjpyViWufntY\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nTlNPdFdtZ3FqTlR0dmdK\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO BzVYvbndh  JEfsETWa-V  uO1g-2BX-Xc \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nRDBuRzByRA==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO I3  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nczk=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndFI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nSlV6Q2FWWGdh\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nSGxsdzA0ZA==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nQWM4Vw==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nYkdJUlNxVU5sZUdrZjNfQm5P\r\n334 UGFzc3dvcmQ6\r\nUHF5dnA5NU5XTW0zWUZRVA==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nTDl3Zm1lZHpWdzVK\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nM2YzaTF3ZlRUYVI4\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nX0kwcU4=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nZzRBZWptRkRiaVVfbjdD\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<buisqsiikixeq@poecimxdzngqkxaxldcc.de>\r\n250 Ok\r\nRCPT TO:<cdrsrfjrzvdj@yuj.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: EHdoxvcxUDteNf\r\nfrom: uaiyvtwqugejonnpgc@exfqjodmymhgszb.de\r\nto: icagfsut@jvmbgugjofbo.de\r\ndate: Fri, 17 Dec 2010 22:41:39 +0000\r\nx-mailer: MQEqzaJOw\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\ndGNSSTk2Qjh6Zw==\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<kjmgxbysmxlagpw@buresunywmcgbefho.de>\r\n250 Ok\r\nRCPT TO:<mt@wjswzitwkrhoyfhcpzj.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: D2lcq0Azqgw9wuneL5\r\nfrom: rtfteucqgl@qnih.de\r\nto: kijjmsngiaslgyj@gcqmrubvg.de\r\ndate: Sat, 02 Jan 1993 03:11:29 +0000\r\nx-mailer: IlznfxOwAtfCL\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nOVc1bFJDY2lXdlE=\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO qBAUcYnPny VdRTx5FpCeJ6kX1DCRi jPl0pNHtHbS3XQHd IcN  pd MAXyN5HpnEeg0 kuHxGGb0xUo  cLuHFU TOx 7kOEtyx j4ePTKyZA4g4y YyMkr  BeGnxKQWIMRIzqkpjzVt  8HZ Qyw  AvQj  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nSg==\r\n334 UGFzc3dvcmQ6\r\nTDdqQjhVbQ==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ncVBKWlpFT0RPM0ZJ\r\n334 UGFzc3dvcmQ6\r\nM0FWYnJ3a0RyV25MV1dRYllDWg==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<wzzgvcn@swvomnvqzbcxqme.de>\r\n250 Ok\r\nRCPT TO:<n@rcrwasyzbirqoszxyose.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: IDNDqN .j7I\r\nfrom: ftybkmmkzslkoakdtv@tqgndlrjwd.de\r\nto: aehaeztlqnst@w.de\r\ndate: Wed, 09 Dec 1981 02:08:59 +0000\r\nx-mailer: psNqqqDaIaIg\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nWlhUZDczTE84NkNTWFFKT3U=\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO MWhFZUO4SBJbjd  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<xrthmeqldpwhdipnz@mlvduinhqkxdedimuw.de>\r\n250 Ok\r\nRCPT TO:<hkixgvpzkluzlkmatus@afgze.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: u3zC4c\r\nfrom: py@smbndyyvrdfdfckivetd.de\r\nto: krbwhvabruj@ieagecow.de\r\ndate: Thu, 21 Jul 2005 12:26:42 +0000\r\nx-mailer: UuGAIYsStjnM\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nSmZKY0cyNGI=\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<osdtryljnk@wkoyq.de>\r\n250 Ok\r\nRCPT TO:<hxayktpohb@wjieqexrdshrrvvrvym.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: y1Sk_X7A\r\nfrom: cnonzigelbm@ebuytte.de\r\nto: ndznwnlyfxacy@mzbkgpkclzmrk.de\r\ndate: Thu, 13 Aug 1981 00:45:40 +0000\r\nx-mailer: m\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nblFNUkxQRQo=\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<fsbtgeubpjpyftc@s.de>\r\n250 Ok\r\nRCPT TO:<quwsadmbqiuyszgluczp@cygyegyrjrbyrjsmqk.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: dhAHGdvqJIlSJ:\r\nfrom: qrbdtcl@gnrr.de\r\nto: rbzhlz@cqrarsdodytisfpky.de\r\ndate: Fri, 04 Aug 1978 08:30:51 +0000\r\nx-mailer: cWeMrmhYRdvORcSpT\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\ndw==\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO d  UVxnn7F  FigLkDbm  HME4g.2AeX  TLwJw-MfljV8N  VkKwtdhwD02v yjv30bZo 9vjNcF01XGmp U7f2h0nGE6xNFOD-  wX8kSFwrjY  PCV4FOylbdqhZ4 c \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<ymhkc@hkabpujqlavxjrf.de>\r\n250 Ok\r\nRCPT TO:<d@baybezad.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: 9xj6Ux\r\nfrom: etvahzfygeqipbsmkm@luuujsizpqiclgknzr.de\r\nto: fpghxtjbxdly@jmb.de\r\ndate: Fri, 18 Dec 2020 09:12:30 +0000\r\nx-mailer: xakeyAGUkL\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nSmtxdWhMOGVC\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO k4d  QYNCT u \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ncnk0UGh0RlY3ZDg3eEo=\r\n334 UGFzc3dvcmQ6\r\nSWdBclFW\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nY3Fkdm5LSWhrYVFWNkNoNjQ0eQ==\r\n334 UGFzc3dvcmQ6\r\nS21GekV1Q3l6QmtjVmFJMHdoMnI=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<zvukjcfzj@aczkbzvbainfsuqtysn.de>\r\n250 Ok\r\nRCPT TO:<vzomzoaqbxmvtwmz@vealbktbiim.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: PFIHrLi3gqfA64T9\r\nfrom: clxvjfjkygkoslcxazs@aihsvanxyfyjlegf.de\r\nto: igtg@fd.de\r\ndate: Mon, 21 Mar 1994 00:46:52 +0000\r\nx-mailer:  GoEjwtDzjwehMraTwn\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\neWU4dWdGeVZEY0t0QmpWUjVI\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO P.2Dps9  9TcP UAPJmPdJ00W  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nXzJQQm13Q3lrWE1DYk9LeWFMUw==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nczliRWl2N1VmSjk=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nenFLWTI0RW9GT1lYQw==\r\n334 UGFzc3dvcmQ6\r\ndnZIckthRFdPb3J5S0c=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\naE5RTmpfRWd0ZWVC\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nRmRQbXhWMmZrYWZFeVBmYg==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\na2NvS2N6bkx6TmRfY0M=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nWmJrS0p5U3c=\r\n334 UGFzc3dvcmQ6\r\nV29lb2hSeDN2MEFINDc0Xw==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nZnlqbXQ1U3FLQ1RYTlhiM2s2aQ==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nZVZvb3pNd3c2dHBxWG1HMUc3ZG8=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nNTNIRnVDczdKOURMb3ZNeDB5RXE=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nX2pX\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nelVYb2t6S3QxZm9CX3Y4eVZI\r\n334 UGFzc3dvcmQ6\r\nclNiUmxjWg==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nWWNxbHQxWQ==\r\n334 UGFzc3dvcmQ6\r\nVFE1Wl9yMWxyM0dmeXVOZzR3M2w=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nYUhMeHdOaw==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\naE91YWpSYzBUUg==\r\n334 UGFzc3dvcmQ6\r\nUUprYQ==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nVEtRN2k3Y2tTU3J1aVZS\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\neXFVOVFqcnExODRfVkN6Tk8=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nRkdTNkk=\r\n334 UGFzc3dvcmQ6\r\nRUN3S1MwRjNxbmRpNVFFcUQxNg==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nS2pzUXpsc1lJdQ==\r\n334 UGFzc3dvcmQ6\r\nYlVfelpMZg==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nNGhUZGRk\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nX0ZkaU9EWXd5QWU1Qg==\r\n334 UGFzc3dvcmQ6\r\nUEtScjJZTkJlQjZEOVNlOXNvODE=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nMGFOUk1Fc011cGdk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nak52VFBfckE=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO c5ZE3  Zlfy3pnGU9sBs FvGlu83Ae  legAVGL6 SV9S6-x9ceInj8D6cqNj  UuzzEtQuzNrZO-IF0  CmCjGAMorB6yN cBmf.3LHTZZOUXoVS Ipcg6s9-jWc  hqcPKukB4j8AEXKS  IK0.UHXQDFHz Z22z HUcr4BjEqo7td3cUhpIY A1wZVhSinn PwDY1 m.ynu3kVeXFv9kyS1p- \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nUg==\r\n334 UGFzc3dvcmQ6\r\ndzM1QjVDWGYzbHI5T3RXTXRfcnE=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGFIb0J2UGVTbUU=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<ttnfkfoajw@epdswmqljymhfsux.de>\r\n250 Ok\r\nRCPT TO:<azlvsrwje@djmxnhu.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: aTT\r\nfrom: zbichaechtotrhbtxk@rii.de\r\nto: pmfcajfmjvlih@owcyfmsatz.de\r\ndate: Fri, 23 May 2003 07:04:18 +0000\r\nx-mailer: iVrk\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nSDN1R0NmMkFwaVVUV3NJWmxo\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<njxjah@xongqjlinfumt.de>\r\n250 Ok\r\nRCPT TO:<vjdqtdyioegjsh@yjlr.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: stikAFxC:4l\r\nfrom: efyybbluzoc@mrzgfzpejsnndifkpdk.de\r\nto: oxjhutv@scyikgkcavrv.de\r\ndate: Sun, 06 Apr 1997 20:33:29 +0000\r\nx-mailer: LiEbmuTX\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nY3RmCkRRDWo0QVo=\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO M tt9AllR4plAcuaL  zp9BmYd2y 8-5n4KN3J4KoVZR39 zQX0  5RA5Oc iY4 YO 51V8h7 DY4BWaYoxaV5  q  D xILELN2unj2mko6Ur  HwjZ  Rrjm84YJ7Duh  PPE2q7HCQZo6kArdmN  bkgca0P2znSTyP5P30 nuS  gA8a9MbgkbhRCQG MlLl2yHWBq-F  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nSzFMdnFGaE1wSQ==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGNHNThhX3F4b1dtMlA=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<miqmh@rnrpakmapieudqlssos.de>\r\n250 Ok\r\nRCPT TO:<gfgsejzeukxkgkp@cslziiulecbt.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: uU7bge3.0\r\nfrom: yvvnibggtmhnrpwicdo@iorwqlr.de\r\nto: prtbpf@mzlyjyskcjhubpv.de\r\ndate: Tue, 10 Jul 2029 08:27:56 +0000\r\nx-mailer: hExWUoSO\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nOFRuMUt5bE96c2E=\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO tuLu6LZvroGA0UtDMloA  ZKY6DC46N N  GtBjxZsW-yHvfaH3pcHx oDmXHb6j54atouN6rD. j 4p1RMG3eITV3a Kkcs3WqbMq0ICT V.Wbbe BEtOwbYeI  zr6 \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nS1A0TldDU2N1NERYbjFJOQ==\r\n334 UGFzc3dvcmQ6\r\nUlpVNTN5\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nVkVaWWdHSzZ0\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO g6ggZzyYv6  6yldE1LzJrG GojLph2  4tyEMC-Jyo  eMu-sjM8nckcU OXk zypp8b9BHFD5UrGi WvQ l3eKiaNgbuSMWpux QIT6-Dif6gH EQFNlb-JMzlAQGo  .SOQw2lVn6aAo9EeVV9 y5oKtzjb7IYp3  Y a2dU0UvV6Y9  CZWbeijvqUp ObpvP0pjupPmNg \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndzdqaHBibkY0N1BCQXRQT2Q=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\naA==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nMHFITGZwMFpISTFLNHo=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO f  lLbcpWuU7npCYm0Ux wOx  -SAaGGqc  pozIJ0m76HSod8tUlKnx i8DOLexW9cRsuo  q4  ZGxm- Mam  S0R 0nGN WDHrMlYXaFuKnm z9iwfyptn1DUcWRFF \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<ougwpce@dprnrkfniljvursccpeb.de>\r\n250 Ok\r\nRCPT TO:<rrx@cuaxsxryct.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: aaCkCNQ\r\nfrom: fbdihupazcer@f.de\r\nto: ofwsdbrcrrxu@oxjywahoyz.de\r\ndate: Tue, 25 Dec 2035 10:17:24 +0000\r\nx-mailer: peC\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nQ0c3OXlWRk45\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<cxjaaitnye@hqvxocmlbeygybjzjcy.de>\r\n250 Ok\r\nRCPT TO:<yrihtnpfurdw@glwuxwsvvei.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: fQ7itvCAuxPVRGb1\r\nfrom: rqnzphr@x.de\r\nto: kpufvfjewuvhxgjpehn@phwqcrm.de\r\ndate: Wed, 22 Sep 2004 02:18:28 +0000\r\nx-mailer: OfQqre\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nZ2RsczNDRW45TXdpdw==\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO c Pd.U pPz  hUSKGTEnVXVjwaEz YaS6 ZN9.tI9lpj.EOEH6-el  QAhrd6ybE-Vez0rjlL  HAIb5VRbbWaS PZE.n6NqAWffObE7 LKlVwJDgZTabzw  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
Coverage log:
Nr trees generated: 52
Nr messages exchanged: 2124
Overall time elapsed: 376.04s

Process finished with exit code 0
