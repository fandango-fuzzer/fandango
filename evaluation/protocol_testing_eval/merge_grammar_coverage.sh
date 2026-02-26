#!/bin/bash

python3 multi_run_merger.py ./smtp/coverage_w_guidance ./coverage_merged/msgs/smtp_median_grammar_coverage_guided.csv "percent___role_unique_Client"
python3 multi_run_merger.py ./smtp/coverage_wo_guidance ./coverage_merged/msgs/smtp_median_grammar_coverage_unguided.csv "percent___role_unique_Client"

python3 multi_run_merger.py ./dns/coverage_w_guidance ./coverage_merged/msgs/dns_median_grammar_coverage_guided.csv "percent___role_unique_Client"
python3 multi_run_merger.py ./dns/coverage_wo_guidance ./coverage_merged/msgs/dns_median_grammar_coverage_unguided.csv "percent___role_unique_Client"

python3 multi_run_merger.py ./ftp/coverage_w_guidance ./coverage_merged/msgs/ftp_median_grammar_coverage_guided.csv "percent___role_unique_ClientControl"
python3 multi_run_merger.py ./ftp/coverage_wo_guidance ./coverage_merged/msgs/ftp_median_grammar_coverage_unguided.csv "percent___role_unique_ClientControl"

python3 multi_run_merger.py ./dune/coverage_w_guidance ./coverage_merged/msgs/dune_median_grammar_coverage_guided.csv "percent___role_unique_Client"
python3 multi_run_merger.py ./dune/coverage_wo_guidance ./coverage_merged/msgs/dune_median_grammar_coverage_unguided.csv "percent___role_unique_Client"

python3 multi_run_merger.py ./chatgpt/coverage_w_guidance ./coverage_merged/msgs/chatgpt_median_grammar_coverage_guided.csv "percent___role_unique_Client"
python3 multi_run_merger.py ./chatgpt/coverage_wo_guidance ./coverage_merged/msgs/chatgpt_median_grammar_coverage_unguided.csv "percent___role_unique_Client"


python3 multi_run_merger.py ./smtp/coverage_w_guidance ./coverage_merged/overall/smtp_median_grammar_coverage_guided.csv "percent_<start>"
python3 multi_run_merger.py ./smtp/coverage_wo_guidance ./coverage_merged/overall/smtp_median_grammar_coverage_unguided.csv "percent_<start>"

python3 multi_run_merger.py ./dns/coverage_w_guidance ./coverage_merged/overall/dns_median_grammar_coverage_guided.csv "percent_<start>"
python3 multi_run_merger.py ./dns/coverage_wo_guidance ./coverage_merged/overall/dns_median_grammar_coverage_unguided.csv "percent_<start>"

python3 multi_run_merger.py ./ftp/coverage_w_guidance ./coverage_merged/overall/ftp_median_grammar_coverage_guided.csv "percent_<start>"
python3 multi_run_merger.py ./ftp/coverage_wo_guidance ./coverage_merged/overall/ftp_median_grammar_coverage_unguided.csv "percent_<start>"

python3 multi_run_merger.py ./dune/coverage_w_guidance ./coverage_merged/overall/dune_median_grammar_coverage_guided.csv "percent_<start>"
python3 multi_run_merger.py ./dune/coverage_wo_guidance ./coverage_merged/overall/dune_median_grammar_coverage_unguided.csv "percent_<start>"

python3 multi_run_merger.py ./chatgpt/coverage_w_guidance ./coverage_merged/overall/chatgpt_median_grammar_coverage_guided.csv "percent_<start>"
python3 multi_run_merger.py ./chatgpt/coverage_wo_guidance ./coverage_merged/overall/chatgpt_median_grammar_coverage_unguided.csv "percent_<start>"