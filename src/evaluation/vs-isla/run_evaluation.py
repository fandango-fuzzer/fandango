from csv_evaluation.csv import evaluate_csv
from rest.rest import evaluate_rest
from scriptsizec.scriptsizec import evaluate_scriptsizec
from tar.tar import evaluate_tar
from xml_.xml import evaluate_xml


def run_evaluation():
    evaluate_csv()
    evaluate_rest()
    evaluate_scriptsizec()
    evaluate_tar()
    evaluate_xml()


if __name__ == "__main__":
    run_evaluation()
