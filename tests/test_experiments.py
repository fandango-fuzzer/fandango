import unittest

from evaluation.experiments.run_experiments import run_experiments


class TestExperiments(unittest.TestCase):
    def test_run_experiments_one_second(self):
        try:
            run_experiments()
        except Exception as e:
            self.fail(f"run_evaluation raised an exception: {e}")


if __name__ == "__main__":
    unittest.main()
