import random

from evaluation.experiments.faker.faker_experiment import evaluate_faker
from evaluation.experiments.hash.hash_experiment import evaluate_hash
from evaluation.experiments.pixels.pixels_experiment import evaluate_pixels
from evaluation.experiments.transactions.transactions_experiment import (
    evaluate_transactions,
)
from evaluation.experiments.voltage.voltage_experiment import evaluate_voltage


def run_experiments():
    random_seed = 1

    # Set the random seed
    random.seed(random_seed)

    evaluate_faker()
    evaluate_hash()
    evaluate_pixels()
    evaluate_transactions()
    evaluate_voltage()


if __name__ == "__main__":
    run_experiments()
