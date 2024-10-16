from faker.faker import evaluate_faker
from hash.hash import evaluate_hash
from img.img import evaluate_img
from int.int import evaluate_int
from voltage.voltage import evaluate_voltage


def run_evaluation():
    evaluate_faker()
    evaluate_hash()
    evaluate_img()
    evaluate_int()
    evaluate_voltage()


if __name__ == "__main__":
    run_evaluation()
