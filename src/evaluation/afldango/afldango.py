import warnings

from fandango.evolution.algorithm import FANDANGO
from fandango.language.parse import parse_file

warnings.filterwarnings("ignore")

if __name__ == '__main__':
    grammar, constraints = parse_file('xml.fan')
    inputs = FANDANGO(grammar, constraints, verbose=False).evolve()
