from typing import List

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import jaccard_score

from evaluation.evaluation.csv_evaluation.csv_evaluation import evaluate_csv
from evaluation.evaluation.rest_evaluation.rest_evaluation import evaluate_rest
from evaluation.evaluation.xml_evaluation.xml_evaluation import evaluate_xml
from fandango.language.tree import DerivationTree





def run_evaluation():
    evaluate_csv()
    evaluate_rest()
    evaluate_xml()


if __name__ == "__main__":
    run_evaluation()
