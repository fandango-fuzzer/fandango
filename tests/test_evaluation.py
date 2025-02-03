import unittest

from evaluation.vs_isla.run_evaluation import run_evaluation


class TestEvaluation(unittest.TestCase):
    def test_run_evaluation_one_second(self):
        # Run the evaluation for 1 second and ensure it doesn't throw exceptions
        try:
            run_evaluation(1)  # Run evaluation with time limit of 1 second
        except Exception as e:
            self.fail(f"run_evaluation raised an exception: {e}")


if __name__ == "__main__":
    unittest.main()
