/Users/alexander/PycharmProjects/fandango/.venv/bin/python /Users/alexander/PycharmProjects/fandango/evaluation/experiments/smtp/smtp.py 
fandango:WARNING: Symbol <pass_incorrect> defined, but not used
fandango:WARNING: Symbol <user_incorrect> defined, but not used
fandango:WARNING: Symbol <unix_time> defined, but not used
fandango:WARNING: Symbol <mail_contents> defined, but not used
fandango:INFO: ---------- Initializing FANDANGO algorithm ---------- 
fandango:INFO: Generating (additional) initial population (size: 100)...
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Initial population generated in 0.00 seconds
fandango:INFO: Current coverage: 0.00%
fandango:INFO: Server: <response_setup> '220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\n'
fandango:INFO: Current coverage: 0.03%
fandango:INFO: Client: <request_ehlo> 'EHLO MNNh31K-0uD-ipB l7.S2EkwYi02 bzd2SWm  nrqjBMxgyY-d  7L7Nv-3yboM.rCBPx  J9VA3eKAM7ja8qJmU  YNl \r\n'
fandango:INFO: Current coverage: 0.05%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.11%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.14%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.15%
fandango:INFO: Client: <request_auth_user_incorrect> 'enpVVzRfemdjWkhkTFQ=\r\n'
fandango:INFO: Current coverage: 0.18%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.19%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 0.21%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.23%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.25%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.25%
fandango:INFO: Client: <request_auth_user_incorrect> 'NHhqN0dCR1lLSlVEWmRyU09D\r\n'
fandango:INFO: Current coverage: 0.26%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.26%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 0.27%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.27%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.29%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.30%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.32%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.29%
fandango:INFO: Client: <request_auth_pass_incorrect> 'TTliOHBkQ1U1\r\n'
fandango:INFO: Current coverage: 0.32%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.32%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.33%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.34%
fandango:INFO: Client: <request_auth_user_incorrect> 'M0FPTk1VZVNXcFdDd1FGR1k=\r\n'
fandango:INFO: Current coverage: 0.32%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.32%
fandango:INFO: Client: <request_auth_pass_incorrect> 'TXpUSUxudlpV\r\n'
fandango:INFO: Current coverage: 0.32%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.32%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.32%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.32%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.35%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.36%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 0.37%
fandango:INFO: Server: <response_auth_success> '235 Authentication successful.\r\n'
fandango:INFO: Current coverage: 0.40%
fandango:INFO: Client: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.43%
fandango:INFO: Server: <response_quit> '221 Bye\r\n'
fandango:INFO: Current coverage: 0.45%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.45%
fandango:INFO: Server: <response_setup> '220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\n'
fandango:INFO: Current coverage: 0.45%
fandango:INFO: Client: <request_ehlo> 'EHLO mbAsqAGHuUe  6-wx6g-Ik8PSM8x6bzw q  wyIfI  mI OKXqsdIRmjwpcexvW ayezyHqf7sregwGQK  .EjvMXuRxAg m93ogl4McXF  fVXaimP1.1yLYWHxFA 9ynlONZ7tm1SHgBs9  anUv 9Ne5b1  IVtNiquavy \r\n'
fandango:INFO: Current coverage: 0.45%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.45%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.45%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.45%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.47%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Client: <request_auth_pass_incorrect> 'VFRkZkF5SVJLazE3UG41TV9Z\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'Sg==\r\n'
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
fandango:INFO: Client: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Server: <response_quit> '221 Bye\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Server: <response_setup> '220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Client: <request_ehlo> 'EHLO a  aiIH 3bx0fg.7Aap15 \r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.47%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.48%
fandango:INFO: Client: <request_auth_pass_incorrect> 'ZkRyZUd0a3A=\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Client: <request_auth_user_incorrect> 'cWdxVXIxZ0hy\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Client: <request_auth_user_incorrect> 'aQ==\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Client: <request_auth_pass_incorrect> 'VmdvS0J1cTUwZnhQWlJUMg==\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'N0g=\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Client: <request_auth_user_incorrect> 'OWtMU0Z5aw==\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Client: <request_auth_user_incorrect> 'bmhwX3hhQktEVTlHRl9tRU93\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Client: <request_auth_user_incorrect> 'SlNWMHdQWXN0Szl3c3FrR2JpZHQ=\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Client: <request_auth_user_incorrect> 'QW8yTzQ=\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.46%
fandango:INFO: Client: <request_auth_pass_incorrect> 'bg==\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<kmwwjcpp@kgcjxbvqpzrzfi.de>\r\n'
fandango:INFO: Current coverage: 0.50%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.53%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<o@qgcekfq.de>\r\n'
fandango:INFO: Current coverage: 0.56%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.58%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.59%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.61%
fandango:INFO: Client -> Server: <mail_data> 'subject: gSM3Mh6LQXkRIcv\r\nfrom: rtxhlnvhcif@ygxdhnduvynkbaidtyf.de\r\nto: kdcebjcrqagh@cmqlcnphubl.de\r\ndate: Fri, 26 Oct 2001 06:54:22 +0000\r\nx-mailer: cBV lMmyufKtVNf\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nTHpkZ1ZMOWlDbXl2\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.86%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.88%
fandango:INFO: Client: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_quit> '221 Bye\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_setup> '220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_ehlo> 'EHLO HP9reAOQzd e  \r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.91%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_auth_user_incorrect> 'ZGc3S1o=\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_auth_pass_incorrect> 'bVl4OG8=\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'UkdfUzM=\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_auth_user_incorrect> 'ajBQOFc5aFpkR2FmZzdN\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_auth_pass_incorrect> 'dFZXSUJEVUVhY1dN\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'MXd4eA==\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<nkjlaulftbabphloosg@utsnuepwbdbg.de>\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<vzhndadavnyhldgfw@wkrcivxfuhzwmldo.de>\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client -> Server: <mail_data> 'subject: E5NBBYCIuBx\r\nfrom: ecrmnmndfy@smshst.de\r\nto: qaxnicjgsidfohed@lfdrvnmvgjbzoezsupdv.de\r\ndate: Fri, 10 May 2013 20:34:43 +0000\r\nx-mailer: ZFTeESnTTyB\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nYlM0NWQ5d1Q=\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_quit> 'QUIT\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_quit> '221 Bye\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Starting new protocol run.
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_setup> '220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_ehlo> 'EHLO uyHMzlPlsG  ONmd8nfVN  R.f  uzz  uVGTY1Tpv6Oca91en2 S8-tGVmsFp9Lgq2gi  ZeG6PE-  6Lpd0CXQr PmfoJI \r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.91%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_auth_user_incorrect> 'a0VyWDlwRFd3cDFxQ2g5\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_auth_pass_incorrect> 'clJKT2RHTTRzNUZjcnptMXIyR3c=\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'ZmlDRDJlRzE2\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'dVE=\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_auth_user_incorrect> 'N3RHUTVYRk13X1lPNE9WRkFudGE=\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_auth_pass_incorrect> 'c0lTVWEzWkdH\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'X2hC\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_auth_user_incorrect> 'eQ==\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_auth_pass_incorrect> 'VA==\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_auth_user_incorrect> 'Vm1DaWNTWHVxYzlSVDN3dw==\r\n'
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
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_auth_pass_incorrect> 'a083ek9HSlhfWk9WMGdhdg==\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<xfzlmqtxcrsghoa@wybtgrcywcodgolzqd.de>\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<zr@yrjwaiffrcezc.de>\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client -> Server: <mail_data> 'subject: BtStBLjIh\r\nfrom: i@no.de\r\nto: ffffhborbsghwuwfyrel@pquvcocppoc.de\r\ndate: Sun, 07 Dec 2036 20:15:22 +0000\r\nx-mailer: qwvsLAKu\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nRA==\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.90%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<nygp@abcmbckxac.de>\r\n'
fandango:INFO: Current coverage: 0.91%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.92%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<riqiik@qrw.de>\r\n'
fandango:INFO: Current coverage: 0.93%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.94%
fandango:INFO: Client -> Server: <mail_data> 'subject: 854qKFk-hV.TMRUZ_\r\nfrom: yffatxj@sshsvbgwbvkiifemk.de\r\nto: aszvlopednh@ilprslwxpjejgdsbd.de\r\ndate: Mon, 10 Dec 1973 13:52:36 +0000\r\nx-mailer: xB\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\na0VzWjczeUpiTmFnaDNnS1FX\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.95%
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
fandango:INFO: Client: <request_ehlo> 'EHLO V4sxR kLOGw94E3R p0rBlXLW  vgt48  YC4eL  kese E-JPO4-Ssf2-M2V0-1  LPrItph \r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.98%
fandango:INFO: Client: <request_auth_pass_incorrect> 'VDAxVUlfZEtIdGNDaHY=\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO BSHtMZ9qA ZT-IFjZXKCNLdE JW1j  3Snx1GOPtY L  5kfB-C h1S7bDHaSD  \r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Client: <request_auth_user_incorrect> 'VENhRUNLYWVzczRvdFJGbg==\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'ZjJq\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<hbkyaymcjtmioocued@zuwokgejcst.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<daqnkwf@ht.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: s\r\nfrom: drrzvbfotisyatz@jem.de\r\nto: gm@yenlwbtybjyenjjmmtr.de\r\ndate: Sat, 17 Dec 1983 08:08:02 +0000\r\nx-mailer: XJbHDBynt\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\ndlJtVUZGCnRYdEJSd1BiSA==\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO Bb6GUsSkZR3z6gMOLbOk Z9GYha FrMPwh pZnvJHSoZtG07sw  AGxWhUWz5UAA-P5CK0l HfaYeXi68qZN.bB9Lx  JzesnQ33vuQeXBaY1p K4iVVURKhgyQ tNUbkCFFqGY9lJlWgm0Q  wNw7PlUyZXC ny8Ui uDMau \r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'T2JsbXZv\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'VTR2emxzdzI3\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'ZXFoREtyWg==\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'OXpoUEw=\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'bGZQYXZUVDQ=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'UW82SlRaQ2lqbTBxWUla\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<ttjgmpnvqxcdtdgqwt@vrgcfkdpqh.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<f@usdpbzrarzflhvpiwt.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: dyx1\r\nfrom: kzflynnxik@stxzaeqwbn.de\r\nto: lkjajk@ebptvabigncbmafudep.de\r\ndate: Sun, 28 Jul 1985 18:15:29 +0000\r\nx-mailer: KYsHgqhluyXOfqSss\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nYnFOVnN4R283MXVENzRJamg=\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO W9u735SE9vzfweH8w  . yT \r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'UnZUZTFTMFA3eUNubA==\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'djZyQUpY\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'M19FV0xpSlp1\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_fail> '535 Authentication credentials invalid\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_user_incorrect> 'QmxVc2hhR1RPX1Y=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'ZF9GTU5UWk9QTG5ZR3B5TkRrYQ==\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO I I4ewsUJcQ8R  BiEAwp1U3UfUQQh9  IlUzmRtvHquB \r\n'
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
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_incorrect> 'Z2s0R0tfN1BUM0Q=\r\n'
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
fandango:INFO: Client: <request_auth_pass_incorrect> 'UEtvbWZsTmUwXzFP\r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<vaieahmrchjkahtcsddm@hemzaaee.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<rvzcfiyybvtfcusuasq@iqiwolytenkeigwtgwmj.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: lKSvOPkXrrHdOgogZF\r\nfrom: gbiuelgqjqkvolszzgk@dvbacvynsdjmteusx.de\r\nto: hwcs@xcplpbgrgynn.de\r\ndate: Sat, 04 Apr 1970 21:08:39 +0000\r\nx-mailer: CHSrjEkyubce\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\ndUp0dm5hcHQzU1o4T0c=\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<xelnkeyvew@gvogboutcmlf.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<zbgtkl@qmvungcpjn.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: k6v\r\nfrom: ddbts@umvlhxh.de\r\nto: bugfgwjhpzi@qwpemxbqlwyc.de\r\ndate: Thu, 04 Feb 1971 20:46:39 +0000\r\nx-mailer: fHSbtfYlzZgyvqaAShcg\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\naWdZ\r\n\r\n.\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_submit> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<gevpqwtysfwitngk@qd.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<glqyrzqegzees@bvoiwq.de>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client -> Server: <mail_data> 'subject: 55:K2XpZ0Y6\r\nfrom: qf@lmghpkkbid.de\r\nto: u@mhzsu.de\r\ndate: Sat, 28 Dec 2030 21:51:02 +0000\r\nx-mailer: BCVTkuLy\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nVjlpWWlxa0hGTkRWDQ==\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO YGVqeNr4-PAnN  n22aIZH1-YNzui2Lwqx G9rzWXVgTEyMo3y bCKdjVuHodiH-yCZ mSEq0 O1A06BbTK6qTIVUv  rDVcjE  Wou5 0Ok5S73-XIF  \r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 0.97%
fandango:INFO: Client: <request_auth_user_correct> 'dGhlX3VzZXI=\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 0.96%
fandango:INFO: Client: <request_auth_pass_correct> 'dGhlX3Bhc3N3b3Jk\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: Server: <response_auth_success> '235 Authentication successful.\r\n'
fandango:INFO: Current coverage: 0.99%
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<hecfdep@bactyzy.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<gikoafbcrksng@bxqzt.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: sxx\r\nfrom: kysdadlufwguisxnld@wuclg.de\r\nto: l@rxtcunkuxdmkpcao.de\r\ndate: Sat, 01 Sep 2001 13:19:14 +0000\r\nx-mailer: nLfA\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nVmpIb2R3amhP\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO .2ryTw2a9FPSdWor LjDL1k Uv  fQ6q8voH  nxnld4mFEs  jadVhHdur9YFXXI36up  B-hYjf6JfUIH L  O KGdBj1a1  5Y91fPnZpFYSgTW3P LHe6t9 npvM69QeRs \r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'S3IxckhwSkRJbWt4\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_pass> '334 UGFzc3dvcmQ6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_pass_incorrect> 'eGpCNEMz\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO 2e11fkmBPsDUl6.Hf YAqL7fU0lpO F9NK  7DkZA0 Ri51WYR7euAE87vYSC  lkhHVyZD3WF  .CLgohqZ.a  6N3tij.xlalzmJlxPOk 7xENJ231Q  fLu6EVWP.lUcVj9  N68pR8z5qsDTgk  Bu  b QXDB3lbj  QX1OAmonTue  0 gufH-W5cDi  sUThJitpTNLD50dBfA  5Xyzp5-5f.pwYZZ  c  \r\n'
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
fandango:INFO: Client: <request_mail_from> 'MAIL FROM:<f@axd.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_from> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_mail_to> 'RCPT TO:<wtbjvzxeia@yvn.de>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_to> '250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_mail_data> 'DATA\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_mail_data> '354 End data with <CR><LF>.<CR><LF>\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client -> Server: <mail_data> 'subject: vKvhvBkjkb5x\r\nfrom: qcmwcughvlvjhkz@wjaubdzwzncyvbhlozi.de\r\nto: clknvcoprquvdta@lnnwbwlqgi.de\r\ndate: Sat, 15 May 1971 08:11:12 +0000\r\nx-mailer: BGdtmSjKxelqkanDN\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\ndzhUNEU2Tzd4YU9TODJtc25BVk8=\r\n\r\n.\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO u555QX6  To tgDtyy9-hPWOb dL6OdyPoLd6Ii eZ  2  gE mjnUsB  2qXpWmCW sTR7I0X  8z9Si0luGTi  teuGYH-J7nRTmBLhyn7 b-lxXqaOLVd2hQw9VqZ pdPSYWp6CodrEH2ADK2D  \r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_ehlo> '250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:WARNING: Could not generate a full population of unique individuals. Population size reduced to 1.
fandango:INFO: Client: <request_auth> 'AUTH LOGIN\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Server: <response_auth_expect_user> '334 VXNlcm5hbWU6\r\n'
fandango:INFO: Current coverage: 1.00%
fandango:INFO: Client: <request_auth_user_incorrect> 'bQ==\r\n'
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
fandango:INFO: Client: <request_auth_user_incorrect> 'cmNtUk92\r\n'
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
fandango:INFO: Client: <request_ehlo> 'EHLO sUsS.8  yrs8YFpMkqNftHw.G  kRGVhjlNzP7E0k wt-kUIo.hN  .Vq SRlwe  6.E7UrXB6tKUIWw7o  J.T1m30Z  UI U5tmtHK5qjgD  eHXK  QBsWz8L7JNYo NnEkTlzbG6wYwuNiLL  .hSQPhf0CFF1wcT2w  \r\n'
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
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO MNNh31K-0uD-ipB l7.S2EkwYi02 bzd2SWm  nrqjBMxgyY-d  7L7Nv-3yboM.rCBPx  J9VA3eKAM7ja8qJmU  YNl \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nenpVVzRfemdjWkhkTFQ=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nNHhqN0dCR1lLSlVEWmRyU09D\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nTTliOHBkQ1U1\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nM0FPTk1VZVNXcFdDd1FGR1k=\r\n334 UGFzc3dvcmQ6\r\nTXpUSUxudlpV\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO mbAsqAGHuUe  6-wx6g-Ik8PSM8x6bzw q  wyIfI  mI OKXqsdIRmjwpcexvW ayezyHqf7sregwGQK  .EjvMXuRxAg m93ogl4McXF  fVXaimP1.1yLYWHxFA 9ynlONZ7tm1SHgBs9  anUv 9Ne5b1  IVtNiquavy \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nVFRkZkF5SVJLazE3UG41TV9Z\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nSg==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO a  aiIH 3bx0fg.7Aap15 \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nZkRyZUd0a3A=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ncWdxVXIxZ0hy\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\naQ==\r\n334 UGFzc3dvcmQ6\r\nVmdvS0J1cTUwZnhQWlJUMg==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nN0g=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nOWtMU0Z5aw==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nbmhwX3hhQktEVTlHRl9tRU93\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nSlNWMHdQWXN0Szl3c3FrR2JpZHQ=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nQW8yTzQ=\r\n334 UGFzc3dvcmQ6\r\nbg==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<kmwwjcpp@kgcjxbvqpzrzfi.de>\r\n250 Ok\r\nRCPT TO:<o@qgcekfq.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: gSM3Mh6LQXkRIcv\r\nfrom: rtxhlnvhcif@ygxdhnduvynkbaidtyf.de\r\nto: kdcebjcrqagh@cmqlcnphubl.de\r\ndate: Fri, 26 Oct 2001 06:54:22 +0000\r\nx-mailer: cBV lMmyufKtVNf\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nTHpkZ1ZMOWlDbXl2\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO HP9reAOQzd e  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nZGc3S1o=\r\n334 UGFzc3dvcmQ6\r\nbVl4OG8=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nUkdfUzM=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\najBQOFc5aFpkR2FmZzdN\r\n334 UGFzc3dvcmQ6\r\ndFZXSUJEVUVhY1dN\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nMXd4eA==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<nkjlaulftbabphloosg@utsnuepwbdbg.de>\r\n250 Ok\r\nRCPT TO:<vzhndadavnyhldgfw@wkrcivxfuhzwmldo.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: E5NBBYCIuBx\r\nfrom: ecrmnmndfy@smshst.de\r\nto: qaxnicjgsidfohed@lfdrvnmvgjbzoezsupdv.de\r\ndate: Fri, 10 May 2013 20:34:43 +0000\r\nx-mailer: ZFTeESnTTyB\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nYlM0NWQ5d1Q=\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO uyHMzlPlsG  ONmd8nfVN  R.f  uzz  uVGTY1Tpv6Oca91en2 S8-tGVmsFp9Lgq2gi  ZeG6PE-  6Lpd0CXQr PmfoJI \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\na0VyWDlwRFd3cDFxQ2g5\r\n334 UGFzc3dvcmQ6\r\nclJKT2RHTTRzNUZjcnptMXIyR3c=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nZmlDRDJlRzE2\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndVE=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nN3RHUTVYRk13X1lPNE9WRkFudGE=\r\n334 UGFzc3dvcmQ6\r\nc0lTVWEzWkdH\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nX2hC\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\neQ==\r\n334 UGFzc3dvcmQ6\r\nVA==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nVm1DaWNTWHVxYzlSVDN3dw==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\na083ek9HSlhfWk9WMGdhdg==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<xfzlmqtxcrsghoa@wybtgrcywcodgolzqd.de>\r\n250 Ok\r\nRCPT TO:<zr@yrjwaiffrcezc.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: BtStBLjIh\r\nfrom: i@no.de\r\nto: ffffhborbsghwuwfyrel@pquvcocppoc.de\r\ndate: Sun, 07 Dec 2036 20:15:22 +0000\r\nx-mailer: qwvsLAKu\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nRA==\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<nygp@abcmbckxac.de>\r\n250 Ok\r\nRCPT TO:<riqiik@qrw.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: 854qKFk-hV.TMRUZ_\r\nfrom: yffatxj@sshsvbgwbvkiifemk.de\r\nto: aszvlopednh@ilprslwxpjejgdsbd.de\r\ndate: Mon, 10 Dec 1973 13:52:36 +0000\r\nx-mailer: xB\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\na0VzWjczeUpiTmFnaDNnS1FX\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO V4sxR kLOGw94E3R p0rBlXLW  vgt48  YC4eL  kese E-JPO4-Ssf2-M2V0-1  LPrItph \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nVDAxVUlfZEtIdGNDaHY=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO BSHtMZ9qA ZT-IFjZXKCNLdE JW1j  3Snx1GOPtY L  5kfB-C h1S7bDHaSD  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nVENhRUNLYWVzczRvdFJGbg==\r\n334 UGFzc3dvcmQ6\r\nZjJq\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<hbkyaymcjtmioocued@zuwokgejcst.de>\r\n250 Ok\r\nRCPT TO:<daqnkwf@ht.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: s\r\nfrom: drrzvbfotisyatz@jem.de\r\nto: gm@yenlwbtybjyenjjmmtr.de\r\ndate: Sat, 17 Dec 1983 08:08:02 +0000\r\nx-mailer: XJbHDBynt\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\ndlJtVUZGCnRYdEJSd1BiSA==\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO Bb6GUsSkZR3z6gMOLbOk Z9GYha FrMPwh pZnvJHSoZtG07sw  AGxWhUWz5UAA-P5CK0l HfaYeXi68qZN.bB9Lx  JzesnQ33vuQeXBaY1p K4iVVURKhgyQ tNUbkCFFqGY9lJlWgm0Q  wNw7PlUyZXC ny8Ui uDMau \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nT2JsbXZv\r\n334 UGFzc3dvcmQ6\r\nVTR2emxzdzI3\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nZXFoREtyWg==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nOXpoUEw=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nbGZQYXZUVDQ=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nUW82SlRaQ2lqbTBxWUla\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<ttjgmpnvqxcdtdgqwt@vrgcfkdpqh.de>\r\n250 Ok\r\nRCPT TO:<f@usdpbzrarzflhvpiwt.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: dyx1\r\nfrom: kzflynnxik@stxzaeqwbn.de\r\nto: lkjajk@ebptvabigncbmafudep.de\r\ndate: Sun, 28 Jul 1985 18:15:29 +0000\r\nx-mailer: KYsHgqhluyXOfqSss\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nYnFOVnN4R283MXVENzRJamg=\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO W9u735SE9vzfweH8w  . yT \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nUnZUZTFTMFA3eUNubA==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndjZyQUpY\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nM19FV0xpSlp1\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nQmxVc2hhR1RPX1Y=\r\n334 UGFzc3dvcmQ6\r\nZF9GTU5UWk9QTG5ZR3B5TkRrYQ==\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO I I4ewsUJcQ8R  BiEAwp1U3UfUQQh9  IlUzmRtvHquB \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nZ2s0R0tfN1BUM0Q=\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\nUEtvbWZsTmUwXzFP\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<vaieahmrchjkahtcsddm@hemzaaee.de>\r\n250 Ok\r\nRCPT TO:<rvzcfiyybvtfcusuasq@iqiwolytenkeigwtgwmj.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: lKSvOPkXrrHdOgogZF\r\nfrom: gbiuelgqjqkvolszzgk@dvbacvynsdjmteusx.de\r\nto: hwcs@xcplpbgrgynn.de\r\ndate: Sat, 04 Apr 1970 21:08:39 +0000\r\nx-mailer: CHSrjEkyubce\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\ndUp0dm5hcHQzU1o4T0c=\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<xelnkeyvew@gvogboutcmlf.de>\r\n250 Ok\r\nRCPT TO:<zbgtkl@qmvungcpjn.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: k6v\r\nfrom: ddbts@umvlhxh.de\r\nto: bugfgwjhpzi@qwpemxbqlwyc.de\r\ndate: Thu, 04 Feb 1971 20:46:39 +0000\r\nx-mailer: fHSbtfYlzZgyvqaAShcg\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\naWdZ\r\n\r\n.\r\n250 Ok\r\nMAIL FROM:<gevpqwtysfwitngk@qd.de>\r\n250 Ok\r\nRCPT TO:<glqyrzqegzees@bvoiwq.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: 55:K2XpZ0Y6\r\nfrom: qf@lmghpkkbid.de\r\nto: u@mhzsu.de\r\ndate: Sat, 28 Dec 2030 21:51:02 +0000\r\nx-mailer: BCVTkuLy\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nVjlpWWlxa0hGTkRWDQ==\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO YGVqeNr4-PAnN  n22aIZH1-YNzui2Lwqx G9rzWXVgTEyMo3y bCKdjVuHodiH-yCZ mSEq0 O1A06BbTK6qTIVUv  rDVcjE  Wou5 0Ok5S73-XIF  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<hecfdep@bactyzy.de>\r\n250 Ok\r\nRCPT TO:<gikoafbcrksng@bxqzt.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: sxx\r\nfrom: kysdadlufwguisxnld@wuclg.de\r\nto: l@rxtcunkuxdmkpcao.de\r\ndate: Sat, 01 Sep 2001 13:19:14 +0000\r\nx-mailer: nLfA\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\nVmpIb2R3amhP\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO .2ryTw2a9FPSdWor LjDL1k Uv  fQ6q8voH  nxnld4mFEs  jadVhHdur9YFXXI36up  B-hYjf6JfUIH L  O KGdBj1a1  5Y91fPnZpFYSgTW3P LHe6t9 npvM69QeRs \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nS3IxckhwSkRJbWt4\r\n334 UGFzc3dvcmQ6\r\neGpCNEMz\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO 2e11fkmBPsDUl6.Hf YAqL7fU0lpO F9NK  7DkZA0 Ri51WYR7euAE87vYSC  lkhHVyZD3WF  .CLgohqZ.a  6N3tij.xlalzmJlxPOk 7xENJ231Q  fLu6EVWP.lUcVj9  N68pR8z5qsDTgk  Bu  b QXDB3lbj  QX1OAmonTue  0 gufH-W5cDi  sUThJitpTNLD50dBfA  5Xyzp5-5f.pwYZZ  c  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nMAIL FROM:<f@axd.de>\r\n250 Ok\r\nRCPT TO:<wtbjvzxeia@yvn.de>\r\n250 Ok\r\nDATA\r\n354 End data with <CR><LF>.<CR><LF>\r\nsubject: vKvhvBkjkb5x\r\nfrom: qcmwcughvlvjhkz@wjaubdzwzncyvbhlozi.de\r\nto: clknvcoprquvdta@lnnwbwlqgi.de\r\ndate: Sat, 15 May 1971 08:11:12 +0000\r\nx-mailer: BGdtmSjKxelqkanDN\r\nmime-version: 1.0\r\ncontent-type: text/plain; charset=utf-8\r\ncontent-transfer-encoding: base64\r\n\r\ndzhUNEU2Tzd4YU9TODJtc25BVk8=\r\n\r\n.\r\n250 Ok\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO u555QX6  To tgDtyy9-hPWOb dL6OdyPoLd6Ii eZ  2  gE mjnUsB  2qXpWmCW sTR7I0X  8z9Si0luGTi  teuGYH-J7nRTmBLhyn7 b-lxXqaOLVd2hQw9VqZ pdPSYWp6CodrEH2ADK2D  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\nbQ==\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ncmNtUk92\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n535 Authentication credentials invalid\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'
b'220 mac.fritz.box ESMTP FakeSMTPServer 2.4.2\r\nEHLO sUsS.8  yrs8YFpMkqNftHw.G  kRGVhjlNzP7E0k wt-kUIo.hN  .Vq SRlwe  6.E7UrXB6tKUIWw7o  J.T1m30Z  UI U5tmtHK5qjgD  eHXK  QBsWz8L7JNYo NnEkTlzbG6wYwuNiLL  .hSQPhf0CFF1wcT2w  \r\n250-mac.fritz.box\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\nAUTH LOGIN\r\n334 VXNlcm5hbWU6\r\ndGhlX3VzZXI=\r\n334 UGFzc3dvcmQ6\r\ndGhlX3Bhc3N3b3Jk\r\n235 Authentication successful.\r\nQUIT\r\n221 Bye\r\n'

Process finished with exit code 0


Coverage metrics:
Nr trees generated: 16
Nr messages exchanged: 516
Overall time elapsed: 56.98s
