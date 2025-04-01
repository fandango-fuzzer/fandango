from evaluation.experiments.faker.faker_experiment import evaluate_faker
from evaluation.experiments.hash.hash_experiment import evaluate_hash
from evaluation.experiments.pixels.pixels_experiment import evaluate_pixels
from evaluation.experiments.voltage.voltage_experiment import evaluate_voltage

if __name__ == "__main__":
    evaluate_faker()
    evaluate_hash()
    evaluate_pixels()
    evaluate_voltage()