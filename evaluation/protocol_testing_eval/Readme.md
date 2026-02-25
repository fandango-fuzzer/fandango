# Evaluation

This folder contains scripts and targets for running evaluation experiments. The evaluations measure both grammar guidance effects and protocol throughput across several targets.

## Evaluation Targets

The following protocol targets are included:

* chatgpt (OpenAI API)
* dns
* dune (Dune API)
* ftp
* smtp

Each target contains its own configuration and output directories where evaluation results are stored.

## Provided Scripts

Two Python scripts are available:

* `run_guidance_eval.py`
  Runs coverage and guidance related experiments.

* `run_throughput_eval.py`
  Measures throughput performance for each protocol target.

Both scripts define a list of protocols in the following form:

```
protocols = [
    ("dune", "dune.fan"),
    ("smtp", "smtp_client.fan"),
    ("dns", "dns.fan"),
    ("ftp", "ftp_client.fan"),
    ("chatgpt", "chatgpt.fan")
]
```

You can modify this list to include or exclude specific targets.

---

## Guidance Evaluation

Run the guidance evaluation with:

```
python run_guidance_eval.py
```

The script executes each protocol target 10 times with guidance enabled and 10 times without guidance.

### Output Locations

Results are written to:

```
./%protocol%/coverage_w_guidance
./%protocol%/coverage_wo_guidance
```

* `coverage_w_guidance` contains runs using the guidance system.
* `coverage_wo_guidance` contains runs without guidance.

### Merging Results

After completing the guidance evaluation runs, merge the collected data into a single CSV file per protocol by executing:

```
./merge_grammar_coverage.sh
```

---

## Throughput Evaluation

Run throughput experiments with:

```
python3 run_throughput_eval.py
```

Results are written to:

```
./%protocol%/throughput_test
```

The protocol list inside the script can be adjusted in the same way as for the guidance evaluation.

---

## Target Setup Requirements

Before running any evaluation, ensure that the corresponding targets are reachable.

### SMTP, FTP, DNS

Each of these targets provides a Docker setup. Start the services from their respective directories:

```
docker-compose up
```

### Dune API

Before running the dune evaluation, visit the API once to initialize it:

```
https://dune-api-a4iq.onrender.com
```

### ChatGPT

Insert your OpenAI API key into the grammar file:

```
chatgpt/chatgpt.fan
```

Replace:

```
YOUR_OPENAI_API_KEY
```

with your actual API token.

---

## Comparison against AflNet
The folder `profuzzbench/LightFTP` contains the scripts to reproduce the experiments from the paper and a readme with further instructions.

---

## Notes

* Make sure all required services are running before starting evaluations.
* Adjust the `protocols` array in the scripts if you only want to evaluate a subset of targets.
* Output directories are created automatically during execution.
