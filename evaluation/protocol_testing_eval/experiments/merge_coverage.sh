#!/bin/bash

python3 merge_coverage.py ./opensmtpd/coverage_guided ./median_coverage/msgs/smtp_median_grammar_coverage_guided.csv "percent___role_unique_Client"
python3 merge_coverage.py ./opensmtpd/coverage_unguided ./median_coverage/msgs/smtp_median_grammar_coverage_unguided.csv "percent___role_unique_Client"

python3 merge_coverage.py ./bind9/coverage_guided ./median_coverage/msgs/dns_median_grammar_coverage_guided.csv "percent___role_unique_Client"
python3 merge_coverage.py ./bind9/coverage_unguided ./median_coverage/msgs/dns_median_grammar_coverage_unguided.csv "percent___role_unique_Client"

python3 merge_coverage.py ./lightftp/coverage_guided ./median_coverage/msgs/ftp_median_grammar_coverage_guided.csv "percent___role_unique_ClientControl"
python3 merge_coverage.py ./lightftp/coverage_unguided ./median_coverage/msgs/ftp_median_grammar_coverage_unguided.csv "percent___role_unique_ClientControl"

python3 merge_coverage.py ./wireguard/coverage_guided ./median_coverage/msgs/wireguard_median_grammar_coverage_guided.csv "percent___role_unique_Client"
python3 merge_coverage.py ./wireguard/coverage_unguided ./median_coverage/msgs/wireguard_median_grammar_coverage_unguided.csv "percent___role_unique_Client"


python3 merge_coverage.py ./opensmtpd/coverage_guided ./median_coverage/overall/smtp_median_grammar_coverage_guided.csv "percent_<start>"
python3 merge_coverage.py ./opensmtpd/coverage_unguided ./median_coverage/overall/smtp_median_grammar_coverage_unguided.csv "percent_<start>"

python3 merge_coverage.py ./bind9/coverage_guided ./median_coverage/overall/dns_median_grammar_coverage_guided.csv "percent_<start>"
python3 merge_coverage.py ./bind9/coverage_unguided ./median_coverage/overall/dns_median_grammar_coverage_unguided.csv "percent_<start>"

python3 merge_coverage.py ./lightftp/coverage_guided ./median_coverage/overall/ftp_median_grammar_coverage_guided.csv "percent_<start>"
python3 merge_coverage.py ./lightftp/coverage_unguided ./median_coverage/overall/ftp_median_grammar_coverage_unguided.csv "percent_<start>"

python3 merge_coverage.py ./wireguard/coverage_guided ./median_coverage/overall/wireguard_median_grammar_coverage_guided.csv "percent_<start>"
python3 merge_coverage.py ./wireguard/coverage_unguided ./median_coverage/overall/wireguard_median_grammar_coverage_unguided.csv "percent_<start>"